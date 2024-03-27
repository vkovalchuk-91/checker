from django.shortcuts import render

from apps.task_manager.models import SessionCheckerCounter


def index(request):
    SessionCheckerCounter(request)
    return render(request, "index.html")
