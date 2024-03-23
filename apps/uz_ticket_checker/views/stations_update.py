from django.shortcuts import render

from apps.uz_ticket_checker.services.stations_update_service import run_all_stations_update


def stations_update(request):
    # if request.user and not request.user.is_superuser:
    #     messages.error(request, 'Доступ до сторінки додавання нових продуктів мають лише суперюзери.')
    #     return redirect(reverse('products:products_list'))

    if request.method == 'GET':
        run_all_stations_update()
    return render(request, 'uz_ticket_checker/stations.html')
