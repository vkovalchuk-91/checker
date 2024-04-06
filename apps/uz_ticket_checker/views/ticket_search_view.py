import json

from celery.result import AsyncResult
from django.http import JsonResponse
from django.shortcuts import render
from loguru import logger

from apps.common.constants import STATIONS
from apps.uz_ticket_checker.tasks import run_tickets_search_task


def search_ticket_view(request):
    context = {}
    if request.method == 'GET':
        context['stations'] = STATIONS

    return render(request, 'uz_ticket_checker/ticket_search_page.html', context)


def get_search_results(request):
    task_result = []
    if request.method == 'POST':
        from_station = request.POST.get('from_station')
        to_station = request.POST.get('to_station')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date', from_date)

        try:
            final_result = run_tickets_search_task.delay(from_station=from_station, to_station=to_station,
                                                         from_date=from_date, to_date=to_date)
            task_id = final_result.id
            async_result = AsyncResult(task_id)
            task_result = async_result.get()
        except Exception as e:
            logger.debug(e)
    return JsonResponse(json.dumps(task_result), safe=False)
