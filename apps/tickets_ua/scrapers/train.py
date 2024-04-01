import json
import logging
from datetime import datetime

import requests

from apps.tickets_ua.parsers.train import TrainParser
from apps.tickets_ua.scrapers.transport import _TransportScraper

logger = logging.getLogger('django')


class TrainScraper(_TransportScraper):
    MAIN_URL = 'https://gd.tickets.ua/'
    SEARCH_URL = 'https://gd.tickets.ua/api/railway/trains'

    parser_class = TrainParser

    def __init__(self, from_station, to_station, date_at: datetime.date, time_at: datetime.time):
        self.from_station = from_station
        self.to_station = to_station
        self.date_at = date_at
        self.time_at = time_at

    @property
    def scrapy_items(self):
        session = requests.Session()
        try:
            response = session.get(self.MAIN_URL)
            response.raise_for_status()
            csrf_token = self._get_token(response.text)

            if not csrf_token:
                raise ValueError

            headers = {**self._HEADERS, **{'x-csrf-token': csrf_token, }}
            json_data = {
                'departure': self.from_station,
                'arrival': self.to_station,
                'date': self.date_at.strftime(self._DATE_FORMAT),
            }
            response = session.post(self.SEARCH_URL, headers=headers, json=json_data)
            response.raise_for_status()
            json_data = json.loads(response.text)

            trains = []
            if json_data.get('success'):
                parser = self.parser_class(data=json_data['result'])
                trains = parser.result_items

            return [train for train in trains if train.date_at.time() >= self.time_at]
        except (requests.RequestException, json.decoder.JSONDecodeError, ValueError, TypeError, KeyError) as e:
            logger.error(f"Invalid scraping trains [{self.from_station}->{self.to_station} at {self.date_at}]")
            return []
        finally:
            session.close()
