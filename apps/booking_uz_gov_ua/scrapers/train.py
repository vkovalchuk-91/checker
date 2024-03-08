import datetime
import json
import logging

import requests

from apps.booking_uz_gov_ua.models import Train, Place

logger = logging.getLogger('django')

MAIN_URL = 'https://booking.uz.gov.ua/'
TRAIN_SEARCH_URL = 'https://booking.uz.gov.ua/train_search/'

HEADERS = {
    'Accept': '*/*',
    'Accept-Language': 'uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6,zh-TW;q=0.5,zh-CN;q=0.4,zh;q=0.3',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Cookie': '__uzma=61e5b534-9a31-4c50-933b-3680913da860; __uzmb=1709272915; __uzme=4607; _gv_lang=uk; cookiesession1=678B286EA4640BBD32E846618C28271E; _ga=GA1.3.1817854823.1709272918; __ssds=3; __ssuzjsr3=a9be0cd8e; __uzmaj3=311032e7-1f0c-44b8-8ae3-08b30359bb62; __uzmbj3=1709272937; _gv_sessid=517fceubd80fvpgkvvoen4onm5; HTTPSERVERID=server2; _gid=GA1.3.1430862200.1709805422; __uzmcj3=518393767117; __uzmdj3=1709805430; __uzmc=8899626844414; __uzmd=1709805451',
    'Origin': 'https://booking.uz.gov.ua',
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

smpl_data = {
    'from': '2200001',
    'to': '2218000',
    'date': '2024-03-08',
    'time': '00:00',
    'get_tpl': '1',
    # 'captcha': '03AFcWeA6leCyyMB_59nAzhOCNCDPtulttbDdMVDlFryDnbRB2a6S6my3ej8xHGYm0I5WkQdJHmayWaRfsZmsxwSZ6RMXSyoGVNUbXNp1M46DEMlASAPCI4fR6JK3yebqBx5QcucjnAfb3XiKmhZVE__r5QiJvnpIFsyJi4rqRJg2jCh6cdOONazmTFkHVpta4vyrDpQRqAqKTNyUU-hFeVcTERnER7Ps123j_ypYgTkBfSIwtw9VKbEhsgY7AOEduXwumgNz8QX0PNZ_v6sCGOTkL3meiE9atA9WlXLJqIEVqUIOPy21zREeaiPGvi5gI9_2fa6zme_CStaC5YOgoVq_it8kCY89af9eJnxIJDg8IV_Nxry0H60DzxWa0fQPgl02VSfF5UVR2Uh8i1vtOhQibH-jDccb-bfRKYZJp9voEN0fX2KYhqCB0SwqM85kDlqBquB1wX6CNAne5HKLl7IUWlhjhSFhyWGTNStuFnX3XcFQO7aShPS9Y9tXGSBetllsWmAisVZBfH-jLMvkcuPiUXWGMdz4v-24M204mOLZUP4YhLDf0FQGerD_2iYCGfqSAiCA5KFdBW1SuH8vUabnvZqt8wF6NeGoaru3rw_9O9Fh6av-ePyNWzNt2OUl3tVKQ1_OcJJkYLyk-o-6TcWE65FBsbwS-rsCBT3B23FyrPjv8TCpaLJo',
}

CAPTCHA = '03AFcWeA6leCyyMB_59nAzhOCNCDPtulttbDdMVDlFryDnbRB2a6S6my3ej8xHGYm0I5WkQdJHmayWaRfsZmsxwSZ6RMXSyoGVNUbXNp1M46DEMlASAPCI4fR6JK3yebqBx5QcucjnAfb3XiKmhZVE__r5QiJvnpIFsyJi4rqRJg2jCh6cdOONazmTFkHVpta4vyrDpQRqAqKTNyUU-hFeVcTERnER7Ps123j_ypYgTkBfSIwtw9VKbEhsgY7AOEduXwumgNz8QX0PNZ_v6sCGOTkL3meiE9atA9WlXLJqIEVqUIOPy21zREeaiPGvi5gI9_2fa6zme_CStaC5YOgoVq_it8kCY89af9eJnxIJDg8IV_Nxry0H60DzxWa0fQPgl02VSfF5UVR2Uh8i1vtOhQibH-jDccb-bfRKYZJp9voEN0fX2KYhqCB0SwqM85kDlqBquB1wX6CNAne5HKLl7IUWlhjhSFhyWGTNStuFnX3XcFQO7aShPS9Y9tXGSBetllsWmAisVZBfH-jLMvkcuPiUXWGMdz4v-24M204mOLZUP4YhLDf0FQGerD_2iYCGfqSAiCA5KFdBW1SuH8vUabnvZqt8wF6NeGoaru3rw_9O9Fh6av-ePyNWzNt2OUl3tVKQ1_OcJJkYLyk-o-6TcWE65FBsbwS-rsCBT3B23FyrPjv8TCpaLJo'

DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H:%M'

PROXIES = [
    {'https': 'https://180.183.157.159:8080'},
    {'http': 'http://46.4.96.137:1080'},
    {'http': 'http://47.91.88.100:1080'},
    {'http': 'http://45.77.56.114:30205'},
    {'http': 'http://82.196.11.105:1080'},
]

cookies = {
    '__uzma': '896344f5-fd16-49fa-b393-20e4c59ec1a3',
    '__uzmb': '1709311875',
    '__uzme': '0135',
    '_gv_lang': 'uk',
    'cookiesession1': '678B286E1F5EF95A9D4015EAA17B0B0E',
    '__ssds': '3',
    '_ga': 'GA1.3.366466215.1709311887',
    '_gid': 'GA1.3.1105481561.1709311887',
    '__ssuzjsr3': 'a9be0cd8e',
    '__uzmaj3': 'ca18f539-65ac-4edf-85e2-b90021fc50ea',
    '__uzmbj3': '1709311883',
    '_gv_sessid': 'bk6naf699c2u0jp7pev4q688b0',
    'HTTPSERVERID': 'server2',
    '__uzmcj3': '250183172317',
    '__uzmdj3': '1709399177',
    '_gat': '1',
    '_ga_PRV3EE0FGZ': 'GS1.3.1709397757.4.1.1709399178.0.0.0',
    '__uzmc': '7701922059979',
    '__uzmd': '1709399184',
}

AAA = '{"data":{"list":[{"num":"143Рћ","category":0,"isTransformer":0,"travelTime":"9:16","from":{"code":"2200001","station":"РљРёС—РІ-РџР°СЃР°Р¶РёСЂСЃСЊРєРёР№","stationTrain":"РЎСѓРјРё","date":"С‡РµС‚РІРµСЂ, 07.03.2024","time":"01:14","sortTime":1709766840,"srcDate":"2024-03-07"},"to":{"code":"2218000","station":"Р›СЊРІС–РІ","stationTrain":"Р Р°С…С–РІ","date":"С‡РµС‚РІРµСЂ, 07.03.2024","time":"10:30","sortTime":1709800200},"types":[],"child":{"minDate":"2010-03-08","maxDate":"2024-03-07"},"allowStudent":0,"allowBooking":1,"isCis":0,"isEurope":0,"allowPrivilege":1,"noReserve":1},{"num":"142Рљ","category":0,"isTransformer":0,"travelTime":"9:16","from":{"code":"2200001","station":"РљРёС—РІ-РџР°СЃР°Р¶РёСЂСЃСЊРєРёР№","stationTrain":"Р§РµСЂРЅС–РіС–РІ","date":"С‡РµС‚РІРµСЂ, 07.03.2024","time":"01:14","sortTime":1709766840,"srcDate":"2024-03-07"},"to":{"code":"2218000","station":"Р›СЊРІС–РІ","stationTrain":"Р†РІР°РЅРѕ-Р¤СЂР°РЅРєС–РІСЃСЊРє","date":"С‡РµС‚РІРµСЂ, 07.03.2024","time":"10:30","sortTime":1709800200},"types":[],"child":{"minDate":"2010-03-08","maxDate":"2024-03-07"},"allowStudent":0,"allowBooking":1,"isCis":0,"isEurope":0,"allowPrivilege":1,"noReserve":1},{"num":"001Р”","category":0,"isTransformer":0,"travelTime":"6:46","from":{"code":"2200001","station":"РљРёС—РІ-РџР°СЃР°Р¶РёСЂСЃСЊРєРёР№","stationTrain":"РҐР°СЂРєС–РІ-РџР°СЃ","date":"С‡РµС‚РІРµСЂ, 07.03.2024","time":"01:54","sortTime":1709769240,"srcDate":"2024-03-07"},"to":{"code":"2218000","station":"Р›СЊРІС–РІ","stationTrain":"Р†РІР°РЅРѕ-Р¤СЂР°РЅРєС–РІСЃСЊРє","date":"С‡РµС‚РІРµСЂ, 07.03.2024","time":"08:40","sortTime":1709793600},"types":[],"child":{"minDate":"2010-03-08","maxDate":"2024-03-07"},"allowStudent":0,"allowBooking":1,"isCis":0,"isEurope":0,"allowPrivilege":1,"noReserve":1},{"num":"201Рљ","category":0,"isTransformer":0,"travelTime":"6:46","from":{"code":"2200001","station":"РљРёС—РІ-РџР°СЃР°Р¶РёСЂСЃСЊРєРёР№","stationTrain":"РҐР°СЂРєС–РІ-РџР°СЃ","date":"С‡РµС‚РІРµСЂ, 07.03.2024","time":"01:54","sortTime":1709769240,"srcDate":"2024-03-07"},"to":{"code":"2218000","station":"Р›СЊРІС–РІ","stationTrain":"Р’РѕСЂРѕС…С‚Р°","date":"С‡РµС‚РІРµСЂ, 07.03.2024","time":"08:40","sortTime":1709793600},"types":[],"child":{"minDate":"2010-03-08","maxDate":"2024-03-07"},"allowStudent":0,"allowBooking":1,"isCis":0,"isEurope":0,"allowPrivilege":1,"noReserve":1},{"num":"104Рџ","category":0,"isTransformer":0,"travelTime":"8:33","from":{"code":"2200001","station":"РљРёС—РІ-РџР°СЃР°Р¶РёСЂСЃСЊРєРёР№","stationTrain":"РљСЂР°РјР°С‚РѕСЂСЃСЊРє","date":"С‡РµС‚РІРµСЂ, 07.03.2024","time":"02:57","sortTime":1709773020,"srcDate":"2024-03-07"},"to":{"code":"2218000","station":"Р›СЊРІС–РІ","stationTrain":"Р›СЊРІС–РІ","date":"С‡РµС‚РІРµСЂ, 07.03.2024","time":"11:30","sortTime":1709803800},"types":[],"child":{"minDate":"2010-03-08","maxDate":"2024-03-07"},"allowStudent":0,"allowBooking":1,"isCis":0,"isEurope":0,"allowPrivilege":1,"noReserve":1},{"num":"021Рћ","category":0,"isTransformer":0,"travelTime":"8:33","from":{"code":"2200001","station":"РљРёС—РІ-РџР°СЃР°Р¶РёСЂСЃСЊРєРёР№","stationTrain":"РҐР°СЂРєС–РІ-РџР°СЃ","date":"С‡РµС‚РІРµСЂ, 07.03.2024","time":"02:57","sortTime":1709773020,"srcDate":"2024-03-07"},"to":{"code":"2218000","station":"Р›СЊРІС–РІ","stationTrain":"Р›СЊРІС–РІ","date":"С‡РµС‚РІРµСЂ, 07.03.2024","time":"11:30","sortTime":1709803800},"types":[],"child":{"minDate":"2010-03-08","maxDate":"2024-03-07"},"allowStudent":0,"allowBooking":1,"isCis":0,"isEurope":0,"allowPrivilege":1,"noReserve":1},{"num":"079Рџ","category":0,"isTransformer":0,"travelTime":"6:49","from":{"code":"2200001","station":"РљРёС—РІ-РџР°СЃР°Р¶РёСЂСЃСЊРєРёР№","stationTrain":"Р”РЅС–РїСЂРѕ-Р“РѕР»РѕРІРЅРёР№","date":"С‡РµС‚РІРµСЂ, 07.03.2024","time":"06:10","sortTime":1709784600,"srcDate":"2024-03-07"},"to":{"code":"2218000","station":"Р›СЊРІС–РІ","stationTrain":"Р›СЊРІС–РІ","date":"С‡РµС‚РІРµСЂ, 07.03.2024","time":"12:59","sortTime":1709809140},"types":[],"child":{"minDate":"2010-03-08","maxDate":"2024-03-07"},"allowStudent":0,"allowBooking":1,"isCis":0,"isEurope":0,"allowPrivilege":1,"noReserve":1},{"num":"743Рљ","category":0,"isTransformer":0,"travelTime":"5:35","from":{"code":"2200001","station":"РљРёС—РІ-РџР°СЃР°Р¶РёСЂСЃСЊРєРёР№","stationTrain":"Р”Р°СЂРЅРёС†СЏ","date":"С‡РµС‚РІРµСЂ, 07.03.2024","time":"06:19","sortTime":1709785140,"srcDate":"2024-03-07"},"to":{"code":"2218000","station":"Р›СЊРІС–РІ","stationTrain":"Р›СЊРІС–РІ","date":"С‡РµС‚РІРµСЂ, 07.03.2024","time":"11:54","sortTime":1709805240},"types":[],"child":{"minDate":"2010-03-08","maxDate":"2024-03-07"},"allowStudent":0,"allowBooking":1,"isCis":0,"isEurope":0,"allowPrivilege":1,"noReserve":1},{"num":"063Рљ","category":0,"isTransformer":0,"travelTime":"7:04","from":{"code":"2200001","station":"РљРёС—РІ-РџР°СЃР°Р¶РёСЂСЃСЊРєРёР№","stationTrain":"РҐР°СЂРєС–РІ-РџР°СЃ","date":"С‡РµС‚РІРµСЂ, 07.03.2024","time":"06:35","sortTime":1709786100,"srcDate":"2024-03-07"},"to":{"code":"2218000","station":"Р›СЊРІС–РІ","stationTrain":"Р›СЊРІС–РІ","date":"С‡РµС‚РІРµСЂ, 07.03.2024","time":"13:39","sortTime":1709811540},"types":[],"child":{"minDate":"2010-03-08","maxDate":"2024-03-07"},"allowStudent":0,"allowBooking":1,"isCis":0,"isEurope":0,"allowPrivilege":1,"noReserve":1},{"num":"112Рџ","category":0,"isTransformer":0,"travelTime":"7:04","from":{"code":"2200001","station":"РљРёС—РІ-РџР°СЃР°Р¶РёСЂСЃСЊРєРёР№","stationTrain":"Р†Р·СЋРј","date":"С‡РµС‚РІРµСЂ, 07.03.2024","time":"06:35","sortTime":1709786100,"srcDate":"2024-03-07"},"to":{"code":"2218000","station":"Р›СЊРІС–РІ","stationTrain":"Р›СЊРІС–РІ","date":"С‡РµС‚РІРµСЂ, 07.03.2024","time":"13:39","sortTime":1709811540},"types":[],"child":{"minDate":"2010-03-08","maxDate":"2024-03-07"},"allowStudent":0,"allowBooking":1,"isCis":0,"isEurope":0,"allowPrivilege":1,"noReserve":1},{"num":"715Рљ","category":0,"isTransformer":0,"travelTime":"7:14","from":{"code":"2200001","station":"РљРёС—РІ-РџР°СЃР°Р¶РёСЂСЃСЊРєРёР№","stationTrain":"РљРёС—РІ-РџР°СЃР°Р¶РёСЂСЃСЊРєРёР№","date":"С‡РµС‚РІРµСЂ, 07.03.2024","time":"12:06","sortTime":1709805960,"srcDate":"2024-03-07"},"to":{"code":"2218000","station":"Р›СЊРІС–РІ","stationTrain":"РџС€РµРјРёСЃР»СЊ","date":"С‡РµС‚РІРµСЂ, 07.03.2024","time":"19:20","sortTime":1709832000},"types":[],"child":{"minDate":"2010-03-08","maxDate":"2024-03-07"},"allowStudent":0,"allowBooking":1,"isCis":0,"isEurope":0,"allowPrivilege":1,"noReserve":1},{"num":"749Рћ","category":0,"isTransformer":0,"travelTime":"6:24","from":{"code":"2200001","station":"РљРёС—РІ-РџР°СЃР°Р¶РёСЂСЃСЊРєРёР№","stationTrain":"РљРёС—РІ-РџР°СЃР°Р¶РёСЂСЃСЊРєРёР№","date":"С‡РµС‚РІРµСЂ, 07.03.2024","time":"13:20","sortTime":1709810400,"srcDate":"2024-03-07"},"to":{"code":"2218000","station":"Р›СЊРІС–РІ","stationTrain":"РЈР¶РіРѕСЂРѕРґ","date":"С‡РµС‚РІРµСЂ, 07.03.2024","time":"19:44","sortTime":1709833440},"types":[],"child":{"minDate":"2010-03-08","maxDate":"2024-03-07"},"allowStudent":0,"allowBooking":1,"isCis":0,"isEurope":0,"allowPrivilege":1,"noReserve":1},{"num":"013Рљ","category":6,"isTransformer":0,"travelTime":"9:44","from":{"code":"2200001","station":"РљРёС—РІ-РџР°СЃР°Р¶РёСЂСЃСЊРєРёР№","stationTrain":"РљРёС—РІ-РџР°СЃР°Р¶РёСЂСЃСЊРєРёР№","date":"С‡РµС‚РІРµСЂ, 07.03.2024","time":"15:58","sortTime":1709819880,"srcDate":"2024-03-07"},"to":{"code":"2218000","station":"Р›СЊРІС–РІ","stationTrain":"РЎРѕР»РѕС‚РІРёРЅРѕ 1","date":"РїСЏС‚РЅРёС†СЏ, 08.03.2024","time":"01:42","sortTime":1709854920},"types":[{"id":"Р›","title":"Р›СЋРєСЃ","letter":"Р›","places":4}],"child":{"minDate":"2010-03-08","maxDate":"2024-03-07"},"allowStudent":0,"allowBooking":1,"isCis":0,"isEurope":0,"allowPrivilege":1,"noReserve":1},{"num":"055Рљ","category":0,"isTransformer":0,"travelTime":"9:44","from":{"code":"2200001","station":"РљРёС—РІ-РџР°СЃР°Р¶РёСЂСЃСЊРєРёР№","stationTrain":"РљРёС—РІ-РџР°СЃР°Р¶РёСЂСЃСЊРєРёР№","date":"С‡РµС‚РІРµСЂ, 07.03.2024","time":"15:58","sortTime":1709819880,"srcDate":"2024-03-07"},"to":{"code":"2218000","station":"Р›СЊРІС–РІ","stationTrain":"Р Р°С…С–РІ","date":"РїСЏС‚РЅРёС†СЏ, 08.03.2024","time":"01:42","sortTime":1709854920},"types":[{"id":"Р›","title":"Р›СЋРєСЃ","letter":"Р›","places":2}],"child":{"minDate":"2010-03-08","maxDate":"2024-03-07"},"allowStudent":0,"allowBooking":1,"isCis":0,"isEurope":0,"allowPrivilege":1,"noReserve":1},{"num":"745Рћ","category":0,"isTransformer":0,"travelTime":"6:54","from":{"code":"2200001","station":"РљРёС—РІ-РџР°СЃР°Р¶РёСЂСЃСЊРєРёР№","stationTrain":"РљРёС—РІ-РџР°СЃР°Р¶РёСЂСЃСЊРєРёР№","date":"С‡РµС‚РІРµСЂ, 07.03.2024","time":"16:38","sortTime":1709822280,"srcDate":"2024-03-07"},"to":{"code":"2218000","station":"Р›СЊРІС–РІ","stationTrain":"Р›СЊРІС–РІ","date":"С‡РµС‚РІРµСЂ, 07.03.2024","time":"23:32","sortTime":1709847120},"types":[],"child":{"minDate":"2010-03-08","maxDate":"2024-03-07"},"allowStudent":0,"allowBooking":1,"isCis":0,"isEurope":0,"allowPrivilege":1,"noReserve":1},{"num":"131Рџ","category":0,"isTransformer":0,"travelTime":"15:13","from":{"code":"2200001","station":"РљРёС—РІ-РџР°СЃР°Р¶РёСЂСЃСЊРєРёР№","stationTrain":"Р”РЅС–РїСЂРѕ-Р“РѕР»РѕРІРЅРёР№","date":"С‡РµС‚РІРµСЂ, 07.03.2024","time":"17:58","sortTime":1709827080,"srcDate":"2024-03-07"},"to":{"code":"2218000","station":"Р›СЊРІС–РІ","stationTrain":"Р›СЊРІС–РІ","date":"РїСЏС‚РЅРёС†СЏ, 08.03.2024","time":"09:11","sortTime":1709881860},"types":[],"child":{"minDate":"2010-03-08","maxDate":"2024-03-07"},"allowStudent":0,"allowBooking":1,"isCis":0,"isEurope":0,"allowPrivilege":1,"noReserve":1},{"num":"113Рћ","category":0,"isTransformer":0,"travelTime":"15:13","from":{"code":"2200001","station":"РљРёС—РІ-РџР°СЃР°Р¶РёСЂСЃСЊРєРёР№","stationTrain":"РҐР°СЂРєС–РІ-РџР°СЃ","date":"С‡РµС‚РІРµСЂ, 07.03.2024","time":"17:58","sortTime":1709827080,"srcDate":"2024-03-07"},"to":{"code":"2218000","station":"Р›СЊРІС–РІ","stationTrain":"Р›СЊРІС–РІ","date":"РїСЏС‚РЅРёС†СЏ, 08.03.2024","time":"09:11","sortTime":1709881860},"types":[],"child":{"minDate":"2010-03-08","maxDate":"2024-03-07"},"allowStudent":0,"allowBooking":1,"isCis":0,"isEurope":0,"allowPrivilege":1,"noReserve":1},{"num":"081Рљ","category":6,"isTransformer":0,"travelTime":"9:53","from":{"code":"2200001","station":"РљРёС—РІ-РџР°СЃР°Р¶РёСЂСЃСЊРєРёР№","stationTrain":"РљРёС—РІ-РџР°СЃР°Р¶РёСЂСЃСЊРєРёР№","date":"С‡РµС‚РІРµСЂ, 07.03.2024","time":"18:35","sortTime":1709829300,"srcDate":"2024-03-07"},"to":{"code":"2218000","station":"Р›СЊРІС–РІ","stationTrain":"РЈР¶РіРѕСЂРѕРґ","date":"РїСЏС‚РЅРёС†СЏ, 08.03.2024","time":"04:28","sortTime":1709864880},"types":[{"id":"Рџ","title":"РџР»Р°С†РєР°СЂС‚","letter":"Рџ","places":8}],"child":{"minDate":"2010-03-08","maxDate":"2024-03-07"},"allowStudent":0,"allowBooking":1,"isCis":0,"isEurope":0,"allowPrivilege":1,"noReserve":1},{"num":"029Рљ","category":0,"isTransformer":0,"travelTime":"6:37","from":{"code":"2200001","station":"РљРёС—РІ-РџР°СЃР°Р¶РёСЂСЃСЊРєРёР№","stationTrain":"РљРёС—РІ-РџР°СЃР°Р¶РёСЂСЃСЊРєРёР№","date":"С‡РµС‚РІРµСЂ, 07.03.2024","time":"19:19","sortTime":1709831940,"srcDate":"2024-03-07"},"to":{"code":"2218000","station":"Р›СЊРІС–РІ","stationTrain":"РЈР¶РіРѕСЂРѕРґ","date":"РїСЏС‚РЅРёС†СЏ, 08.03.2024","time":"01:56","sortTime":1709855760},"types":[],"child":{"minDate":"2010-03-08","maxDate":"2024-03-07"},"allowStudent":0,"allowBooking":1,"isCis":0,"isEurope":0,"allowPrivilege":1,"noReserve":1},{"num":"051Рљ","category":0,"isTransformer":0,"travelTime":"6:42","from":{"code":"2200001","station":"РљРёС—РІ-РџР°СЃР°Р¶РёСЂСЃСЊРєРёР№","stationTrain":"РљРёС—РІ-РџР°СЃР°Р¶РёСЂСЃСЊРєРёР№","date":"С‡РµС‚РІРµСЂ, 07.03.2024","time":"19:27","sortTime":1709832420,"srcDate":"2024-03-07"},"to":{"code":"2218000","station":"Р›СЊРІС–РІ","stationTrain":"РџС€РµРјРёСЃР»СЊ","date":"РїСЏС‚РЅРёС†СЏ, 08.03.2024","time":"02:09","sortTime":1709856540},"types":[{"id":"Рљ","title":"РљСѓРїРµ","letter":"Рљ","places":5}],"child":{"minDate":"2010-03-08","maxDate":"2024-03-07"},"allowStudent":0,"allowBooking":1,"isCis":0,"isEurope":0,"allowPrivilege":1,"noReserve":1},{"num":"705Рљ","category":1,"isTransformer":0,"travelTime":"7:29","from":{"code":"2200001","station":"РљРёС—РІ-РџР°СЃР°Р¶РёСЂСЃСЊРєРёР№","stationTrain":"РљРёС—РІ-РџР°СЃР°Р¶РёСЂСЃСЊРєРёР№","date":"С‡РµС‚РІРµСЂ, 07.03.2024","time":"20:05","sortTime":1709834700,"srcDate":"2024-03-07"},"to":{"code":"2218000","station":"Р›СЊРІС–РІ","stationTrain":"РџС€РµРјРёСЃР»СЊ","date":"РїСЏС‚РЅРёС†СЏ, 08.03.2024","time":"03:34","sortTime":1709861640},"types":[{"id":"РЎ1","title":"РЎРёРґСЏС‡РёР№ РїРµСЂС€РѕРіРѕ РєР»Р°СЃСѓ","letter":"РЎ1","places":51},{"id":"РЎ2","title":"РЎРёРґСЏС‡РёР№ РґСЂСѓРіРѕРіРѕ РєР»Р°СЃСѓ","letter":"РЎ2","places":148}],"child":{"minDate":"2010-03-08","maxDate":"2024-03-07"},"allowStudent":0,"allowBooking":1,"isCis":0,"isEurope":0,"allowPrivilege":1,"noReserve":1},{"num":"007Рљ","category":0,"isTransformer":1,"travelTime":"6:43","from":{"code":"2200001","station":"РљРёС—РІ-РџР°СЃР°Р¶РёСЂСЃСЊРєРёР№","stationTrain":"РљРёС—РІ-РџР°СЃР°Р¶РёСЂСЃСЊРєРёР№","date":"С‡РµС‚РІРµСЂ, 07.03.2024","time":"20:21","sortTime":1709835660,"srcDate":"2024-03-07"},"to":{"code":"2218000","station":"Р›СЊРІС–РІ","stationTrain":"Р§РµСЂРЅС–РІС†С–","date":"РїСЏС‚РЅРёС†СЏ, 08.03.2024","time":"03:04","sortTime":1709859840},"types":[{"id":"Рљ","title":"РљСѓРїРµ","letter":"Рљ","places":2},{"id":"Рџ","title":"РџР»Р°С†РєР°СЂС‚","letter":"Рџ","places":5}],"child":{"minDate":"2010-03-08","maxDate":"2024-03-07"},"allowStudent":0,"allowBooking":1,"isCis":0,"isEurope":0,"allowPrivilege":1,"noReserve":1},{"num":"095Рљ","category":0,"isTransformer":0,"travelTime":"6:49","from":{"code":"2200001","station":"РљРёС—РІ-РџР°СЃР°Р¶РёСЂСЃСЊРєРёР№","stationTrain":"РљРёС—РІ-РџР°СЃР°Р¶РёСЂСЃСЊРєРёР№","date":"С‡РµС‚РІРµСЂ, 07.03.2024","time":"20:29","sortTime":1709836140,"srcDate":"2024-03-07"},"to":{"code":"2218000","station":"Р›СЊРІС–РІ","stationTrain":"Р Р°С…С–РІ","date":"РїСЏС‚РЅРёС†СЏ, 08.03.2024","time":"03:18","sortTime":1709860680},"types":[{"id":"Рџ","title":"РџР»Р°С†РєР°СЂС‚","letter":"Рџ","places":1}],"child":{"minDate":"2010-03-08","maxDate":"2024-03-07"},"allowStudent":0,"allowBooking":1,"isCis":0,"isEurope":0,"allowPrivilege":1,"noReserve":1},{"num":"059Рљ","category":0,"isTransformer":0,"travelTime":"9:13","from":{"code":"2200001","station":"РљРёС—РІ-РџР°СЃР°Р¶РёСЂСЃСЊРєРёР№","stationTrain":"РљРёС—РІ-РџР°СЃР°Р¶РёСЂСЃСЊРєРёР№","date":"С‡РµС‚РІРµСЂ, 07.03.2024","time":"20:37","sortTime":1709836620,"srcDate":"2024-03-07"},"to":{"code":"2218000","station":"Р›СЊРІС–РІ","stationTrain":"Р§РѕРї","date":"РїСЏС‚РЅРёС†СЏ, 08.03.2024","time":"05:50","sortTime":1709869800},"types":[],"child":{"minDate":"2010-03-08","maxDate":"2024-03-07"},"allowStudent":0,"allowBooking":1,"isCis":0,"isEurope":0,"allowPrivilege":1,"noReserve":1},{"num":"015Рћ","category":0,"isTransformer":0,"travelTime":"7:00","from":{"code":"2200001","station":"РљРёС—РІ-РџР°СЃР°Р¶РёСЂСЃСЊРєРёР№","stationTrain":"РҐР°СЂРєС–РІ-РџР°СЃ","date":"С‡РµС‚РІРµСЂ, 07.03.2024","time":"21:18","sortTime":1709839080,"srcDate":"2024-03-07"},"to":{"code":"2218000","station":"Р›СЊРІС–РІ","stationTrain":"РЇСЃРёРЅСЏ","date":"РїСЏС‚РЅРёС†СЏ, 08.03.2024","time":"04:18","sortTime":1709864280},"types":[],"child":{"minDate":"2010-03-08","maxDate":"2024-03-07"},"allowStudent":0,"allowBooking":1,"isCis":0,"isEurope":0,"allowPrivilege":1,"noReserve":1},{"num":"043РЁ","category":0,"isTransformer":0,"travelTime":"8:11","from":{"code":"2200001","station":"РљРёС—РІ-РџР°СЃР°Р¶РёСЂСЃСЊРєРёР№","stationTrain":"Р§РµСЂРєР°СЃРё","date":"С‡РµС‚РІРµСЂ, 07.03.2024","time":"21:26","sortTime":1709839560,"srcDate":"2024-03-07"},"to":{"code":"2218000","station":"Р›СЊРІС–РІ","stationTrain":"Р†РІР°РЅРѕ-Р¤СЂР°РЅРєС–РІСЃСЊРє","date":"РїСЏС‚РЅРёС†СЏ, 08.03.2024","time":"05:37","sortTime":1709869020},"types":[{"id":"Рљ","title":"РљСѓРїРµ","letter":"Рљ","places":4}],"child":{"minDate":"2010-03-08","maxDate":"2024-03-07"},"allowStudent":0,"allowBooking":1,"isCis":0,"isEurope":0,"allowPrivilege":1,"noReserve":1},{"num":"049Рљ","category":0,"isTransformer":0,"travelTime":"6:50","from":{"code":"2200001","station":"РљРёС—РІ-РџР°СЃР°Р¶РёСЂСЃСЊРєРёР№","stationTrain":"РљРёС—РІ-РџР°СЃР°Р¶РёСЂСЃСЊРєРёР№","date":"С‡РµС‚РІРµСЂ, 07.03.2024","time":"21:48","sortTime":1709840880,"srcDate":"2024-03-07"},"to":{"code":"2218000","station":"Р›СЊРІС–РІ","stationTrain":"РўСЂСѓСЃРєР°РІРµС†СЊ","date":"РїСЏС‚РЅРёС†СЏ, 08.03.2024","time":"04:38","sortTime":1709865480},"types":[],"child":{"minDate":"2010-03-08","maxDate":"2024-03-07"},"allowStudent":0,"allowBooking":1,"isCis":0,"isEurope":0,"allowPrivilege":1,"noReserve":1},{"num":"089Рљ","category":0,"isTransformer":0,"travelTime":"10:00","from":{"code":"2200001","station":"РљРёС—РІ-РџР°СЃР°Р¶РёСЂСЃСЊРєРёР№","stationTrain":"РљРёС—РІ-РџР°СЃР°Р¶РёСЂСЃСЊРєРёР№","date":"С‡РµС‚РІРµСЂ, 07.03.2024","time":"22:14","sortTime":1709842440,"srcDate":"2024-03-07"},"to":{"code":"2218000","station":"Р›СЊРІС–РІ","stationTrain":"РџС€РµРјРёСЃР»СЊ","date":"РїСЏС‚РЅРёС†СЏ, 08.03.2024","time":"08:14","sortTime":1709878440},"types":[],"child":{"minDate":"2010-03-08","maxDate":"2024-03-07"},"allowStudent":0,"allowBooking":1,"isCis":0,"isEurope":0,"allowPrivilege":1,"noReserve":1},{"num":"091Рљ","category":0,"isTransformer":0,"travelTime":"7:36","from":{"code":"2200001","station":"РљРёС—РІ-РџР°СЃР°Р¶РёСЂСЃСЊРєРёР№","stationTrain":"РљРёС—РІ-РџР°СЃР°Р¶РёСЂСЃСЊРєРёР№","date":"С‡РµС‚РІРµСЂ, 07.03.2024","time":"22:57","sortTime":1709845020,"srcDate":"2024-03-07"},"to":{"code":"2218000","station":"Р›СЊРІС–РІ","stationTrain":"Р›СЊРІС–РІ","date":"РїСЏС‚РЅРёС†СЏ, 08.03.2024","time":"06:33","sortTime":1709872380},"types":[],"child":{"minDate":"2010-03-08","maxDate":"2024-03-07"},"allowStudent":0,"allowBooking":1,"isCis":0,"isEurope":0,"allowPrivilege":1,"noReserve":1},{"num":"149Рћ","category":0,"isTransformer":0,"travelTime":"7:31","from":{"code":"2200001","station":"РљРёС—РІ-РџР°СЃР°Р¶РёСЂСЃСЊРєРёР№","stationTrain":"РџРѕР»С‚Р°РІР°-РџС–РІРґРµРЅРЅР°","date":"С‡РµС‚РІРµСЂ, 07.03.2024","time":"23:19","sortTime":1709846340,"srcDate":"2024-03-07"},"to":{"code":"2218000","station":"Р›СЊРІС–РІ","stationTrain":"Р§РµСЂРЅС–РІС†С–","date":"РїСЏС‚РЅРёС†СЏ, 08.03.2024","time":"06:50","sortTime":1709873400},"types":[{"id":"Р›","title":"Р›СЋРєСЃ","letter":"Р›","places":2},{"id":"Рљ","title":"РљСѓРїРµ","letter":"Рљ","places":2}],"child":{"minDate":"2010-03-08","maxDate":"2024-03-07"},"allowStudent":0,"allowBooking":1,"isCis":0,"isEurope":0,"allowPrivilege":1,"noReserve":1},{"num":"130Рљ","category":0,"isTransformer":0,"travelTime":"7:31","from":{"code":"2200001","station":"РљРёС—РІ-РџР°СЃР°Р¶РёСЂСЃСЊРєРёР№","stationTrain":"РљСЂРµРјРµРЅС‡СѓРє","date":"С‡РµС‚РІРµСЂ, 07.03.2024","time":"23:19","sortTime":1709846340,"srcDate":"2024-03-07"},"to":{"code":"2218000","station":"Р›СЊРІС–РІ","stationTrain":"Р§РµСЂРЅС–РІС†С–","date":"РїСЏС‚РЅРёС†СЏ, 08.03.2024","time":"06:50","sortTime":1709873400},"types":[],"child":{"minDate":"2010-03-08","maxDate":"2024-03-07"},"allowStudent":0,"allowBooking":1,"isCis":0,"isEurope":0,"allowPrivilege":1,"noReserve":1}]}}'


def scrapy(from_station: int, to_station: int, date_at: datetime.date, time_at: datetime.time):
    logger.info(f'Task scrapping trains {from_station}->{to_station} at {date_at}')
    try:
        data_dict = {
            'from': from_station,
            'to': to_station,
            'date': date_at.strftime(DATE_FORMAT),
            'time': time_at.strftime(TIME_FORMAT),
            'get_tpl': '1',
            # 'url': 'train-list'
        }

        # HEADERS['Referer'] = MAIN_URL
        # url_with_params = urljoin(MAIN_URL, '?' + urlencode(data_dict))
        # response = requests.get(url_with_params, headers=HEADERS, )
        # response.raise_for_status()

        # sleep(randint(5, 10))

        # HEADERS['Referer'] = url_with_params
        # data_dict.pop('url')
        # data_dict['get_tpl'] = '1'
        # data_dict['captcha'] = CAPTCHA
        # response = requests.post(TRAIN_SEARCH_URL, data=data_dict, headers=HEADERS, cookies=cookies)
        # response.raise_for_status()
        #
        # data_json = json.loads(response.text)
        # if data_json.get('error'):
        # sleep(randint(10, 15))
        # data_dict['captcha'] = CAPTCHA
        # response = requests.post(TRAIN_SEARCH_URL, data=data_dict, headers=HEADERS, )
        # response.raise_for_status()
        # data_json = json.loads(response.text)

        response = requests.post(TRAIN_SEARCH_URL, data=data_dict, headers=HEADERS, )
        response.raise_for_status()
        data_json = json.loads(response.text)

        if data_json.get('error'):
            data_json = get_data_json_with_proxy(data_dict)

        data_json = json.loads(AAA)

        return scrapy_trains(data_json)
    except Exception as e:
        logger.error(f"Invalid scraping trains [{from_station}->{to_station} at {date_at}]: {e}")
        raise ValueError(f"Invalid scraping trains.")
    finally:
        logger.info(f'Task scrapping trains {from_station}->{to_station} at {date_at} finish')


def get_data_json_with_proxy(data_dict):
    data_json = ""
    for proxies in PROXIES:
        try:
            response = requests.post(TRAIN_SEARCH_URL, data=data_dict, headers=HEADERS, proxies=proxies)
            response.raise_for_status()
        except requests.exceptions:
            continue
        data_json = json.loads(response.text)
        if not data_json.get('error'):
            return data_json

    return data_json


def scrapy_trains(data_json: dict):
    if not data_json or data_json.get('error'):
        logger.warning(f'No data for scrapy.')
        return

    items = data_json['data']['list']

    trains = []
    for item in items:
        train = parse_train(item)
        if train:
            trains.append(train)

    return trains


def parse_train(item: dict):
    places = parse_places(item['types'])
    if not places:
        return None

    date_at = datetime.datetime.strptime(item['from']['srcDate'], DATE_FORMAT).date()
    time = datetime.datetime.strptime(item['from']['time'], TIME_FORMAT).time()

    return {
        'train': Train(
            num=item['num'],
            category=int(item['category']),
            date_at=date_at,
            time_at=time, ),
        'places': places
    }


def parse_places(items: list[dict]):
    return [
        Place(
            letter=item['letter'],
            title=item['title'],
            places=int(item['places']),
        )
        for item in items
    ]
