from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from apps.accounts.models import CheckerTask
from apps.accounts.utils.telegram import has_user_related_telegram_id
from apps.uz_ticket_checker.models import TicketSearchParameter
from apps.uz_ticket_checker.services.checker_service import add_new_checker, get_checkers_parameters_list
from apps.uz_ticket_checker.services.trains_search_service import get_checker_matches


def checkers_view(request):
    # if request.user and not request.user.is_authenticated:
    #     messages.error(request, 'Доступ до сторінки додавання нових продуктів мають лише авторизовані користувачі.')
    #     return render(request, "ticket_search_page.html")

    context = {}
    if request.method == 'GET':
        if not has_user_related_telegram_id(request):
            return redirect(reverse('telegram'))
        user = request.user
        context['parameters'] = get_checkers_parameters_list(user)

    return render(request, 'uz_ticket_checker/checker.html', context)


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
    return redirect(reverse('uz_ticket_checker_app:checker'))


def checker_delete(request, pk):
    # if request.user and not request.user.is_superuser:
    #     messages.error(request, 'Доступ до сторінки додавання нових продуктів мають лише суперюзери.')
    #     return redirect(reverse('products:products_list'))

    delete_object = get_object_or_404(CheckerTask, pk=pk)
    if request.method == 'GET':
        parameter_id = delete_object.task_params.pk
        ticket_search_parameter_obj = TicketSearchParameter.objects.get(pk=parameter_id)
        ticket_search_parameter_obj.train_number.clear()
        ticket_search_parameter_obj.wagon_type.clear()
        ticket_search_parameter_obj.seat_type.clear()
        ticket_search_parameter_obj.delete()
        delete_object.delete()
    return redirect(reverse('uz_ticket_checker_app:checker'))


def checker_change_is_active(request, pk):
    # if request.user and not request.user.is_superuser:
    #     messages.error(request, 'Доступ до сторінки додавання нових продуктів мають лише суперюзери.')
    #     return redirect(reverse('products:products_list'))

    change_object = get_object_or_404(CheckerTask, pk=pk)
    if request.method == 'POST':
        is_active = change_object.is_active
        change_object.is_active = not is_active
        change_object.save()
    return redirect(reverse('uz_ticket_checker_app:checker'))


def checker_check(request):
    # if request.user and not request.user.is_superuser:
    #     messages.error(request, 'Доступ до сторінки додавання нових продуктів мають лише суперюзери.')
    #     return redirect(reverse('products:products_list'))

    if request.method == 'GET':
        user = request.user
        user_checker_tasks_queryset = CheckerTask.objects.filter(user=user.pk).filter(
            task_params__param_type__param_category_name="UZ Ticket Checker").filter(is_active=True).all()
        for item in user_checker_tasks_queryset:
            parameter_id = item.task_params.pk
            ticket_search_parameter_obj = TicketSearchParameter.objects.get(pk=parameter_id)
            train_checker_info = {
                'departure_station': str(ticket_search_parameter_obj.departure_station.express_3_id),
                'arrival_station': str(ticket_search_parameter_obj.arrival_station.express_3_id),
                'start_date': ticket_search_parameter_obj.start_date.strftime("%Y-%m-%d"),
                'end_date': ticket_search_parameter_obj.end_date.strftime("%Y-%m-%d"),
                'train_number': list(
                    str(train_number.train_number) for train_number in ticket_search_parameter_obj.train_number.all()),
                'wagon_type': list(
                    str(wagon_type.wagon_type) for wagon_type in ticket_search_parameter_obj.wagon_type.all()),
                'seat_type': list(
                    str(seat_type.seat_type) for seat_type in ticket_search_parameter_obj.seat_type.all()),
            }
            tickets_matches = get_checker_matches(train_checker_info)
            print(1111111)
            for ticket in tickets_matches:
                print(ticket)

    return render(request, 'uz_ticket_checker/checker.html')
