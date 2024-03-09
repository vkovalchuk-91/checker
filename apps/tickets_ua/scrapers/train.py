import json
import logging
import re
from dataclasses import dataclass
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from apps.tickets_ua.enums.seat_type import SeatType

logger = logging.getLogger('django')


@dataclass
class Seat:
    type: SeatType
    available: int


@dataclass
class Train:
    number: str
    name: str
    travel_time_minutes: int
    date_at: datetime
    seats: list[Seat]


MAIN_URL = 'https://gd.tickets.ua/'
TRAIN_SEARCH_URL = 'https://gd.tickets.ua/api/railway/trains'

HEADERS = {
    'authority': 'gd.tickets.ua',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'uk-UA,uk;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    # 'cookie': 'jsession_tua=7h7rcd96t0irb7ngf0s4786ji2; extended_user_token=0903665097; featured=a1b962f6314; history_token=65ec84b389779; _gid=GA1.2.1921264314.1709999289; _gcl_au=1.1.1890335134.1709999289; booking-checkbox=true; _gat=1; _clck=esderj%7C2%7Cfjx%7C0%7C1529; _hjSessionUser_1384942=eyJpZCI6Ijg0YmMyZTVjLWViMjctNTU3NC1hYzk2LWU2OGRiNzg2YmIyMyIsImNyZWF0ZWQiOjE3MDk5OTkyOTMzMDIsImV4aXN0aW5nIjpmYWxzZX0=; _hjSession_1384942=eyJpZCI6ImU5MGI2MjY1LTY1ODQtNDgyNi1hY2NmLWU4ODJlNTRlNTY5NCIsImMiOjE3MDk5OTkyOTMzMDQsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=; _clsk=1211k5d%7C1709999293717%7C1%7C1%7Cp.clarity.ms%2Fcollect; __zlcmid=1KhmYY4pYXdMi3x; _ga_MHZEN4Q0P4=GS1.1.1709999292.1.0.1709999311.41.0.0; _ga=GA1.2.1877075567.1709999289',
    'origin': 'https://gd.tickets.ua',
    'pragma': 'no-cache',
    'referer': 'https://gd.tickets.ua/search/result/f/2200001-2218000/15.03.2024',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'withcredentials': 'true',
    'x-api-version': 'v1',
    # 'x-csrf-token': 'LPvuoP88sSmbH3ISvxCi3Wd4SQfImYJS',
    'x-requested-with': 'XMLHttpRequest',
}

smpl_data = {
    'departure': '2200001',
    'arrival': '2218000',
    'date': '15.03.2024',
    'is_roundtrip': False,
    'session': '08psx76irp7i',

}

CAPTCHA = '03AFcWeA6leCyyMB_59nAzhOCNCDPtulttbDdMVDlFryDnbRB2a6S6my3ej8xHGYm0I5WkQdJHmayWaRfsZmsxwSZ6RMXSyoGVNUbXNp1M46DEMlASAPCI4fR6JK3yebqBx5QcucjnAfb3XiKmhZVE__r5QiJvnpIFsyJi4rqRJg2jCh6cdOONazmTFkHVpta4vyrDpQRqAqKTNyUU-hFeVcTERnER7Ps123j_ypYgTkBfSIwtw9VKbEhsgY7AOEduXwumgNz8QX0PNZ_v6sCGOTkL3meiE9atA9WlXLJqIEVqUIOPy21zREeaiPGvi5gI9_2fa6zme_CStaC5YOgoVq_it8kCY89af9eJnxIJDg8IV_Nxry0H60DzxWa0fQPgl02VSfF5UVR2Uh8i1vtOhQibH-jDccb-bfRKYZJp9voEN0fX2KYhqCB0SwqM85kDlqBquB1wX6CNAne5HKLl7IUWlhjhSFhyWGTNStuFnX3XcFQO7aShPS9Y9tXGSBetllsWmAisVZBfH-jLMvkcuPiUXWGMdz4v-24M204mOLZUP4YhLDf0FQGerD_2iYCGfqSAiCA5KFdBW1SuH8vUabnvZqt8wF6NeGoaru3rw_9O9Fh6av-ePyNWzNt2OUl3tVKQ1_OcJJkYLyk-o-6TcWE65FBsbwS-rsCBT3B23FyrPjv8TCpaLJo'

DATE_FORMAT = '%d.%m.%Y'
TIME_FORMAT = '%H:%M'

