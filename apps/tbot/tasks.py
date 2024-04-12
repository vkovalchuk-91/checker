from loguru import logger

from apps.accounts.models import User
from apps.celery import celery_app as app
from apps.tbot_base.bot import tbot as bot


@app.task(name='send_bot_message')
def send_bot_message(**kwargs):
    telegram_id = kwargs.get('telegram_id')
    message = kwargs.get('message')
    bot.send_message(telegram_id, message)


@app.task(name='send_feedback_bot_message_to_admins')
def send_feedback_bot_message_to_admins(**kwargs):
    contact_info = kwargs.get('contact_info')
    subject = kwargs.get('subject')
    description = kwargs.get('description')
    logger.debug(description)
    admins = User.objects.filter(is_superuser=True, personal_setting__isnull=False).exclude(
        personal_setting__telegram_user_id=0).all()
    logger.debug(admins)
    for admin in admins:
        bot.send_message(admin.personal_setting.telegram_user_id, f"Новий відгук на сервісі Checker!\n"
                                                                  f"Від кого: {contact_info}\n"
                                                                  f"Тема: {subject}\n"
                                                                  f"Опис: {description}")
