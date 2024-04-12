from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from loguru import logger

from apps.accounts.utils.telegram import has_user_related_telegram_id
from apps.common.constants import STATIONS, WAGON_TYPES, SEAT_TYPES
from apps.task_manager.models import CheckerTask, SessionTaskManager
from apps.tbot.handlers.send_uz_tickets_matches import send_tickets
from apps.uz_ticket_checker.models import TicketSearchParameter
from apps.uz_ticket_checker.services.checker_service import add_new_checker, get_checkers_parameters_list_for_frontend, \
    get_direction_info_str, get_checker_matches, get_checker_matches_info_dict


def checkers_view(request):
    if request.user and not request.user.is_authenticated:
        messages.info(request, 'Доступ до сторінки списку чекерів мають лише авторизовані користувачі.')
        return redirect(reverse('uz_ticket_checker_app:search_results'))
    if not has_user_related_telegram_id(request):
        return redirect(reverse('telegram'))

    context = {}
    user = request.user
    context['parameters'] = get_checkers_parameters_list_for_frontend(user)
    context['stations'] = STATIONS
    context['wagon_types'] = WAGON_TYPES
    context['seat_types'] = SEAT_TYPES

    if request.method == 'GET':
        context['from_station'] = int(request.GET.get('from_station', 2200001))
        context['to_station'] = int(request.GET.get('to_station', 2218000))
        if request.GET.get('train_number'):
            context['train_number'] = request.GET.get('train_number')
        if request.GET.get('wagon_type'):
            context['selected_wagon_types'] = request.GET.get('wagon_type')
        if request.GET.get('from_date'):
            from_date = request.GET.get('from_date')
            context['from_date'] = from_date
            context['to_date'] = request.GET.get('to_date', from_date)

    if request.method == 'POST':
        context['from_station'] = request.POST.get('from_station', 2200001)
        context['to_station'] = request.POST.get('to_station', 2218000)
        context['train_number'] = request.POST.get('to_station', 2218000)
        context['selected_wagon_types'] = []
        context['selected_seat_types'] = []
        if request.POST.get('from_date'):
            from_date = request.POST.get('from_date')
            context['from_date'] = from_date
            context['to_date'] = request.POST.get('to_date', from_date)

    SessionTaskManager(request)
    return render(request, 'uz_ticket_checker/checker.html', context)


def checker_add(request):
    if request.user and not request.user.is_authenticated:
        previous_page = request.META.get('HTTP_REFERER', '/')
        return HttpResponseRedirect(previous_page)

    user = request.user
    if not CheckerTask.objects.can_create_new_task(user.pk):
        messages.info(request, 'Кількість вільних для використання чекерів закінчилася.')
    elif request.method == 'POST':
        departure_station_str = request.POST.get('from_station')
        arrival_station_str = request.POST.get('to_station')
        trip_dates = request.POST.get('trip_dates').split(" - ")
        start_date_str = trip_dates[0]
        end_date_str = trip_dates[1]
        train_numbers = request.POST.get('train_numbers').split(",")
        wagon_types = request.POST.getlist('wagon_types')
        seat_types = request.POST.getlist('seat_types')

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
            SessionTaskManager(request)
        except Exception as e:
            logger.error(e)
    return redirect(reverse('uz_ticket_checker_app:checker'))


def checker_delete(request, pk):
    if request.user and not request.user.is_authenticated:
        previous_page = request.META.get('HTTP_REFERER', '/')
        return HttpResponseRedirect(previous_page)

    delete_object = get_object_or_404(CheckerTask, pk=pk)
    if request.method == 'GET':
        delete_object.is_delete = True
        delete_object.save()
        SessionTaskManager(request)
    return redirect(reverse('uz_ticket_checker_app:checker'))


def checker_change_is_active(request, pk):
    if request.user and not request.user.is_authenticated:
        previous_page = request.META.get('HTTP_REFERER', '/')
        return HttpResponseRedirect(previous_page)

    change_object = get_object_or_404(CheckerTask, pk=pk)
    if request.method == 'POST':
        is_active = change_object.is_active
        change_object.is_active = not is_active
        change_object.save()
    return redirect(reverse('uz_ticket_checker_app:checker'))


def checker_check(request):  # testing endpoint
    if request.user and not request.user.is_authenticated:
        previous_page = request.META.get('HTTP_REFERER', '/')
        return HttpResponseRedirect(previous_page)

    if request.method == 'GET':
        user = request.user
        user_checker_tasks_queryset = CheckerTask.objects.filter(user=user.pk).filter(
            task_param__param_type__param_category_name="UZ Ticket Checker", is_active=True,
            is_delete=False).all()
        for item in user_checker_tasks_queryset:
            parameter_id = item.task_param.pk
            ticket_search_parameter_obj = TicketSearchParameter.objects.get(pk=parameter_id)
            checker_matches_info = get_checker_matches_info_dict(ticket_search_parameter_obj)
            tickets_matches = get_checker_matches(checker_matches_info)
            direction_info = get_direction_info_str(ticket_search_parameter_obj)
            send_tickets(396264878, item.pk, direction_info, tickets_matches)

    return render(request, 'uz_ticket_checker/checker.html')
