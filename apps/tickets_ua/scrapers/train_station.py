import json
import logging

import requests

from apps.tickets_ua.parsers.train_station import TrainStationParser
from apps.tickets_ua.scrapers.transport import _TransportScraper

logger = logging.getLogger('django')


class TrainStationScraper(_TransportScraper):
    SEARCH_URL = 'https://tickets.ua/complete/railway'

    parser_class = TrainStationParser

    def __init__(self, data: str):
        self.data = data

    @property
    def scrapy_items(self):
        try:
            data = {
                'filter': self.data,
                'type': 'ukraine',
                'parent': 'undefined',
            }
            response = requests.post(self.SEARCH_URL, headers=self._HEADERS, data=data)
            response.raise_for_status()

            json_data = json.loads(response.text)
            if not json_data:
                return []

            parser = self.parser_class(data=json_data)
            stations = parser.result_items
            return stations
        except (requests.RequestException, json.decoder.JSONDecodeError, ValueError, TypeError, KeyError) as e:
            logger.warning(f"Empty result of scraping trains stations: {self.data}: {e}")
            return []
