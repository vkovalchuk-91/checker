import requests


def get_current_search_tickets(departure_station_code, arrival_station_code, departure_date):
    body_search = {
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
        json=body_search)
    current_search_tickets = []
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
            current_search_tickets.append({
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
    for wagon_type in response_details.json()['wagonTypes']:
        wagon_type_name = wagon_type['name']
        for wagon_class in wagon_type['classes']:
            wagon_class_name = ""
            if 'name' in wagon_class:
                wagon_class_name = f" {wagon_class['name']}"

            min_price = wagon_class['minPrice']
            available_seats = wagon_class['availableSeats']
            seat_types = wagon_class['seatsDetails']

            details.append({
                'wagon_type': f"{wagon_type_name}{wagon_class_name}",
                'min_price': min_price,
                'available_seats': available_seats,
                'seat_types': seat_types
            })
    return details


def get_checker_matches_by_train_number(train_checker_info, current_date, train_number):
    request_body = {
        'language': 'uk',
        'supplier': 'uz_train',
        'transactionId': '3835b4beef23',
        'sourceType': 'FRONTEND',
        'departureCode': train_checker_info['departure_station'],
        'arrivalCode': train_checker_info['arrival_station'],
        'departureDate': current_date.strftime('%Y-%m-%d'),
        'transNumber': train_number,
    }
    response_details = requests.post(
        'https://de-prod-lb.cashalot.in.ua/rest/prices',
        json=request_body
    )

    checker_matches = []

    wagon_types = []
    checker_matches.append({
        'departure_station': response_details.json()['departureCode'],
        'arrival_station': response_details.json()['arrivalCode'],
        'departure_date': response_details.json()['departureDate'],
        'train_number': response_details.json()['transNumber'],
        'wagon_types': wagon_types,
    })
    for wagon_type in response_details.json()['wagonTypes']:
        wagon_type_name = wagon_type['name']
        for wagon_class in wagon_type['classes']:
            wagon_class_name = ""
            if 'name' in wagon_class:
                wagon_class_name = f" {wagon_class['name']}"

            is_wagon_type_valid = True
            # if train_checker_info['wagon_type'] is not None:
            if len(train_checker_info['wagon_type']) != 0:
                response_wagon_type = f"{wagon_type_name}{wagon_class_name}"
                if response_wagon_type not in train_checker_info['wagon_type']:
                    is_wagon_type_valid = False

            if is_wagon_type_valid and train_checker_info['seat_type'] is not None:
                seats = []
                wagon_types.append({
                    'wagon_type': f"{wagon_type_name}{wagon_class_name}",
                    'min_price': wagon_class['minPrice'],
                    'available_seats': wagon_class['availableSeats'],
                    'seats': seats,
                })
                response_seats = wagon_class['seatsDetails']

                for response_seat, seats_qty in response_seats.items():
                    is_seats_not_defined = len(train_checker_info['seat_type']) == 0
                    is_seat_in_search_list = response_seat in train_checker_info['seat_type']
                    if seats_qty != 0 and (is_seats_not_defined or is_seat_in_search_list):
                        seats.append({
                            'seat_type': response_seat,
                            'available_seats': seats_qty,
                        })
    print(checker_matches)
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
    train_numbers = []
    print(response_search.json())
    for trip in response_search.json()['trips']:
        for leg in trip['legs']:
            train_number = leg['transInfo']['number']
            train_numbers.append(train_number)
    return train_numbers
