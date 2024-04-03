from datetime import datetime

from apps.tickets_ua.enums.seat import SeatType
from apps.tickets_ua.parsers.transport import _TransportParser


class TrainParser(_TransportParser):
    def __init__(self, data):
        self.data = data

    @property
    def result_items(self):
        train_items = self.data['trains']

        train_instances = []
        for item_item in train_items:
            train_instance = self._parse_instance(item_item)
            if train_instance:
                train_instances.append(train_instance)

        return train_instances

    def _parse_instance(self, json_data: dict):
        seats = SeatType.find_by_value(json_data['seats'])

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
