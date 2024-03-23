from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic.list import ListView

from apps.uz_ticket_checker.models import TicketSearchParameter


class UzTicketCheckerListView(ListView):
    model = TicketSearchParameter
    template_name = 'uz_ticket_checker/index.html'
    context_object_name = 'uz_ticket_checker'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['seat_types'] = [i.name.replace('_', ' ').lower() for i in SeatType if i != SeatType.DEFAULT]
        return context

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            messages.warning(self.request, _('Invalid access. Please log in.'))
            return redirect(reverse('index'))

        return super().get(request, *args, **kwargs)
