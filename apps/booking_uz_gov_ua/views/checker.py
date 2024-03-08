from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic.list import ListView

from apps.booking_uz_gov_ua.models import Checker


class CheckerListView(ListView):
    template_name = 'booking_uz_gov_ua/index.html'
    context_object_name = 'checkers'

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return []

        queryset = Checker.objects.filter(user_id=user.id)
        return queryset

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            messages.warning(self.request, _('Unauthorized access. Please log in.'))
            return redirect(reverse('index'))

        return super().get(request, *args, **kwargs)
