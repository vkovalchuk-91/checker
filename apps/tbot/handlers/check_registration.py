from apps.tbot_base.bot import tbot as bot

registered_users = [396264878]


def check_existing_user_email(email):
    return True


def get_active_checkers_number():
    return {'UZ-Tickets': 4}


def get_related_email():
    return 'example@example.com'


def check_existing_user_email_with_related_tg(email):
    return False


def check_is_user_registered(user_id):
    return True


@bot.message_handler(func=lambda message: True)
def send_registration_info(message):
    user_id = message.chat.id
    tg_username = message.chat.username
    user_text = message.text

    is_user_unregistered = check_is_user_registered(user_id)
    has_existing_user_email_with_related_tg = check_existing_user_email_with_related_tg(user_text)
    has_existing_user_email = check_existing_user_email(user_text)

    if is_user_unregistered and user_text == '/start':
        bot.send_message(message.from_user.id,
                         f"Привіт! Щоб користуватися оповіщенням в Telegram, будь-ласка, введіть e-mail "
                         f"зареєстрованого вами користувача на сайті Checker.")
    elif is_user_unregistered and has_existing_user_email:
        bot.send_message(user_id,
                         f"Не знайдено зареєстрованого користувача з E-mail {user_text}, будь-ласка "
                         f"зареєструйтесь на сайті Checker в розділі реєстрація та повторіть спробу.")
    elif is_user_unregistered and has_existing_user_email_with_related_tg:
        bot.send_message(user_id,
                         f"E-mail користувача {user_text} вже містить пов'язаний з ним Telegram аккаунт, будь-ласка "
                         f"введіть e-mail іншого користувача або видаліть у користувача з e-mail {user_text}"
                         f"пов'язаний з ним Telegram аккаунт сайті Checker в розділі налаштування та повторіть спробу.")
    else:
        get_registered_user_response(tg_username, user_id)


def get_registered_user_response(tg_username, user_id):
    email = get_related_email()
    checkers_number = get_active_checkers_number()
    response_text = f"Вітаємо @{tg_username}! Ваш Telegram аккаунт пов'язаний з користувачем {email}\n"
    if len(checkers_number) == 1:
        checker_service_name = next(iter(checkers_number))
        checker_qty = checkers_number[checker_service_name]
        response_text += f"На даний момент у вас {checker_qty} активних чекерів сервісу {checker_service_name}"
    else:
        response_text = f"На даний момент у вас така кількість активних чекерів:\n"
        for checker_service_name, checker_qty in checkers_number.items():
            response_text += f"Сервіс {checker_service_name} - {checker_qty}\n"
    bot.send_message(user_id, response_text)
