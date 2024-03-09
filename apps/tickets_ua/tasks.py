import logging

from django.db import transaction
from django.utils import timezone

from apps.celery import celery_app as app
from apps.tickets_ua.models import Checker, Station
from apps.tickets_ua.scrapers.station import scrapy as station_scrapy
from apps.tickets_ua.scrapers.train import scrapy as train_scrapy

DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H:%M'


@app.task(name='scraping_uz_stations')
def scraping_uz_stations(title: str):
    stations = station_scrapy(title)
    if stations:
        with transaction.atomic():
            for station in stations:
                if not Station.objects.filter(value=station.value).exists():
                    station.save()


@app.task(name='run_uz_checkers')
def run_checkers(id_list):
    for checker in Checker.objects.filter(id__in=id_list):
        trains = train_scrapy(
            from_station=checker.from_station.value,
            to_station=checker.to_station.value,
            date_at=checker.date_at,
            time_at=checker.time_at,
        )
        checker.updated_at = timezone.now()
        checker.is_available = len(trains) > 0
        checker.save(update_fields=['updated_at', 'is_available'])
        if trains:
            logging.info('Checker has results.')
