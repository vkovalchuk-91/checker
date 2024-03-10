from datetime import datetime

from apps.tickets_ua.parsers.transport import _TransportParser


class TrainParser(_TransportParser):
    def __init__(self, data):
        self.data = data

    @property
    def result_items(self):
        train_items = self.data['trains']

        trains = []
        for item in train_items:
            train = self._parse_transports(item)
            if train:
                trains.append(train)

        return trains

    def _parse_transports(self, json_data: dict):
        seats = self._parse_seats(json_data['seats'])

        number = r"{}".format(json_data['number'])
        name = r"{}".format(json_data['name'])
        travel_time_minutes = json_data['travelTime']['minutes']

        date_at = datetime.strptime(json_data['departure']['date'], '%Y-%m-%dT%H:%M:%S%z')

        return self.result_class(
            number=number,
            name=name,
            date_at=date_at,
            travel_time_minutes=travel_time_minutes,
            seats=seats,
        )

    def _parse_seats(self, json_seats: list[dict]):
        seats = []
        for json_seat in json_seats:
            type_value = json_seat['type']
            type_seat = self.get_seat_type_by_value(type_value)
            seat = self.seat_class(
                type=type_seat,
                available=int(json_seat['availableSeats']),
            )
            seats.append(seat)

        return seats
