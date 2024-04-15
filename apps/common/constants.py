import os
from pathlib import Path

import environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


BOT_TITLE = env('BOT_TITLE')
BOT_LINK = env('BOT_LINK')
BOT_USERNAME = env('BOT_USERNAME')
BOT_TELEGRAM_ID = env('BOT_TELEGRAM_ID')
BOT_TOKEN = env('BOT_TOKEN')
BOT_WEBHOOK_URL = env('BOT_WEBHOOK_URL')

SEAT_TYPES = [
    {'seat_type': 'seaters', 'seat_type_name': 'Сидячі місця'},
    {'seat_type': 'lowerSleepers', 'seat_type_name': 'Нижні місця'},
    {'seat_type': 'upperSleepers', 'seat_type_name': 'Верхні місця'},
    {'seat_type': 'lowerSideSleepers', 'seat_type_name': 'Нижні бокові місця'},
    {'seat_type': 'upperSideSleepers', 'seat_type_name': 'Верхні бокові місця'}
]

WAGON_TYPES = [
    "Сидячий 1-й клас", "Сидячий 2-й клас", "Сидячий 3-й клас", "Плацкарт Економ", "Плацкарт Стандартний",
    "Плацкарт Покращений", "Купе Економ", "Купе Стандартний", "Купе Покращений", "Люкс Економ", "Люкс Стандартний",
    "Люкс Покращений", "М'який Загальний"
]

STATIONS = {}

UKRAINIAN_ALPHABET = ['А', 'Б', 'В', 'Г', 'Ґ', 'Д', 'Е', 'Є', 'Ж', 'З', 'И', 'І', 'Ї', 'Й', 'К', 'Л', 'М', 'Н', 'О',
                      'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ь', 'Ю', 'Я']

USER_UPDATE_PERIOD_DEFAULT = 0

DATA_FORMAT_DEFAULT = "%Y-%m-%d"
TIME_FORMAT_DEFAULT = "%H:%M"

ACTIVE_TITLE_CATEGORIES_DEFAULT = ["Побутова техніка", "Комп'ютери", "Смартфони"]

TITLE_REGEX_DEFAULT = r"^[a-zA-Zа-яА-ЯєіїЄІЇ0-9\-',. ]{2,100}$"

RUN_VIP_CHECKER_INTERVAL_DEFAULT = 1
RUN_ALL_CHECKER_INTERVAL_DEFAULT = 5
TIME_SLEEP_DEFAULT = 2
LOCK_EXPIRE_DEFAULT = 60 * 10

CACHE_SAVE_INTERVAL_DEFAULT = 60 * 60

RUN_UZ_TICKET_CELERY_BEAT_INTERVAL_DEFAULT = int(env('RUN_UZ_TICKET_CELERY_BEAT_INTERVAL_DEFAULT'))  # Seconds
TICKETS_MATCHES_CASH_EXPIRE_RATIO = int(env('TICKETS_MATCHES_CASH_EXPIRE_RATIO'))  # User_update_period (minutes) x2
TG_MENUS_EXPIRE_TIME = int(env('TG_MENUS_EXPIRE_TIME'))  # 5 Minutes
