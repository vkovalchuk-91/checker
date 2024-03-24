from django.shortcuts import render
from django.views.generic import ListView

from apps.accounts.models import CheckerTask
from apps.uz_ticket_checker.models import TicketSearchParameter, Station
from apps.uz_ticket_checker.services.checker_service import add_new_checker


class CheckersListView(ListView):
    model = CheckerTask
    template_name = 'uz_ticket_checker/checker.html'
    context_object_name = 'checkers'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        queryset = queryset.filter(user=user)
        return queryset


def checker_add(request):
    # if request.user and not request.user.is_superuser:
    #     messages.error(request, 'Доступ до сторінки додавання нових продуктів мають лише суперюзери.')
    #     return redirect(reverse('products:products_list'))

    if request.method == 'GET':
        departure_station_str = request.GET.get('from_station')
        arrival_station_str = request.GET.get('to_station')
        start_date_str = request.GET.get('from_date')
        end_date_str = request.GET.get('to_date', start_date_str)
        train_numbers = request.GET.get('train_numbers', [])
        wagon_types = request.GET.get('wagon_types', [])
        seat_types = request.GET.get('seat_types', [])
        user = request.user

        try:
            add_new_checker(
                user,
                departure_station_str,
                arrival_station_str,
                start_date_str,
                end_date_str,
                train_numbers,
                wagon_types,
                seat_types
            )
        except Exception as e:
            print(e)
    return render(request, 'uz_ticket_checker/checker.html')
