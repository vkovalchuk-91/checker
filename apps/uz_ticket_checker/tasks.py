from datetime import timedelta, datetime

from django.utils import timezone

from apps.celery import celery_app as app
from apps.uz_ticket_checker.models import Station, Country
from apps.uz_ticket_checker.parsers.stations_parser import handle_one_phrase_stations
from apps.uz_ticket_checker.parsers.trains_parser import get_current_search_tickets


@app.task(name='run_tickets_search')
def run_tickets_search_task(**kwargs):
    from_station = kwargs.get('from_station')
    to_station = kwargs.get('to_station')
    from_date = kwargs.get('from_date')
    to_date = kwargs.get('to_date')
    search_results = []
    search_summary = []

    start_date = datetime.strptime(from_date, "%Y-%m-%d")
    end_date = datetime.strptime(to_date, "%Y-%m-%d")

    current_date = start_date
    while current_date <= end_date:
        current_search_results, search_direction = (
            get_current_search_tickets(from_station, to_station, current_date.strftime("%Y-%m-%d")))
        search_results += current_search_results
        if not search_summary:
            search_summary = search_direction
        current_date += timedelta(days=1)
    if start_date == end_date:
        search_summary += f" ({start_date.strftime("%Y-%m-%d")})"
    else:
        search_summary += f" ({start_date.strftime("%Y-%m-%d")} - {end_date.strftime("%Y-%m-%d")})"
    return search_results, search_summary


@app.task(name='run_stations_scraping')
def run_stations_scraping_task(**kwargs):
    UKRAINIAN_ALPHABET = ['А', 'Б', 'В', 'Г', 'Ґ', 'Д', 'Е', 'Є', 'Ж', 'З', 'И', 'І', 'Ї', 'Й', 'К', 'Л', 'М', 'Н', 'О',
                          'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ь', 'Ю', 'Я']
    phrase = kwargs.get('phrase')

    stations_data = handle_one_phrase_stations(phrase)
    if len(stations_data) == 10:
        for letter in UKRAINIAN_ALPHABET:
            run_stations_scraping_task.delay(phrase=phrase+letter)
    else:
        print(f"Додано в чергу задачу на оновлення станцій, що містять в назві '{phrase}'")
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
