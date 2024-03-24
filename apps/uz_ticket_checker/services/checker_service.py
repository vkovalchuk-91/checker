from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist

from apps.accounts.models import ParameterCategory, CheckerTask
from apps.uz_ticket_checker.models import SeatType, WagonType, TrainNumber, Station, TicketSearchParameter


def get_checkers_parameters_list(user):
    parameters = []
    user_checker_tasks_queryset = CheckerTask.objects.filter(user=user.pk).filter(
            task_params__param_type__param_category_name="UZ Ticket Checker").all()
    for item in user_checker_tasks_queryset:
        checker_parameter = {}
        parameter_id = item.task_params.pk
        ticket_search_parameter_obj = TicketSearchParameter.objects.get(pk=parameter_id)

        checker_parameter['departure_station'] = ticket_search_parameter_obj.departure_station
        checker_parameter['arrival_station'] = ticket_search_parameter_obj.arrival_station
        checker_parameter['start_date'] = ticket_search_parameter_obj.start_date
        checker_parameter['end_date'] = ticket_search_parameter_obj.end_date
        checker_parameter['train_numbers'] = (
            ', '.join(str(train_number.train_number) for train_number in
                      ticket_search_parameter_obj.train_number.all()))
        checker_parameter['wagon_types'] = (
            ', '.join(
                str(wagon_type.wagon_type) for wagon_type in ticket_search_parameter_obj.wagon_type.all()))
        checker_parameter['seat_types'] = (
            ', '.join(str(seat_type.seat_type) for seat_type in ticket_search_parameter_obj.seat_type.all()))
        checker_parameter['update_period'] = item.update_period
        checker_parameter['last_run_at'] = item.last_run_at
        checker_parameter['is_active'] = item.is_active
        checker_parameter['checker_id'] = item.pk
        parameters.append(checker_parameter)
    return parameters


def add_new_checker(
        user,
        departure_station_str,
        arrival_station_str,
        start_date_str,
        end_date_str,
        train_numbers,
        wagon_types,
        seat_types
):
    existing_departure_station = Station.objects.filter(express_3_id=departure_station_str).first()
    if not existing_departure_station:
        return None

    existing_arrival_station = Station.objects.filter(express_3_id=arrival_station_str).first()
    if not existing_arrival_station:
        return None

    try:
        existing_start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        existing_end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    except ValueError as e:
        print(e)
        return None

    if seat_types:
        seat_types = seat_types.split(",")
        for seat_type in seat_types:
            if not SeatType.objects.filter(seat_type=seat_type).exists():
                return None
    seat_types_obj = SeatType.objects.filter(seat_type=seat_types)

    if wagon_types:
        wagon_types = wagon_types.split(",")
        for wagon_type in wagon_types:
            if not WagonType.objects.filter(wagon_type=wagon_type).exists():
                return None
    wagon_types_obj = WagonType.objects.filter(wagon_type__in=wagon_types)

    if train_numbers:
        train_numbers = train_numbers.split(",")
        for train_number in train_numbers:
            if not TrainNumber.objects.filter(train_number=train_number).exists():
                new_train_number = TrainNumber(train_number=train_number)
                new_train_number.save()
    train_numbers_obj = TrainNumber.objects.filter(train_number__in=train_numbers)

    existing_param_category = ParameterCategory.objects.filter(param_category_name="UZ Ticket Checker").first()
    if existing_param_category:
        param_category = existing_param_category
    else:
        new_param_category = ParameterCategory(param_category_name="UZ Ticket Checker")
        new_param_category.save()
        param_category = new_param_category

    ticket_search_parameter_data = {
        "param_type": param_category,
        "departure_station": existing_departure_station,
        "arrival_station": existing_arrival_station,
        "start_date": existing_start_date,
        "end_date": existing_end_date,
    }

    ticket_search_parameter_obj = None
    try:
        ticket_search_parameter_objs = TicketSearchParameter.objects.filter(**ticket_search_parameter_data)
        ticket_search_parameter_obj_is_exist = False
        for item in ticket_search_parameter_objs:
            existing_train_numbers_obj = item.train_number.all()  # Отримуємо всі номера поїздів перевіряємого існуючого ticket_search_parameter
            existing_wagon_types_obj = item.wagon_type.all()  # Отримуємо всі типи вагонів перевіряємого існуючого ticket_search_parameter
            existing_seat_types_obj = item.seat_type.all()  # Отримуємо всі типи місць перевіряємого існуючого ticket_search_parameter
            if set(existing_train_numbers_obj) == set(train_numbers_obj) and set(existing_wagon_types_obj) == set(
                    wagon_types_obj) and set(existing_seat_types_obj) == set(seat_types_obj):
                ticket_search_parameter_obj = item
                ticket_search_parameter_obj_is_exist = True
                break  # порівнюємо їх всіх, якщо є повне співпадіння значить такий обєкт вже існує й беремо його
        if not ticket_search_parameter_obj_is_exist:  # створюємо новий обєкт з лише унікальним набором номерів поїздів, типів вагонів, типів місць
            ticket_search_parameter_obj = create_new_ticket_search_parameter_obj(
                existing_arrival_station, existing_departure_station,
                existing_end_date, existing_start_date, param_category,
                seat_types_obj, train_numbers_obj, wagon_types_obj)
    except ObjectDoesNotExist:  # створюємо новий обєкт з повністю унікальним ticket_search_parameter
        ticket_search_parameter_obj = create_new_ticket_search_parameter_obj(
            existing_arrival_station, existing_departure_station,
            existing_end_date, existing_start_date, param_category,
            seat_types_obj, train_numbers_obj, wagon_types_obj)

    existing_task = CheckerTask.objects.filter(user=user.pk).filter(task_params=ticket_search_parameter_obj).first()
    if existing_task is None:
        CheckerTask.objects.create(
            is_active=True,
            user=user,
            update_period=5,
            task_params=ticket_search_parameter_obj
        )


def create_new_ticket_search_parameter_obj(existing_arrival_station, existing_departure_station, existing_end_date,
                                           existing_start_date,
                                           param_category, seat_types_obj,
                                           train_numbers_obj, wagon_types_obj):
    ticket_search_parameter_obj = TicketSearchParameter.objects.create(
        param_type=param_category,
        departure_station=existing_departure_station,
        arrival_station=existing_arrival_station,
        start_date=existing_start_date,
        end_date=existing_end_date
    )
    ticket_search_parameter_obj.train_number.set(train_numbers_obj)
    ticket_search_parameter_obj.wagon_type.set(wagon_types_obj)
    ticket_search_parameter_obj.seat_type.set(seat_types_obj)
    return ticket_search_parameter_obj
