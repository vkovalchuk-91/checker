from django.shortcuts import render
from django.views.generic.list import ListView

from apps.common.constants import UKRAINIAN_ALPHABET
from apps.uz_ticket_checker.models import Station


class StationsListView(ListView):
    model = Station
    template_name = 'uz_ticket_checker/stations.html'
    context_object_name = 'stations'
    paginate_by = 300

    def get_queryset(self):
        return Station.objects.filter(is_active=1).order_by('-weight')


def stations_update(request, run_stations_scraping_task=None):
    # if request.user and not request.user.is_superuser:
    #     messages.error(request, 'Доступ до сторінки додавання нових продуктів мають лише суперюзери.')
    #     return redirect(reverse('products:products_list'))

    if request.method == 'GET':
        for letter in UKRAINIAN_ALPHABET:
            run_stations_scraping_task.delay(phrase=letter)
    return render(request, 'uz_ticket_checker/stations.html')
