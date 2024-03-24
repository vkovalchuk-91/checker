from datetime import datetime

from apps.accounts.models import ParameterCategory, CheckerTask
from apps.uz_ticket_checker.models import SeatType, WagonType, TrainNumber, Station, TicketSearchParameter


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
    TicketSearchParameter.objects.update_or_create(defaults=ticket_search_parameter_data)
    ticket_search_parameter_obj = TicketSearchParameter.objects.get(**ticket_search_parameter_data)
    ticket_search_parameter_obj.train_number.set(train_numbers_obj)
    ticket_search_parameter_obj.wagon_type.set(wagon_types_obj)
    ticket_search_parameter_obj.seat_type.set(seat_types_obj)

    check_task_data = {
        "is_active": True,
        "user": user,
        "update_period": 5,
        "task_params": ticket_search_parameter_obj,
    }

    CheckerTask.objects.update_or_create(defaults=check_task_data)
