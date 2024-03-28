from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic.list import BaseListView

from apps.task_manager.models import CheckerTask, SessionTaskManager


class BaseCheckerListView(BaseListView):
    model_class = None
    template_name = None
    context_object_name = None
    checker_type = None

    def get_queryset(self):
        user = self.request.user
        checker_ids = CheckerTask.objects.filter(
            user_id=user.id,
            checker_type=self.checker_type.value
        ).values_list('checker_id')
        return self.model_class.objects.filter(pk__in=checker_ids)

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            messages.warning(self.request, _('Invalid access. Please log in.'))
            return redirect(reverse('index'))

        if not user.is_active:
            messages.warning(self.request, _('User blocked. You can logout.'))
            return redirect(reverse('index'))

        SessionTaskManager(request)

        return super().get(request, *args, **kwargs)

    class Meta:
        abstract = True
