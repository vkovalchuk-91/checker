from django.http import HttpResponseRedirect
from django.shortcuts import redirect

from apps.accounts.utils.telegram import unlink_telegram_id_from_user, has_user_related_telegram_id


def link_unlink_telegram(request):
    if has_user_related_telegram_id(request):
        unlink_telegram_id_from_user(request)
    else:
        return redirect("https://t.me/CheckerGeekHubBot")
    previous_page = request.META.get('HTTP_REFERER', '/')
    return HttpResponseRedirect(previous_page)
