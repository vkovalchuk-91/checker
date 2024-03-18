import json


class CountSearchParser:

    def __init__(self, data):
        self.data = data

    @property
    def result_items(self):
        return self.data['byPathQuerySection']['filteredProductsCount']
