from django.apps import AppConfig


class TbotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.tbot_base'  # must contain full path to this app
    verbose_name = 'Настройки Telegram бота'
    verbose_name_plural = 'Настройки Telegram ботов'
