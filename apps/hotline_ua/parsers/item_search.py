from dataclasses import dataclass


@dataclass
class Item:
    code: int
    title: str
    url: str


class ItemSearchParser:
    result_class = Item

    def __init__(self, data):
        self.data = data

    @property
    def result_items(self):
        stations = []
        for item in self.data:
            station = self.result_class(
                code=item['id'],
                title=item['title'],
                url=item['url'],
            )
            stations.append(station)

        return stations
