from django.shortcuts import redirect
from django.urls import reverse

from apps.accounts.utils.telegram import unlink_telegram_id_from_user, has_user_related_telegram_id


def link_telegram(request):
    if has_user_related_telegram_id(request):
        unlink_telegram_id_from_user(request)
    else:
        return redirect(reverse('index'))
    return redirect(request.path)
