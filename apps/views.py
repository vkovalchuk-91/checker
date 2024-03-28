from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _

from apps.task_manager.models import SessionTaskManager


def index(request):
    SessionTaskManager(request)
    return render(request, "index.html")


def redirect_to_index_page(request):
    messages.warning(request, _('Invalid access. User is blocked. Please try another.'))
    return redirect("index")
