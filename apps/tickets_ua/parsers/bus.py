import re
from datetime import datetime

from apps.tickets_ua.parsers.transport import _TransportParser


class BusParser(_TransportParser):

    def __init__(self, data):
        self.data = data

    @property
    def result_items(self):
        bus_items = self.data['items']

        buses = []
        for item in bus_items:
            train = self._parse_transports(item)
            if train:
                buses.append(train)

        return buses

    def _parse_transports(self, json_data: dict):
        seats = self._parse_seats(json_data['placesInfo'])
        if not seats:
            return

        number = r"{}".format(json_data['number'])
        name = number
        travel_time_minutes = json_data['travelInfo']['duration']['minutes']

        date_str = json_data['departure']["date"]["date"]
        time_str = json_data['departure']["time"]["date"]
        combined_datetime_str = f"{date_str[:11]}{time_str[11:]}"
        date_at = datetime.strptime(combined_datetime_str, '%Y-%m-%dT%H:%M:%S%z')

        return self.result_class(
            number=number,
            name=name,
            date_at=date_at,
            travel_time_minutes=travel_time_minutes,
            seats=seats,
        )

    def _parse_seats(self, json_seat: dict):
        available_str = json_seat['label']
        match = re.search(r'\b\d+\b', available_str)
        if match:
            return self.seat_class(
                type=self.get_seat_type_by_value(None),
                available=int(match.group()),
            )
