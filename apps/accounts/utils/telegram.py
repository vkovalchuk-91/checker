import re

from django.contrib import messages
from django.utils.safestring import mark_safe

from apps.accounts.models import User, PersonalSetting
from apps.task_manager.models import CheckerTask


def check_linked_telegram_id(request):
    user = request.user
    if user.is_authenticated and (user.personal_setting is None or user.personal_setting.telegram_user_id == 0):
        link = '<a href="https://t.me/CheckerGeekHubBot">CheckerGeekHubBot</a>'
        message = "Для можливості повноцінного використання сервісу Checker, будь-ласка перейдіть в {} та підв'яжіть свій Telegram-аккаунт до вашого облікового запису в сервісі Checker".format(
            link)
        messages.info(request, mark_safe(message))


def has_user_related_telegram_id(request):
    return request.user.is_authenticated and request.user.personal_setting is not None and request.user.personal_setting.telegram_user_id != 0


def check_is_user_unregistered_in_data_base_by_telegram_id(user_telegram_id):
    personal_setting = PersonalSetting.objects.filter(telegram_user_id=user_telegram_id).first()
    if personal_setting is None:
        return True
    return User.objects.filter(personal_setting=personal_setting).first() is None


def check_is_user_exist_in_data_base_by_email(email):
    return User.objects.filter(email=email.lower()).first() is not None


def check_has_exist_user_related_tg_by_email(email):
    user = User.objects.filter(email=email.lower()).first()
    if user is not None and user.personal_setting is not None and user.personal_setting.telegram_user_id != 0:
        return True
    return False


def validate_email(email):
    email_pattern = r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$"
    if not re.match(email_pattern, email, re.IGNORECASE):
        return False
    return True


def get_user_checkers_number(user):
    checker_tasks = CheckerTask.objects.filter(user=user).all()
    checkers_number = {}
    for checker_task in checker_tasks:
        param_category_name = checker_task.task_param.param_type.param_category_name
        if param_category_name in checkers_number:
            checkers_number[param_category_name] = checkers_number[param_category_name] + 1
        else:
            checkers_number[param_category_name] = 1
    return checkers_number


def get_registered_user_with_linked_tg_by_telegram_id(user_telegram_id):
    personal_setting = PersonalSetting.objects.filter(telegram_user_id=user_telegram_id).first()
    return User.objects.filter(personal_setting=personal_setting).first()


def link_telegram_id_to_user(tg_user_id, user_email):
    user = User.objects.filter(email=user_email.lower()).first()
    personal_setting = user.personal_setting
    if personal_setting is None:
        personal_setting = PersonalSetting.objects.create(telegram_user_id=tg_user_id)
        user.personal_setting = personal_setting
    else:
        personal_setting.telegram_user_id = tg_user_id
    personal_setting.save()
    user.save()


def unlink_telegram_id_from_user(request):
    personal_setting = request.user.personal_setting
    personal_setting.telegram_user_id = 0
    personal_setting.save()
