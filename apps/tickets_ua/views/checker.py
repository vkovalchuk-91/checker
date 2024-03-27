from django.views.generic import ListView

from apps.common.views import BaseCheckerListView
from apps.common.enums.checker_name import CheckerTypeName
from apps.tickets_ua.enums.seat import SeatType
from apps.tickets_ua.models import Checker


class CheckerListView(BaseCheckerListView, ListView):
    model_class = Checker
    template_name = 'tickets_ua/index.html'
    context_object_name = 'checkers'
    checker_type = CheckerTypeName.TICKETS_UA

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['seat_types'] = [i.name.replace('_', ' ').lower() for i in SeatType if i != SeatType.DEFAULT]
        return context
