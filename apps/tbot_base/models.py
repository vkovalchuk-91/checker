import os
from pathlib import Path

import environ
from django.db import models
from django.core.exceptions import ValidationError

from loguru import logger
from telebot.apihelper import ApiTelegramException

AUTO_FILLED_IN = 'это поле автоматически заполнится'


class BotConfig(models.Model):
    """ Base Telegram bot model """
    title = models.CharField(verbose_name='Название Бота', max_length=100,
                             blank=True, editable=False, default=AUTO_FILLED_IN)
    link = models.URLField(verbose_name='Ссылка на бот', max_length=150,
                           blank=True, editable=False, default=AUTO_FILLED_IN)
    username = models.CharField(max_length=100, blank=True, editable=False,
                                default=AUTO_FILLED_IN)
    tid = models.CharField(max_length=100, blank=True, editable=False,
                           default=AUTO_FILLED_IN)

    token = models.CharField(verbose_name='Токен Бота', max_length=150,
                             help_text='вставьте токен, полученный у BotFather')
    server_url = models.CharField(verbose_name='Webhook Url', max_length=200,
                                  help_text='https://<название домена>')

    is_active = models.BooleanField(default=True)

    def update_bot_config(self):
        from .bot import tbot

        tbot.config = self
        tbot.token = self.token

        return tbot

    def set_fields(self, tbot):
        j_data = tbot.get_me()

        self.title = j_data.first_name
        self.username = j_data.username
        self.tid = j_data.id
        self.link = f"https://t.me/{j_data.username}"

    def set_hook(self, tbot):
        webhook_url = f"{self.server_url}/get_tel_hook/"
        result = tbot.set_webhook(webhook_url, drop_pending_updates=True, timeout=10)
        logger.info(f"Webhook: {result}")

    def set_active_config(self):
        if self.is_active:
            other_active_configs = BotConfig.objects.filter(is_active=True)
            for config in other_active_configs:
                if config.pk != self.pk:
                    config.is_active = False
                    config.save()

    def clean(self):
        tbot = self.update_bot_config()

        try:
            self.set_fields(tbot)
            self.set_hook(tbot)
            self.set_active_config()

        except ApiTelegramException as e:
            logger.debug(e)
            raise ValidationError(
                'Неверный указан "Токен Бота" либо "Webhook Url"! '
                'Исправьте ошибку и сохраните конфигурацию ещё раз.'
            )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Настройки Telegram бота'
        verbose_name_plural = 'Настройки Telegram ботов'


env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


try:
    # logger.debug(3333)
    bot_config_obj = BotConfig.objects
    new_bot_config_from_env_condition_1 = not bot_config_obj.exists()
    new_bot_config_from_env_condition_2 = len(bot_config_obj.all()) == 1 and (
            bot_config_obj.first().token != env('BOT_TOKEN') or bot_config_obj.first().server_url != env(
        'BOT_WEBHOOK_URL'))

    if new_bot_config_from_env_condition_1 or new_bot_config_from_env_condition_2:
        new_config = BotConfig(title=env('BOT_TITLE'), link=env('BOT_LINK'), username=env('BOT_USERNAME'),
                               tid=env('BOT_TELEGRAM_ID'), token=env('BOT_TOKEN'),
                               server_url=env('BOT_WEBHOOK_URL'))
        new_config.clean()
        new_config.save()
except Exception as e:
    logger.info(e)
