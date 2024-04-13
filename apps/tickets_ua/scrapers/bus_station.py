import json
import logging

import requests

from apps.tickets_ua.parsers.bus_station import BusStationParser
from apps.tickets_ua.scrapers.transport import _TransportScraper

logger = logging.getLogger('django')


class BusStationScraper(_TransportScraper):
    SEARCH_URL = 'https://bus.tickets.ua/complete/bus'

    parser_class = BusStationParser

    def __init__(self, data: str):
        self.data = data

    @property
    def scrapy_items(self):
        try:
            data = {
                'filter': self.data,
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
            logger.error(f"Can't scraping or empty: {self.data}: {e}")
            return []
