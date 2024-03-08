import json
import logging
from random import randint
from time import sleep

import requests
from django.db import transaction

from apps.booking_uz_gov_ua.models import Station

logger = logging.getLogger('django')

URL = 'https://booking.uz.gov.ua/train_wagons/'

HEADERS = {
    'Accept': '*/*',
    'Accept-Language': 'uk-UA,uk;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Cookie': '__uzma=48795874-3270-4a23-969a-773febae62b0; __uzmb=1709398801; __uzme=6494; _gv_lang=uk; _gv_sessid=uhn81fuop41jqmb9onfpvir763; HTTPSERVERID=server3; cookiesession1=678B286EBEED465E1F72AC9F728641A9; __ssds=3; _ga=GA1.3.1732004976.1709399341; _gid=GA1.3.877593508.1709399341; __ssuzjsr3=a9be0cd8e; __uzmaj3=60a241a7-9190-4f6a-ad60-3515dd5fb2ac; __uzmbj3=1709399340; __uzmcj3=833952221343; __uzmdj3=1709400306; __uzmc=6985714551199; __uzmd=1709400683',
    'Origin': 'https://booking.uz.gov.ua',
    'Pragma': 'no-cache',
    'Referer': 'https://booking.uz.gov.ua/?from=2200001&to=2218000&date=2024-03-04&time=00%3A00&train=045%D0%94&wagon_type_id=%D0%9A&url=train-wagons',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'cache-version': '761',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

smpl_data = {
    'from': '2200001',
    'to': '2218000',
    'date': '2024-03-04',
    'train': '045Д',
    'wagon_type_id': 'К',
    'get_tpl': '1',
    'captcha': '03AFcWeA6leCyyMB_59nAzhOCNCDPtulttbDdMVDlFryDnbRB2a6S6my3ej8xHGYm0I5WkQdJHmayWaRfsZmsxwSZ6RMXSyoGVNUbXNp1M46DEMlASAPCI4fR6JK3yebqBx5QcucjnAfb3XiKmhZVE__r5QiJvnpIFsyJi4rqRJg2jCh6cdOONazmTFkHVpta4vyrDpQRqAqKTNyUU-hFeVcTERnER7Ps123j_ypYgTkBfSIwtw9VKbEhsgY7AOEduXwumgNz8QX0PNZ_v6sCGOTkL3meiE9atA9WlXLJqIEVqUIOPy21zREeaiPGvi5gI9_2fa6zme_CStaC5YOgoVq_it8kCY89af9eJnxIJDg8IV_Nxry0H60DzxWa0fQPgl02VSfF5UVR2Uh8i1vtOhQibH-jDccb-bfRKYZJp9voEN0fX2KYhqCB0SwqM85kDlqBquB1wX6CNAne5HKLl7IUWlhjhSFhyWGTNStuFnX3XcFQO7aShPS9Y9tXGSBetllsWmAisVZBfH-jLMvkcuPiUXWGMdz4v-24M204mOLZUP4YhLDf0FQGerD_2iYCGfqSAiCA5KFdBW1SuH8vUabnvZqt8wF6NeGoaru3rw_9O9Fh6av-ePyNWzNt2OUl3tVKQ1_OcJJkYLyk-o-6TcWE65FBsbwS-rsCBT3B23FyrPjv8TCpaLJo',
}

cookies = {
    '__uzma': '48795874-3270-4a23-969a-773febae62b0',
    '__uzmb': '1709398801',
    '__uzme': '6494',
    '_gv_lang': 'uk',
    '_gv_sessid': 'uhn81fuop41jqmb9onfpvir763',
    'HTTPSERVERID': 'server3',
    'cookiesession1': '678B286EBEED465E1F72AC9F728641A9',
    '__ssds': '3',
    '_ga': 'GA1.3.1732004976.1709399341',
    '_gid': 'GA1.3.877593508.1709399341',
    '__ssuzjsr3': 'a9be0cd8e',
    '__uzmaj3': '60a241a7-9190-4f6a-ad60-3515dd5fb2ac',
    '__uzmbj3': '1709399340',
    '__uzmcj3': '833952221343',
    '__uzmdj3': '1709400306',
    '__uzmc': '6985714551199',
    '__uzmd': '1709400683',
}


def scrap(**kwargs):
    logger.info(f'Task scrapping train start')
    try:
        data_dict = {
            'from': kwargs['from'],
            'to': kwargs['to'],
            'date': kwargs['date'],
            'time': kwargs['time'],
        }
        response = requests.post(URL, data=data_dict, headers=HEADERS, )
        response.raise_for_status()
        items = json.loads(response.text)
        return save_items(items)
    except Exception as e:
        logger.error(f"Can't scraping: train: {e}")

    logger.info('Task scrapping train done')


def save_items(items: list[dict]):
    if not items:
        logger.warning(f'No items for save.')
        return

    stations = (Station(title=item['title'], value=item['value']) for item in items)
    with transaction.atomic():
        for station in stations:
            if not Station.objects.filter(value=station.value).exists():
                station.save()
