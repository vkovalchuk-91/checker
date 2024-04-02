import json
import logging
from datetime import datetime

import requests

from apps.tickets_ua.models import Station
from apps.tickets_ua.parsers.bus import BusParser
from apps.tickets_ua.scrapers.transport import _TransportScraper

logger = logging.getLogger('django')


class BusScraper(_TransportScraper):
    MAIN_URL = 'https://bus.tickets.ua'
    SEARCH_URL = 'https://bus.tickets.ua/api/bus/search'
    RESULT_URL = 'https://bus.tickets.ua/api/bus/result'

    BUS_HEADERS = {
        'authority': 'bus.tickets.ua',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6,zh-TW;q=0.5,zh-CN;q=0.4,zh;q=0.3',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        # 'cookie': 'history_token=65ec825a4f978; _gid=GA1.2.1194441803.1709998688; _gcl_au=1.1.1898267651.1709998692; user_accepts_cookies=1; _hjSessionUser_1384942=eyJpZCI6IjMzOGFhODgyLTIxNWMtNWZhMC04NTk1LTg5OWMyM2RmMDU4MiIsImNyZWF0ZWQiOjE3MDk5OTg2OTQ3MDYsImV4aXN0aW5nIjp0cnVlfQ==; __zlcmid=1KhmYY1mFyddu0D; _hjSessionUser_1404726=eyJpZCI6IjEzNGExNTAxLTE2M2MtNWU1ZS1iMmZmLTQ1YmYxNThjZGVhYyIsImNyZWF0ZWQiOjE3MDk5OTg4ODU3MzksImV4aXN0aW5nIjp0cnVlfQ==; _clck=k7s58u%7C2%7Cfjy%7C0%7C1529; _hjSessionUser_1404731=eyJpZCI6IjU3MGMyN2MxLTMwZDEtNWM3OS1hYzY4LTYwNWEzZDI0YWFjNCIsImNyZWF0ZWQiOjE3MTAwMTczNDcwODIsImV4aXN0aW5nIjp0cnVlfQ==; jsession_tua=lq420kict5idcebj1jc6rpmahj; extended_user_token=1003714250; featured=a1b962f6314; booking_countdown=0; _hjSession_1384942=eyJpZCI6ImRkMmY5Y2MzLWVjNzgtNGY4NS1iOWFkLWRkZjE1MzY3ODRjMCIsImMiOjE3MTAwOTMyNzY0NTEsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; bus_search_params=from_name%3D%25D0%259A%25D0%25B8%25D1%2597%25D0%25B2%26to_name%3D%25D0%259B%25D1%258C%25D0%25B2%25D1%2596%25D0%25B2%26from_code%3Dkiev%26to_code%3Dlvov%26departure_date%3D19.03.2024%26depth%3D1%26with_transfer%3D1%26adults%3D1%26children%3D0; _clsk=1eb5oi9%7C1710095666476%7C10%7C1%7Cp.clarity.ms%2Fcollect; _ga_MHZEN4Q0P4=GS1.1.1710093132.9.1.1710095679.60.0.0; _ga=GA1.2.316140365.1709998688; booking-checkbox=false',
        'origin': 'https://bus.tickets.ua',
        'pragma': 'no-cache',
        'referer': 'https://bus.tickets.ua/',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'withcredentials': 'true',
        'x-api-version': 'v1',
        'x-requested-with': 'XMLHttpRequest',
    }

    parser_class = BusParser

    def __init__(self, from_station: Station, to_station: Station, date_at: datetime.date, time_at: datetime.time):
        self.from_station = from_station
        self.to_station = to_station
        self.date_at = date_at
        self.time_at = time_at

    @property
    def scraper_items(self):
        session = requests.Session()
        try:
            response = session.get(self.MAIN_URL)
            response.raise_for_status()
            csrf_token = self._get_token(response.text)

            if not csrf_token:
                raise ValueError

            headers = {**self.BUS_HEADERS, **{'x-csrf-token': csrf_token, }}

            json_data = {
                'departure': self.from_station,
                'arrival': self.to_station,
                'departureDate': self.date_at.strftime(self._DATE_FORMAT),
                'adults': '1',
                'children': '0',
            }

            response = requests.post(self.SEARCH_URL, headers=headers, json=json_data)
            response.raise_for_status()
            json_session_data = json.loads(response.text)

            session_id = None
            if json_session_data.get('success'):
                session_id = json_session_data['result']['sessionId']

            if not session_id:
                raise ValueError

            json_data['sessionId'] = session_id
            json_data['currency'] = 'UAH'
            json_data['filters'] = {'trip': 'direct'}

            response = requests.post(self.RESULT_URL, headers=headers, json=json_data)
            response.raise_for_status()
            json_data = json.loads(response.text)

            buses = []
            if json_data.get('success'):
                parser = self.parser_class(data=json_data['result'])
                buses = parser.result_items

            return [bus for bus in buses if bus.date_at.time() >= self.time_at]
        except (requests.RequestException, json.decoder.JSONDecodeError, ValueError, TypeError, KeyError):
            logger.error(f"Invalid scraping buses [{self.from_station}->{self.to_station} at {self.date_at}]")
            return []
        finally:
            session.close()
