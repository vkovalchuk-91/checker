from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic.list import BaseListView

from apps.task_manager.models import SessionTaskManager


class BaseCheckerListView(BaseListView):
    model_class = None
    template_name = None
    context_object_name = None
    checker_type = None

    def get_queryset(self):
        user = self.request.user
        return self.model_class.objects.filter(
            param_type__checker_task_parameters__user_id=user.id,
            param_type__checker_task_parameters__is_delete=False,
        )

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
