from django.shortcuts import render
from django.views.generic.list import ListView

from apps.uz_ticket_checker.models import Station
from apps.uz_ticket_checker.services.stations_update_service import run_all_stations_update


class StationsListView(ListView):
    model = Station
    template_name = 'uz_ticket_checker/stations.html'
    context_object_name = 'stations'
    paginate_by = 100

    def get_queryset(self):
        return Station.objects.filter(is_active=1).order_by('-weight')


def stations_update(request):
    # if request.user and not request.user.is_superuser:
    #     messages.error(request, 'Доступ до сторінки додавання нових продуктів мають лише суперюзери.')
    #     return redirect(reverse('products:products_list'))

    if request.method == 'GET':
        run_all_stations_update()
    return render(request, 'uz_ticket_checker/stations.html')
