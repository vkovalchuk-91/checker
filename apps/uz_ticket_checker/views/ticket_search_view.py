from django.contrib import messages
from django.shortcuts import render

from apps.uz_ticket_checker.services.trains_search_service import get_search_result_tickets


def search_results_view(request):
    # if request.user and not request.user.is_authenticated:
    #     messages.error(request, 'Доступ до сторінки додавання нових продуктів мають лише авторизовані користувачі.')
    #     return render(request, "ticket_search_page.html")

    context = {}
    if request.method == 'GET':
        from_station = request.GET.get('from_station')
        to_station = request.GET.get('to_station')
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date', from_date)

        try:
            search_results, search_summary = get_search_result_tickets(from_station, to_station, from_date, to_date)
            context = {'search_results': search_results, 'search_summary': search_summary}
        except Exception as e:
            pass

        # search_results, direction = get_current_search_tickets(
        #     '2200001', '2208099', '2024-03-26')

    return render(request, 'uz_ticket_checker/ticket_search_page.html', context)

