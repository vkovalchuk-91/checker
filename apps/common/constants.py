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
    'Сидячий 1-й клас', 'Сидячий 2-й клас', 'Плацкарт Економ', 'Плацкарт Стандартний', 'Плацкарт Покращений',
    'Купе Економ', 'Купе Стандартний', 'Купе Покращений', 'Люкс Стандартний'
]

STATIONS = {}

UKRAINIAN_ALPHABET = ['А', 'Б', 'В', 'Г', 'Ґ', 'Д', 'Е', 'Є', 'Ж', 'З', 'И', 'І', 'Ї', 'Й', 'К', 'Л', 'М', 'Н', 'О',
                      'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ь', 'Ю', 'Я']
