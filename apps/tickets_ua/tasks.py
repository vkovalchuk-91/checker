import logging

from django.utils import timezone

from apps.accounts.models import User
from apps.accounts.tasks import send_email_checker_result_msg

from apps.celery import celery_app as app
from apps.common.enums.checker_name import CheckerTypeName
from apps.common.tasks import BaseTaskWithRetry
from apps.tickets_ua.models import BaseSearchParameter, Station
from apps.tickets_ua.scrapers.bus_station import BusStationScraper
from apps.tickets_ua.scrapers.train import TrainScraper
from apps.tickets_ua.scrapers.train_station import TrainStationScraper

DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H:%M'

logger = logging.getLogger('django')


@app.task(name='tickets_ua_scraping_train_stations', base=BaseTaskWithRetry)
def scraping_train_stations(title: str):
    scraper = TrainStationScraper(data=title)
    stations = scraper.scrapy_items
    if stations:
        for station in stations:
            if not Station.objects.filter(code=station.code).exists():
                station = Station.objects.create(
                    code=station.code,
                    name=station.name,
                    bus_name='',
                )
                scraping_bus_station_name.apply_async(args=(station.id,))


@app.task(name='tickets_ua_scraping_bus_station_name', base=BaseTaskWithRetry)
def scraping_bus_station_name(station_id: int):
    if not Station.objects.filter(id=station_id).exists():
        return ''

    station = Station.objects.get(id=station_id)
    scraper = BusStationScraper(data=station.name)
    bus_stations = scraper.scrapy_items
    if bus_stations:
        for bus_station in bus_stations:
            if bus_station.name.lower().startswith(station.name.lower()):
                station.bus_name = bus_station.code
                station.save(update_fields=['bus_name', ])
                return bus_station.code


@app.task(name='tickets_ua_run_checkers')
def run_checkers(ids):
    logger.info('Run tickets_ua checkers')
    if not ids or len(ids) == 0:
        return

    for checker in BaseSearchParameter.objects.filter(id__in=ids, is_active=True):
        if checker.date_at < timezone.now().date():
            if checker.is_available:
                checker.updated_at = timezone.now()
                checker.is_available = False
                checker.save(update_fields=['updated_at', 'is_available'])
            continue

        data = {
            'from_station': checker.from_station.code,
            'to_station': checker.to_station.code,
            'date_at': checker.date_at,
            'time_at': checker.time_at,
        }

        train_scraper = TrainScraper(**data)
        trains = train_scraper.scrapy_items

        # data['from_station'] = checker.from_station.bus_name
        # data['to_station'] = checker.to_station.bus_name
        # bus_scraper = BusScraper(**data)
        # buses = bus_scraper.scraper_items

        checker.updated_at = timezone.now()
        checker.is_available = len(trains) > 0
        checker.save(update_fields=['updated_at', 'is_available'])

        if len(trains) > 0:
            msg = f"have {len(trains)} train(s) by your check."
            user = User.objects.get(
                checker_tasks__checker_id=checker.id,
                checker_tasks__checker_type=CheckerTypeName.TICKETS_UA.value,
            )
            send_email_checker_result_msg.apply_async(args=(user.id, msg,))
