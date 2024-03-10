from dataclasses import dataclass

from apps.tickets_ua.parsers.transport import _TransportParser


@dataclass
class TrainStation:
    code: int
    name: str


class TrainStationParser(_TransportParser):
    result_class = TrainStation

    def __init__(self, data):
        self.data = data

    @property
    def result_items(self):
        stations = []
        for item in self.data:
            station = self.result_class(
                code=item['code'],
                name=item['name'],
            )
            stations.append(station)

        return stations
