import logging

from django.utils import timezone

from apps.accounts.models import User
from apps.accounts.tasks import send_email_checker_result_msg
from apps.celery import celery_app as app
from apps.common.tasks import BaseTaskWithRetry
from apps.tickets_ua.models import BaseSearchParameter, Station
from apps.tickets_ua.scrapers.bus import BusScraper
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
    logger.info(f'Run tickets_ua checkers [{ids}]')
    if not ids or len(ids) == 0:
        return

    for search_parameter in BaseSearchParameter.objects.filter(id__in=ids, is_active=True):
        if search_parameter.date_at < timezone.now().date():
            if search_parameter.is_active or search_parameter.is_available:
                search_parameter.updated_at = timezone.now()
                search_parameter.is_available = False
                search_parameter.is_active = False
                search_parameter.save(update_fields=['updated_at', 'is_available', 'is_active'])
            continue

        data = {
            'from_station': search_parameter.from_station.code,
            'to_station': search_parameter.to_station.code,
            'date_at': search_parameter.date_at,
            'time_at': search_parameter.time_at,
        }

        train_scraper = TrainScraper(**data)
        trains = train_scraper.scrapy_items

        buses = []
        if len(search_parameter.from_station.bus_name) > 0 and len(search_parameter.to_station.bus_name) > 0:
            data['from_station'] = search_parameter.from_station.bus_name
            data['to_station'] = search_parameter.to_station.bus_name
            bus_scraper = BusScraper(**data)
            buses = bus_scraper.scraper_items

        search_parameter.updated_at = timezone.now()
        search_parameter.is_available = len(trains) > 0
        search_parameter.save(update_fields=['updated_at', 'is_available'])

        if len(trains) > 0 or len(buses) > 0:
            user = User.objects.get(checker_tasks__task_param__ticket_ua_search_parameters__id=search_parameter.id)
            msg = get_result_message(search_parameter, trains, buses)
            if user.is_email_verified:
                send_email_checker_result_msg.apply_async(args=(user.id, msg,))
            if user.personal_setting and user.personal_setting.telegram_user_id:
                # TODO telegram send message
                ...


def get_result_message(search_parameter: BaseSearchParameter, trains, buses):
    from_station = search_parameter.from_station.name
    to_station = search_parameter.to_station.name
    date_at = search_parameter.date_at
    msg = f"{from_station}-{to_station} at {date_at} available"
    if len(trains) > 0:
        msg += f" by trains: {len(trains)} ticket(s)"
    if len(buses) > 0:
        msg += ' and' if len(trains) > 0 else ''
        msg += f" by buses: {len(buses)} ticket(s)"

    msg += f" check in ticket.ua"
    return msg
