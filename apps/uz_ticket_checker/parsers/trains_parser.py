import requests
from loguru import logger

from apps.common.constants import SEAT_TYPES


def get_current_search_tickets(departure_station_code, arrival_station_code, departure_date):
    request_body = {
        'language': 'uk',
        'supplier': 'uz_train',
        'transactionId': '3835b4beef23',
        'sourceType': 'FRONTEND',
        'arrivalCode': arrival_station_code,
        'departureCode': departure_station_code,
        'departureDate': departure_date,
    }
    response_search = requests.post(
        'https://de-prod-lb.cashalot.in.ua/rest/supplier/search',
        json=request_body)

    current_search_tickets = []
    search_direction = ""
    try:
        if 'errorCode' in response_search.json() and response_search.json().get('errorCode') == 80:
            current_search_tickets = "no_trains_error"
            search_direction = "На даний момент на вказані дати відсутні квитки на потяги між вказаними станціями"
            return current_search_tickets, search_direction
        if 'errorCode' in response_search.json() and response_search.json().get('errorCode') == 1002:
            current_search_tickets = "proizd_ua_service_error"
            search_direction = "Вибачте, сервіс тимчасово недоступний. Спробуйте пізніше."
            return current_search_tickets, search_direction

        search_direction = \
            f"{response_search.json()['departureStation']['name']} - {response_search.json()['arrivalStation']['name']}"
        for trip in response_search.json()['trips']:
            for leg in trip['legs']:
                departure_date = leg['departureStation']['departureDate']
                departure_time = leg['departureStation']['departureTime']
                arrival_date = leg['arrivalStation']['arrivalDate']
                arrival_time = leg['arrivalStation']['arrivalTime']
                train_category = leg['transInfo']['categoryName']
                train_number = leg['transInfo']['number']
                train_name = \
                    f"{leg['transInfo']['departureStation']['name']} - {leg['transInfo']['arrivalStation']['name']}"
                wagon_details = get_wagon_type_details(
                    departure_station_code,
                    arrival_station_code,
                    departure_date,
                    train_number
                )
                if wagon_details is None:
                    current_search_tickets = "proizd_ua_price_details_error"
                    search_direction = "Вибачте, сервіс тимчасово недоступний (помилка отримання деталей цін). Спробуйте пізніше."
                    return current_search_tickets, search_direction

                current_search_tickets.append({
                    'from_station': departure_station_code,
                    'to_station': arrival_station_code,
                    'departure_date': departure_date,
                    'arrival_date': arrival_date,
                    'departure_time': departure_time,
                    'arrival_time': arrival_time,
                    'train_category': train_category,
                    'train_number': train_number,
                    'train_name': train_name,
                    'wagon_details': wagon_details,
                    'rowspan': len(wagon_details),
                })
    except Exception as e:
        logger.error(request_body)
        logger.error(response_search.json())
        logger.error(e)
    return current_search_tickets, search_direction


def get_wagon_type_details(departure_station_code, arrival_station_code, departure_date, train_number):
    request_body = {
        'language': 'uk',
        'supplier': 'uz_train',
        'transactionId': '3835b4beef23',
        'sourceType': 'FRONTEND',
        'departureCode': departure_station_code,
        'arrivalCode': arrival_station_code,
        'departureDate': departure_date,
        'transNumber': train_number,
    }

    response_details = requests.post(
        'https://de-prod-lb.cashalot.in.ua/rest/prices',
        json=request_body
    )

    details = []
    try:
        for wagon_type in response_details.json()['wagonTypes']:
            wagon_type_name = wagon_type['name']
            for wagon_class in wagon_type['classes']:
                wagon_class_name = ""
                if 'name' in wagon_class:
                    wagon_class_name = f" {wagon_class['name']}"

                min_price = wagon_class['minPrice']
                available_seats = wagon_class['availableSeats']
                seat_types = wagon_class['seatsDetails']
                seat_types_str = ""
                for seat_type, number in seat_types.items():
                    for SEAT_TYPE in SEAT_TYPES:
                        if SEAT_TYPE['seat_type'] == seat_type and number != 0:
                            seat_types_str += f"{SEAT_TYPE['seat_type_name']} - {number}\n"
                details.append({
                    'wagon_type': f"{wagon_type_name}{wagon_class_name}",
                    'min_price': min_price,
                    'available_seats': available_seats,
                    'seat_types': seat_types_str
                })
    except Exception as e:
        logger.error(request_body)
        logger.error(response_details.json())
        logger.error(e)
        details = None
    return details


