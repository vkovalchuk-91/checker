from dataclasses import dataclass

from apps.tickets_ua.parsers.transport import _TransportParser


@dataclass
class BusStation:
    code: str
    name: str


class BusStationParser(_TransportParser):
    result_class = BusStation

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
