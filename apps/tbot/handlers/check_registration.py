from apps.accounts.utils.telegram import check_is_user_unregistered_in_data_base_by_telegram_id, \
    check_has_exist_user_related_tg_by_email, check_is_user_exist_in_data_base_by_email, get_user_checkers_number, \
    validate_email, link_telegram_id_to_user, get_registered_user_with_linked_tg_by_telegram_id
from apps.tbot_base.bot import tbot as bot

registered_users = [396264878]


@bot.message_handler(func=lambda message: True)
def send_registration_info(message):
    user_id = message.chat.id
    tg_username = message.chat.username
    user_text = message.text
    is_user_unregistered = check_is_user_unregistered_in_data_base_by_telegram_id(user_id)

    if is_user_unregistered and user_text == '/start':
        bot.send_message(message.from_user.id,
                         f"Привіт! Щоб користуватися оповіщенням в Telegram, будь-ласка, введіть e-mail "
                         f"зареєстрованого вами користувача на сайті Checker.")
    elif is_user_unregistered and not validate_email(user_text):
        bot.send_message(user_id,
                         f"Ви ввели невалідний E-mail '{user_text}', будь-ласка повторіть спробу.")
    elif is_user_unregistered and not check_is_user_exist_in_data_base_by_email(user_text):
        bot.send_message(user_id,
                         f"Не знайдено зареєстрованого користувача з E-mail {user_text}, будь-ласка "
                         f"зареєструйтесь на сайті Checker в розділі реєстрація та повторіть спробу.")
    elif is_user_unregistered and check_has_exist_user_related_tg_by_email(user_text):
        bot.send_message(user_id,
                         f"E-mail користувача {user_text.lower()} вже містить пов'язаний з ним Telegram аккаунт, "
                         f"будь-ласка введіть e-mail іншого користувача або видаліть у користувача з e-mail {user_text}"
                         f"пов'язаний з ним Telegram аккаунт сайті Checker в розділі налаштування та повторіть спробу.")
    else:
        if is_user_unregistered:
            link_telegram_id_to_user(user_id, user_text)
        get_linked_tg_user_response(tg_username, user_id)


def get_linked_tg_user_response(tg_username, tg_user_id):
    user = get_registered_user_with_linked_tg_by_telegram_id(tg_user_id)
    checkers_number = get_user_checkers_number(user)
    response_text = f"Вітаємо @{tg_username}! Ваш Telegram аккаунт пов'язаний з користувачем {user.email.lower()}\n"
    if len(checkers_number) == 0:
        response_text += f"На даний момент у вас немає жодних збережених чекерів"
    elif len(checkers_number) == 1:
        checker_service_name = next(iter(checkers_number))
        checker_qty = checkers_number[checker_service_name]
        response_text += f"На даний момент у вас для сервіса '{checker_service_name}' кількість активних чекерів - {checker_qty}"
    else:
        response_text = f"На даний момент у вас така кількість активних чекерів:\n"
        for checker_service_name, checker_qty in checkers_number.items():
            response_text += f"Сервіс '{checker_service_name}' - {checker_qty}\n"
    bot.send_message(tg_user_id, response_text)
