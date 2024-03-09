from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic.list import ListView

from apps.tickets_ua.enums.seat_type import SeatType
from apps.tickets_ua.models import Checker


class CheckerListView(ListView):
    template_name = 'tickets_ua/index.html'
    context_object_name = 'checkers'

    def get_queryset(self):
        user = self.request.user
        return Checker.objects.filter(user_id=user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['seat_types'] = [i.name.replace('_', ' ').lower() for i in SeatType if i != SeatType.DEFAULT]
        return context

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            messages.warning(self.request, _('Unauthorized access. Please log in.'))
            return redirect(reverse('index'))

        return super().get(request, *args, **kwargs)
