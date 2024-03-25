from settings.base import *

import socket

from apps.celery import celery_app as apps

# third part
INSTALLED_APPS += [
    "anymail",
    'django_extensions',

    'rest_framework',

    # project
    'apps.accounts',
    'apps.hotline_ua',
    'apps.tickets_ua',

    # project template tags

    # OAuth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    # celery
    'django_celery_results',
]

# OAuth
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'EMAIL_AUTHENTICATION': True,
        'APP': {
            'client_id': env("CLIENT_ID"),
            'secret': env("CLIENT_SECRET"),
            'key': '',
        },
    }
}

ACCOUNT_USER_MODEL_USERNAME_FIELD = 'email'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_ADAPTER = 'apps.accounts.adapter.GoogleAccountAdapter'

MIDDLEWARE += [
    'allauth.account.middleware.AccountMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

# redis
REDIS_URL = env("REDIS_URL", default="redis://redis:6379")

# Celery
CELERY_TIMEZONE = "Europe/Kiev"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_BROKER_URL = f'{REDIS_URL}/0'
CELERY_RESULT_BACKEND = f'{REDIS_URL}/0'

# logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# rest
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

SPECTACULAR_SETTINGS = {
    'TITLE': 'Project API',
    'DESCRIPTION': 'Final project description',
    'VERSION': '0.0.1',
    'SERVE_INCLUDE_SCHEMA': False,
}

TEMPLATES[0]['DIRS'].append('templates')

# email
if ENVIRONMENT == DEVELOPMENT_ENVIRONMENT:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"

ANYMAIL = {
    "MAILGUN_API_KEY": env('MAILGUN_API_KEY'),
    "MAILGUN_SENDER_DOMAIN": env('MAILGUN_SENDER_DOMAIN'),
}
DEFAULT_FROM_EMAIL = env("FROM_EMAIL", default="prodaction@example.com")

FRONTEND_HOST = env("FRONTEND_HOST", default="http://localhost:8000")
FRONTEND_CONFIRM_EMAIL_PATH = "/accounts/confirm-email/{uid}/{token}/"

# authorization
LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'index'
LOGIN_URL = 'login'

LANGUAGES = [
    ('en', 'English'),
    ('uk', 'Ukrainian'),
]
LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]
