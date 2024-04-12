from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.accounts.utils.telegram import check_linked_telegram_id, has_user_related_telegram_id
from apps.forms import ContactForm, MaxQueryNumberForm, RegularUsersUpdatePeriodForm, VipUsersUpdatePeriodForm
from apps.task_manager.models import SessionTaskManager
from apps.tbot.tasks import send_feedback_bot_message_to_admins


def index(request):
    check_linked_telegram_id(request)
    SessionTaskManager(request)
    return render(request, "index.html")


def redirect_to_index_page(request):
    messages.warning(request, _('Invalid access. User is blocked. Please try another.'))
    return redirect("index")


def telegram(request):
    if has_user_related_telegram_id(request):
        messages.info(request, "Користувач вже має прив'язаний Telegram-аккаунт")
        return redirect(reverse('index'))
    elif not request.user.is_authenticated:
        messages.info(request, "Для того щоб прив'язати Telegram-аккаунт потрібно спочатку авторизуватися")
        return redirect(reverse('index'))
    else:
        return render(request, "registration/telegram.html")


def feedback(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_info = form.cleaned_data['contact_info']
            subject = form.cleaned_data['subject']
            description = form.cleaned_data['description']
            send_feedback_bot_message_to_admins.delay(contact_info=contact_info, subject=subject,
                                                      description=description)
            messages.info(request, 'Дані успішно відправлено адміністраторам!')
            return redirect(reverse('index'))
        else:
            messages.error(request, 'Всі поля мають бути заповнені!')
    else:
        form = ContactForm()
    return render(request, 'feedback.html', {'form': form})


def additional_settings(request):
    if request.user and not request.user.is_superuser:
        messages.info(request, 'Доступ до сторінки додаткових налаштувань мають лише суперюзери.')
        previous_page = request.META.get('HTTP_REFERER', '/')
        return HttpResponseRedirect(previous_page)

    SessionTaskManager(request)

    context = {'max_query_number': settings.MAX_QUERY_NUMBER_DEFAULT,
               'regular_users_update_period': settings.TASK_UPDATE_PERIOD_DEFAULT,
               'vip_users_update_period': settings.VIP_USER_TASK_UPDATE_PERIOD_DEFAULT}
    return render(request, "settings.html", context)


def change_max_query_number(request):
    if request.user and not request.user.is_superuser:
        messages.info(request, 'Доступ до зміни додаткових налаштувань мають лише суперюзери.')
        previous_page = request.META.get('HTTP_REFERER', '/')
        return HttpResponseRedirect(previous_page)

    if request.method == 'POST':
        form = MaxQueryNumberForm(request.POST)
        if form.is_valid():
            settings.MAX_QUERY_NUMBER_DEFAULT = int(form.cleaned_data['max_query_number'])
            messages.info(request, 'Максимальну кількість cheker-ів для REGULAR користувачів успішно змінено!')
            return redirect(reverse('settings'))
        else:
            messages.error(request, 'Змінювані поля мають бути заповнені!')
    else:
        form = ContactForm()

    return render(request, 'settings.html', {'form': form})


def change_regular_users_update_period(request):
    if request.user and not request.user.is_superuser:
        messages.info(request, 'Доступ до зміни додаткових налаштувань мають лише суперюзери.')
        previous_page = request.META.get('HTTP_REFERER', '/')
        return HttpResponseRedirect(previous_page)

    if request.method == 'POST':
        form = RegularUsersUpdatePeriodForm(request.POST)
        if form.is_valid():
            settings.TASK_UPDATE_PERIOD_DEFAULT = int(form.cleaned_data['regular_users_update_period'])
            messages.info(request, 'Час через який будуть повторюватися cheker запити для REGULAR користувачів успішно змінено!')
            return redirect(reverse('settings'))
        else:
            messages.error(request, 'Змінювані поля мають бути заповнені!')
    else:
        form = ContactForm()

    return render(request, 'settings.html', {'form': form})


def change_vip_users_update_period(request):
    if request.user and not request.user.is_superuser:
        messages.info(request, 'Доступ до зміни додаткових налаштувань мають лише суперюзери.')
        previous_page = request.META.get('HTTP_REFERER', '/')
        return HttpResponseRedirect(previous_page)

    if request.method == 'POST':
        form = VipUsersUpdatePeriodForm(request.POST)
        if form.is_valid():
            settings.VIP_USER_TASK_UPDATE_PERIOD_DEFAULT = int(form.cleaned_data['vip_users_update_period'])
            messages.info(request, 'Час через який будуть повторюватися cheker запити для VIP користувачів успішно змінено!')
            return redirect(reverse('settings'))
        else:
            messages.error(request, 'Змінювані поля мають бути заповнені!')
    else:
        form = ContactForm()

    return render(request, 'settings.html', {'form': form})
