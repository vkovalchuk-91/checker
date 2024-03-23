from django.utils import timezone

from apps.celery import celery_app as app
from apps.uz_ticket_checker.models import Station, Country
from apps.uz_ticket_checker.parsers.stations_parser import handle_one_phrase_stations


@app.task(name='run_stations_scraping')
def run_stations_scraping_task(**kwargs):
    phrase = kwargs.get('phrase')
    print(f"Додано в чергу задачу на оновлення станцій, що містять в назві '{phrase}'")
    stations_data = handle_one_phrase_stations(phrase)
    for station in stations_data:

        country_name = station['country']
        if country_name is None:
            country_name = "Unspecified"

        if country_name != 'Україна':
            station['is_active'] = False

        existing_country = Country.objects.filter(name=country_name).first()
        if existing_country:
            country = existing_country
        else:
            new_country = Country(name=country_name)
            new_country.save()
            country = new_country
        station['country'] = country

        station['updated_at'] = timezone.now

        Station.objects.update_or_create(express_3_id=station['express_3_id'], defaults=station)
        print(f"Додано/оновлено дані станції '{station['name']}'")
