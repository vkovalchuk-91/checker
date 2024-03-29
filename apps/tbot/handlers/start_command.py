from telebot import types

from tbot.handlers.check_registration import get_registered_user_response, check_is_user_registered
from tbot_base.bot import tbot as bot


@bot.message_handler(commands=['start'])
def text_messages(message: types.Message):
    user_id = message.chat.id
    tg_username = message.chat.username
    is_user_registered = check_is_user_registered(user_id)
    if is_user_registered:
        bot.send_message(message.from_user.id,
                         f"Привіт! Щоб користуватися оповіщенням в Telegram, будь-ласка, введіть e-mail "
                         f"зареєстрованого вами користувача на сайті Checker.")
    else:
        get_registered_user_response(tg_username, user_id)
