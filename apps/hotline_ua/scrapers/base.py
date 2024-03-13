import re

from bs4 import BeautifulSoup


class _BaseScraper:
    _HEADERS = {
        'authority': 'hotline.ua',
        'accept': '*/*',
        'accept-language': 'uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6,zh-TW;q=0.5,zh-CN;q=0.4,zh;q=0.3',
        'authorization': 'Bearer eyJhbGciOiJzaGEyNTYiLCJ0eXAiOiJKV1QifQ==.eyJ1c2VySWQiOiI3MDg3NzUwNTkifQ==.1TwhWXJmVsSV0UFhm84f7KASw16PTLXq7Zfj+1mtr+U=',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'cookie': 'region_mode=1; GN_USER_ID_KEY=135f870d-05ca-474c-8f01-184276ebf6b4; city_id=154; G_ENABLED_IDPS=google; hotline_club_session=fy071b9iv04b17srtwv60sfhubm9tsm2ff75quy2g9rr6rr4wr55f9ity9iq3q87; hl_guest_id=08c4cc93f23cc30f70abe1e4dc5181da; _gcl_au=1.1.1288441519.1705136242; __rtbh.lid=%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%222yNiUmoxOZZMZfKZd3Hm%22%7D; _fbp=fb.1.1705136244176.838695506; am-uid-f=033ed450-d653-459e-bf0f-63080c4ef25e; _tt_enable_cookie=1; _ttp=_HOxyTw-rjSiaLHdWuwvlu3FGpR; _gcl_aw=GCL.1705138683.Cj0KCQiAhomtBhDgARIsABcaYykzGy3EiQzTIf3TcDb6jjTmIAodY2d4Y5xc1zojjq6GM4304OIJl6oaAjFfEALw_wcB; _gac_UA-2141710-13=1.1705138939.Cj0KCQiAhomtBhDgARIsABcaYykzGy3EiQzTIf3TcDb6jjTmIAodY2d4Y5xc1zojjq6GM4304OIJl6oaAjFfEALw_wcB; datePushRejected=1705236250359; __gpi=UID=00000d4166909706:T=1705236258:RT=1705236258:S=ALNI_Mbyl0g6FyRKwkZdvM3XDZ_5-Hn34g; tp_hide=1; gd_cmp=0%2C25131776%2C25106396%2C25066132%2C25036741%2C23889422%2C25050671; region=22; hluniqueid=2a66810ae94e9482cf8adb4f30266e1a; hluniqueid_ctl=0eb97665c1d554d7934e07546382eb78; hl_sid=847ae88f06a7d552ed4c881f04d73974; region_popup=3; user_jwt=eyJhbGciOiJzaGEyNTYiLCJ0eXAiOiJKV1QifQ%3D%3D.eyJ1c2VySWQiOiI3MDg3NzUwNTkifQ%3D%3D.1TwhWXJmVsSV0UFhm84f7KASw16PTLXq7Zfj%2B1mtr%2BU%3D; PHPSESSID=3a76277d93a3ac395bbd397c3b899117; _gid=GA1.2.1318277745.1710145330; store.test; am-uid=9909952a0a70429abed4e26608d410d4; __rtbh.uid=%7B%22eventType%22%3A%22uid%22%2C%22id%22%3A%22708775059%22%7D; language=uk; languageSetByUser=true; store.test=; guest_visited_sections=%5B12%2C128%2C124%2C156%2C28%5D; guest_visited_cards=%5B25066132%2C25131776%2C25106396%2C25063139%2C23889422%2C25050671%2C25101752%2C24600980%2C25034799%2C24567445%5D; __gads=ID=8bb088466c3f62b0:T=1705136394:RT=1710175388:S=ALNI_MY_6ZdtGvmEuryy79yGK91XiWpaXQ; __eoi=ID=1c2ef75ef571b57d:T=1707036366:RT=1710175388:S=AA-AfjYMghVC13M0EcYZTTy13abP; remade_cps=0; _dc_gtm_UA-2141710-13=1; _ga_CYEKXW8GPN=GS1.1.1710175423.15.1.1710175428.55.0.0; _ga=GA1.1.2084401843.1661702529; GN_SESSION_ID_KEY=f77afda5-7c02-4ee8-8037-a9b6d666f52d',
        'origin': 'https://hotline.ua',
        'pragma': 'no-cache',
        'referer': 'https://hotline.ua/',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'x-language': 'uk',
        'x-referer': 'https://hotline.ua//',
        # 'x-request-id': 'b247e3333d8b175ef259ffbddc989ce7',
    }

    _BASE_URL = 'https://hotline.ua/'
    _GRAPHQL_URL = 'https://hotline.ua/svc/frontend-api/graphql'
    _SEARCH_URL = 'https://hotline.ua/svc/search/api/json-rpc'

    parser_class = None

    @property
    def scrapy_items(self):
        return []

    class Meta:
        abstract = True