cookies = {
    'jsession_tua': '7h7rcd96t0irb7ngf0s4786ji2',
    'extended_user_token': '0903665097',
    'featured': 'a1b962f6314',
    'history_token': '65ec84b389779',
    '_gid': 'GA1.2.1921264314.1709999289',
    '_gcl_au': '1.1.1890335134.1709999289',
    'booking-checkbox': 'true',
    '_gat': '1',
    '_clck': 'esderj%7C2%7Cfjx%7C0%7C1529',
    '_hjSessionUser_1384942': 'eyJpZCI6Ijg0YmMyZTVjLWViMjctNTU3NC1hYzk2LWU2OGRiNzg2YmIyMyIsImNyZWF0ZWQiOjE3MDk5OTkyOTMzMDIsImV4aXN0aW5nIjpmYWxzZX0=',
    '_hjSession_1384942': 'eyJpZCI6ImU5MGI2MjY1LTY1ODQtNDgyNi1hY2NmLWU4ODJlNTRlNTY5NCIsImMiOjE3MDk5OTkyOTMzMDQsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=',
    '_clsk': '1211k5d%7C1709999293717%7C1%7C1%7Cp.clarity.ms%2Fcollect',
    '__zlcmid': '1KhmYY4pYXdMi3x',
    '_ga_MHZEN4Q0P4': 'GS1.1.1709999292.1.0.1709999311.41.0.0',
    '_ga': 'GA1.2.1877075567.1709999289',
}


def scrapy(from_station: int, to_station: int, date_at: datetime.date, time_at: datetime.time):
    logger.info(f'Task scrapping trains {from_station}->{to_station} at {date_at}')
    session = requests.Session()
    try:
        response = session.get(MAIN_URL)
        response.raise_for_status()
        csrf_token = get_token(response.text)

        if not csrf_token:
            raise ValueError

        HEADERS['x-csrf-token'] = csrf_token
        json_data = {
            'departure': from_station,
            'arrival': to_station,
            'date': date_at.strftime(DATE_FORMAT),
        }
        response = session.post(TRAIN_SEARCH_URL, headers=HEADERS, json=json_data)
        response.raise_for_status()
        json_response_text = json.loads(response.text)

        trains = []
        if json_response_text.get('success'):
            trains = scrapy_trains(json_response_text['result'])

        return [train for train in trains if train.date_at.time() >= time_at]
    except (requests.RequestException, ValueError, TypeError) as e:
        logger.error(f"Invalid scraping trains [{from_station}->{to_station} at {date_at}]")
        raise ValueError(f"Invalid scraping trains.")
    finally:
        logger.info(f'Task scrapping trains {from_station}->{to_station} at {date_at} finish')
        session.close()


def get_token(response_text):
    soup = BeautifulSoup(response_text, 'html.parser')
    script_content = soup.find('script', string=re.compile(r'"csrfToken"'))

    if script_content:
        match = re.search(r'"csrfToken":"([^"]+)"', script_content.string)
        if match:
            return match.group(1)
    return None


def scrapy_trains(json_data: dict) -> list[Train]:
    train_items = json_data['trains']

    trains = []
    for item in train_items:
        train = parse_train(item)
        if train:
            trains.append(train)

    return trains


def parse_train(json_data: dict) -> Train:
    seats = parse_seats(json_data['seats'])

    number = r"{}".format(json_data['number'])
    name = r"{}".format(json_data['name'])
    travel_time_minutes = json_data['travelTime']['minutes']

    date_at = datetime.strptime(json_data['departure']['date'], '%Y-%m-%dT%H:%M:%S%z')

    return Train(
        number=number,
        name=name,
        date_at=date_at,
        travel_time_minutes=travel_time_minutes,
        seats=seats,
    )


def parse_seats(json_seats: list[dict]):
    seats = []
    for json_seat in json_seats:
        type_value = json_seat['type']
        type_seat = get_seat_type_by_value(type_value)
        seat = Seat(
            type=type_seat,
            available=int(json_seat['availableSeats']),
        )
        seats.append(seat)

    return seats


def get_seat_type_by_value(value) -> SeatType:
    for seat_type in SeatType:
        if isinstance(value, int) and seat_type.value[0] == value:
            return seat_type
        if isinstance(value, str) and seat_type.value[1] == value:
            return seat_type

    return SeatType.DEFAULT
