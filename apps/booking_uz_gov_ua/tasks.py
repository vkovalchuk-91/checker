from datetime import datetime

from django.db import transaction

from apps.booking_uz_gov_ua.models import Checker, Train, Station, Place
from apps.booking_uz_gov_ua.scrapers.train_selenium import TrainScraper

from apps.celery import celery_app as app
from apps.booking_uz_gov_ua.scrapers.station import scrapy as station_scrapy
from apps.booking_uz_gov_ua.scrapers.train import scrapy as train_scrapy

DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H:%M'


@app.task(name='scraping_uz_stations')
def scraping_uz_stations(title: str):
    # print(title)
    stations = station_scrapy(title)
    if stations:
        with transaction.atomic():
            for station in stations:
                if not Station.objects.filter(value=station.value).exists():
                    station.save()


@app.task(name='run_uz_checkers')
def run_checkers(id_list):
    # for checker in Checker.objects.filter(id__in=id_list):
    #     trains = train_scrapy(
    #         from_station=checker.from_station.value,
    #         to_station=checker.to_station.value,
    #         date_at=checker.date_at,
    #         time_at=checker.time_at,
    #     )
    #     try:
    #         update_checker(checker=Checker.objects.get(id=103), trains=trains)
    #     except Exception as e:
    #         print(e)
    scraper = TrainScraper()
    for checker in Checker.objects.filter(id__in=id_list):
        trains = scraper.scrapy(checker)
        try:
            update_checker(checker=Checker.objects.get(id=103), trains=trains)
        except Exception as e:
            print(e)


def update_checker(checker: Checker, trains: list[dict]):
    if not trains:
        return

    with transaction.atomic():
        new_trains = []
        for train_dict in trains:
            train = train_dict['train']
            places = train_dict['places']
            train.save()
            # places = Place.objects.bulk_create(places)
            train.places.set(Place.objects.bulk_create(places))

            new_trains.append(train)

        delete_places = Place.objects.filter(trains__in=checker.trains.all())
        delete_places.delete()

        # delete_trains = Train.objects.filter(id__in=[i['id'] for i in checker.trains.values()])
        delete_trains = Train.objects.filter(checkers=checker)
        delete_trains.delete()

        checker.trains.set(new_trains)
        checker.updated_at = datetime.now()
        checker.save()
