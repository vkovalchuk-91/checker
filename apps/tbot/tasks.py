from apps.celery import celery_app as app
from apps.tbot_base.bot import tbot as bot


@app.task(name='send_bot_message')
def send_bot_message(**kwargs):
    telegram_id = kwargs.get('telegram_id')
    message = kwargs.get('message')
    bot.send_message(telegram_id, message)
