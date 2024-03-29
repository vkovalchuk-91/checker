import logging

from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse

from apps.accounts.utils.telegram import check_linked_telegram_id, has_user_related_telegram_id


def index(request):
    check_linked_telegram_id(request)
    # messages.error(request, 'error')
    # messages.warning(request, 'warning')
    # messages.success(request, 'success')
    # messages.info(request, 'info')
    return render(request, "index.html")


def telegram(request):
    if has_user_related_telegram_id(request):
        messages.info(request, "Користувач вже має прив'язаний Telegram-аккаунт")
        return redirect(reverse('index'))
    elif not request.user.is_authenticated:
        messages.info(request, "Для того щоб прив'язати Telegram-аккаунт потрібно спочатку авторизуватися")
        return redirect(reverse('index'))
    else:
        return render(request, "registration/telegram.html")
