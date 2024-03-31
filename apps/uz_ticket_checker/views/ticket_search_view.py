import json

from celery.result import AsyncResult
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render
from loguru import logger

from apps.uz_ticket_checker.services.trains_search_service import get_search_result_tickets
from apps.uz_ticket_checker.tasks import run_tickets_search_task


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
            dates_result, search_summary = get_search_result_tickets(from_station, to_station, from_date, to_date)
            context = {'dates_result': dates_result, 'search_summary': search_summary}
        except Exception as e:
            logger.debug(e)

        # search_results, direction = get_current_search_tickets(
        #     '2200001', '2208099', '2024-03-26')

    return render(request, 'uz_ticket_checker/ticket_search_page.html', context)


def execute_task(request):
    task_result = []
    if request.method == 'POST':
        from_station = request.POST.get('from_station')
        to_station = request.POST.get('to_station')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date', from_date)

        try:
            dates_result = run_tickets_search_task.delay(from_station=from_station, to_station=to_station, from_date=from_date, to_date=to_date)
            task_id = dates_result.id  # Отримуємо ідентифікатор завдання
            async_result = AsyncResult(task_id)
            task_result = async_result.get()  # Отримуємо результати завдання
        except Exception as e:
            logger.debug(e)
    return JsonResponse(json.dumps(task_result), safe=False)
