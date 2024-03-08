import json
import logging

import requests

from apps.booking_uz_gov_ua.models import Station

logger = logging.getLogger('django')

URL = 'https://booking.uz.gov.ua/train_search/station/'

HEADERS = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6,zh-TW;q=0.5,zh-CN;q=0.4,zh;q=0.3',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': '__uzma=896344f5-fd16-49fa-b393-20e4c59ec1a3; __uzmb=1709311875; __uzme=0135; _gv_lang=uk; _gv_sessid=k5nebo2ei63hvbabl3ue7uf360; HTTPSERVERID=server2; cookiesession1=678B286E1F5EF95A9D4015EAA17B0B0E; __ssds=3; _ga=GA1.3.366466215.1709311887; _gid=GA1.3.1105481561.1709311887; __ssuzjsr3=a9be0cd8e; __uzmaj3=ca18f539-65ac-4edf-85e2-b90021fc50ea; __uzmbj3=1709311883; _gat=1; __uzmcj3=158131979396; __uzmdj3=1709318494; _ga_PRV3EE0FGZ=GS1.3.1709317271.2.1.1709318499.0.0.0; __uzmd=1709318500; __uzmc=330865216110',
    'Pragma': 'no-cache',
    'Referer': 'https://booking.uz.gov.ua/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'cache-version': '761',
    'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

PARAM_NAME = 'term'


def scrapy(title: str):
    if len(title) < 2:
        logger.warning(f'Length {title} is less than 2.')
        return

    logger.info(f'Task scrapping station:{title} start')
    try:
        # sleep(randint(1, 5))
        response = requests.get(URL, params={PARAM_NAME: title}, headers=HEADERS, )
        response.raise_for_status()
        items = json.loads(response.text)
        return scrapy_station(items)
    except Exception as e:
        logger.error(f"Can't scraping: {title}: {e}")
        raise ValueError(f"Can't scraping {title}.")
    finally:
        logger.info(f'Task scrapping station:{title} finish')


def scrapy_station(items: list[dict]):
    if not items:
        logger.warning(f'No items for save.')
        return

    return [Station(title=item['title'], value=item['value']) for item in items]
