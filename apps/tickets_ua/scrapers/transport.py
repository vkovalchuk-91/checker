import re

from bs4 import BeautifulSoup


class _TransportScraper:
    _HEADERS = {
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

    _COOKIES = {
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

    _DATE_FORMAT = '%d.%m.%Y'
    _TIME_FORMAT = '%H:%M'

    parser_class = None

    @property
    def scrapy_items(self):
        return []

    def _get_token(self, response_text: str):
        soup = BeautifulSoup(response_text, 'html.parser')
        script_content = soup.find('script', string=re.compile(r'"csrfToken"'))

        if script_content:
            match = re.search(r'"csrfToken":"([^"]+)"', script_content.string)
            if match:
                return match.group(1)
        return None

    class Meta:
        abstract = True
