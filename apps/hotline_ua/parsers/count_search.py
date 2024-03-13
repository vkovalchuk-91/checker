import json


class CountSearchParser:

    def __init__(self, data):
        self.data = data

    @property
    def result_items(self):
        json_data = json.loads(self.data)
        count = json_data['byPathQuerySection']['filteredProductsCount']
        i = count['_id']
        return i
