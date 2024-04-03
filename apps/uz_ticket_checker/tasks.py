from datetime import timedelta, datetime

from django.utils import timezone
from loguru import logger

from apps.celery import celery_app as app
from apps.common.constants import UKRAINIAN_ALPHABET
from apps.uz_ticket_checker.models import Station, Country
from apps.uz_ticket_checker.parsers.stations_parser import handle_one_phrase_stations
from apps.uz_ticket_checker.parsers.trains_parser import get_current_search_tickets


@app.task(name='run_tickets_search')
def run_tickets_search_task(**kwargs):
    from_station = kwargs.get('from_station')
    to_station = kwargs.get('to_station')
    from_date = kwargs.get('from_date')
    to_date = kwargs.get('to_date')

    dates_result = {}
    search_direction_text = ""
    search_dates_text = ""

    start_date = datetime.strptime(from_date, "%Y-%m-%d")
    end_date = datetime.strptime(to_date, "%Y-%m-%d")

    current_date = start_date
    while current_date <= end_date:
        current_search_results, current_search_direction = (
            get_current_search_tickets(from_station, to_station, current_date.strftime("%Y-%m-%d")))

        if current_search_results in ["no_trains_error", "proizd_ua_service_error", "proizd_ua_price_details_error"]:
            logger.error(current_search_results)
            return {
                'dates_result': current_search_results,
                'search_direction_text': current_search_direction,
                'search_dates_text': ""
            }
        elif len(current_search_results) != 0:
            date = current_search_results[0]['departure_date']
            rowspan_counter = 0
            if date in dates_result:
                for result in current_search_results:
                    rowspan_counter += result['rowspan']
                dates_result[date][0] += current_search_results
                dates_result[date][1] += rowspan_counter
            else:
                link = f"https://proizd.ua/search?fromId={from_station}&toId={to_station}&date={date}"
                for result in current_search_results:
                    rowspan_counter += result['rowspan']
                dates_result[date] = [current_search_results, rowspan_counter, link]

            if not search_direction_text:
                search_direction_text = current_search_direction
                if start_date == end_date:
                    search_dates_text += f" ({start_date.strftime("%Y-%m-%d")})"
                else:
                    search_dates_text += f" ({start_date.strftime("%Y-%m-%d")} - {end_date.strftime("%Y-%m-%d")})"
        current_date += timedelta(days=1)

    final_result = {
        'dates_result': dates_result,
        'search_direction_text': search_direction_text,
        'search_dates_text': search_dates_text
    }
    return final_result


@app.task(name='run_stations_scraping')
def run_stations_scraping_task(**kwargs):
    phrase = kwargs.get('phrase')
    stations_data = handle_one_phrase_stations(phrase)
    if len(stations_data) == 10:
        for letter in UKRAINIAN_ALPHABET:
            run_stations_scraping_task.delay(phrase=phrase + letter)
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
