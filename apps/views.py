from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.accounts.utils.telegram import check_linked_telegram_id, has_user_related_telegram_id
from apps.forms import ContactForm
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