def get_checker_matches_by_train_number(checker_matches_info, current_date, train_number, train_start_station,
                                        train_finish_station, train_departure_station_time):
    request_body = {
        'language': 'uk',
        'supplier': 'uz_train',
        'transactionId': '3835b4beef23',
        'sourceType': 'FRONTEND',
        'departureCode': checker_matches_info['departure_station'],
        'arrivalCode': checker_matches_info['arrival_station'],
        'departureDate': current_date.strftime('%Y-%m-%d'),
        'transNumber': train_number,
    }
    response_details = requests.post(
        'https://de-prod-lb.cashalot.in.ua/rest/prices',
        json=request_body
    )

    checker_matches = []
    wagon_types = []
    try:
        checker_matches.append({
            'departure_station': response_details.json()['departureCode'],
            'arrival_station': response_details.json()['arrivalCode'],
            'departure_date': response_details.json()['departureDate'],
            'train_number': response_details.json()['transNumber'],
            'train_start_station': train_start_station,
            'train_finish_station': train_finish_station,
            'train_departure_station_time': train_departure_station_time,
            'wagon_types': wagon_types,
        })
        for wagon_type in response_details.json()['wagonTypes']:
            wagon_type_name = wagon_type['name']
            for wagon_class in wagon_type['classes']:
                wagon_class_name = ""
                if 'name' in wagon_class:
                    wagon_class_name = f" {wagon_class['name']}"

                is_wagon_type_valid = True
                if len(checker_matches_info['wagon_type']) != 0:
                    response_wagon_type = f"{wagon_type_name}{wagon_class_name}"
                    if response_wagon_type not in checker_matches_info['wagon_type']:
                        is_wagon_type_valid = False

                if is_wagon_type_valid and checker_matches_info['seat_type'] is not None:
                    seats = []
                    wagon_types.append({
                        'wagon_type': f"{wagon_type_name}{wagon_class_name}",
                        'min_price': wagon_class['minPrice'],
                        'available_seats': wagon_class['availableSeats'],
                        'seats': seats,
                    })
                    response_seats = wagon_class['seatsDetails']

                    for response_seat, seats_qty in response_seats.items():
                        is_seats_not_defined = len(checker_matches_info['seat_type']) == 0
                        is_seat_in_search_list = response_seat in checker_matches_info['seat_type']
                        if seats_qty != 0 and (is_seats_not_defined or is_seat_in_search_list):
                            seats.append({
                                'seat_type': response_seat,
                                'available_seats': seats_qty,
                            })
    except Exception as e:
        logger.error(request_body)
        logger.error(response_details.json())
        logger.error(e)
    return checker_matches


def get_all_train_numbers_by_date(departure_station_code, arrival_station_code, departure_date):
    request_body = {
        'language': 'uk',
        'supplier': 'uz_train',
        'transactionId': '3835b4beef23',
        'sourceType': 'FRONTEND',
        'arrivalCode': arrival_station_code,
        'departureCode': departure_station_code,
        'departureDate': departure_date,
    }
    response_search = requests.post(
        'https://de-prod-lb.cashalot.in.ua/rest/supplier/search',
        json=request_body
    )
    train_numbers_info = {}
    try:
        for trip in response_search.json()['trips']:
            for leg in trip['legs']:
                train_number = leg['transInfo']['number']
                train_start_station = leg['transInfo']['departureStation']['name']
                train_finish_station = leg['transInfo']['arrivalStation']['name']
                train_departure_station_time = leg['departureStation']['departureTime'][:5]
                train_numbers_info[train_number] = {
                    'train_start_station': train_start_station,
                    'train_finish_station': train_finish_station,
                    'train_departure_station_time': train_departure_station_time
                }
    except Exception as e:
        logger.error(request_body)
        logger.error(response_search.json())
        logger.error(e)
    return train_numbers_info
