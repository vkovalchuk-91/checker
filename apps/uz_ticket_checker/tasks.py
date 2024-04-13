from datetime import timedelta, datetime

from celery.utils.log import get_task_logger
from django.core.cache import cache
from django.utils import timezone
from loguru import logger

from apps.celery import celery_app as app
from apps.common.constants import UKRAINIAN_ALPHABET, TG_MENUS_EXPIRE_TIME, TICKETS_MATCHES_CASH_EXPIRE_RATIO
from apps.task_manager.models import CheckerTask
from apps.tbot.handlers.send_uz_tickets_matches import send_tickets
from apps.uz_ticket_checker.models import Station, Country, TicketSearchParameter
from apps.uz_ticket_checker.parsers.stations_parser import handle_one_phrase_stations
from apps.uz_ticket_checker.parsers.trains_parser import get_current_search_tickets
from apps.uz_ticket_checker.services.checker_service import get_checker_matches_info_dict, get_checker_matches, \
    get_direction_info_str

celery_logger = get_task_logger(__name__)


@app.task(name='run_tickets_search')
def run_tickets_search_task(**kwargs):
    from_station = kwargs.get('from_station')
    to_station = kwargs.get('to_station')
    from_date = kwargs.get('from_date')
    to_date = kwargs.get('to_date')

    dates_result = {}
    search_direction_text = ""
    search_dates_text = ""
    no_trains_error_text = "no_trains_error"
    no_trains_error_description = "На даний момент на вказані дати відсутні квитки на потяги між вказаними станціями"

    start_date = datetime.strptime(from_date, "%Y-%m-%d")
    end_date = datetime.strptime(to_date, "%Y-%m-%d")

    current_date = start_date
    while current_date <= end_date:
        current_search_results, current_search_direction = (
            get_current_search_tickets(from_station, to_station, current_date.strftime("%Y-%m-%d")))

        if current_search_results in ["proizd_ua_service_error", "proizd_ua_price_details_error"]:
            logger.error(current_search_results)
            return {
                'dates_result': current_search_results,
                'search_direction_text': current_search_direction,
                'search_dates_text': ""
            }
        elif current_search_results != "no_trains_error":
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
                    search_dates_text += f" ({start_date.strftime('%Y-%m-%d')})"
                else:
                    search_dates_text += f" ({start_date.strftime('%Y-%m-%d')} - {end_date.strftime('%Y-%m-%d')})"
        current_date += timedelta(days=1)

    if dates_result:
        final_result = {
            'dates_result': dates_result,
            'search_direction_text': search_direction_text,
            'search_dates_text': search_dates_text
        }
    else:
        final_result = {
            'dates_result': no_trains_error_text,
            'search_direction_text': no_trains_error_description,
            'search_dates_text': ""
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


@app.task(name='run_with_interval_uz_ticket_checkers')
def run_with_interval_uz_ticket_checkers():
    celery_logger.info(f"uz_ticket_checkers_start")

    active_uz_ticket_checker_tasks = CheckerTask.objects.filter(
        is_active=True,
        is_delete=False,
        task_param__param_type__param_category_name="UZ Ticket Checker",
    ).all()
    counter = 0

    for active_uz_ticket_checker_task in active_uz_ticket_checker_tasks:
        last_update_time = active_uz_ticket_checker_task.updated_at
        update_period_minutes = active_uz_ticket_checker_task.update_period
        task_param_id = active_uz_ticket_checker_task.task_param.pk
        ticket_search_parameter = TicketSearchParameter.objects.filter(baseparameter_ptr_id=task_param_id).first()
        end_search_date = ticket_search_parameter.end_date.replace(hour=0, minute=0, second=0, microsecond=0)
        if end_search_date < timezone.now().replace(hour=0, minute=0, second=0, microsecond=0):
            active_uz_ticket_checker_task.is_delete = True
            active_uz_ticket_checker_task.updated_at = timezone.now()
            active_uz_ticket_checker_task.save()
        elif last_update_time + timedelta(minutes=update_period_minutes) <= timezone.now():
            checker_matches_info = get_checker_matches_info_dict(ticket_search_parameter)
            tg_id = active_uz_ticket_checker_task.user.personal_setting.telegram_user_id
            direction_info = get_direction_info_str(ticket_search_parameter)
            execute_and_update_checker_task.delay(checker_id=active_uz_ticket_checker_task.pk,
                                                  update_period=active_uz_ticket_checker_task.update_period,
                                                  tg_id=tg_id,
                                                  direction_info=direction_info,
                                                  checker_matches_info=checker_matches_info)
            counter += 1

    celery_logger.info(f"uz_ticket_checkers_finish updated {counter} checker(s)")


@app.task(name='execute_checker_task')
def execute_and_update_checker_task(**kwargs):
    checker_id = kwargs.get('checker_id')
    update_period = kwargs.get('update_period')
    tg_id = kwargs.get('tg_id')
    direction_info = kwargs.get('direction_info')
    checker_matches_info = kwargs.get('checker_matches_info')

    tickets_matches = get_checker_matches(checker_matches_info)
    cache_tickets_matches_info = cache.get(str(checker_id) + 'tickets_matches')
    cache.set(str(checker_id) + 'tickets_matches', tickets_matches, TICKETS_MATCHES_CASH_EXPIRE_RATIO * update_period)

    if cache_tickets_matches_info is None or cache_tickets_matches_info != tickets_matches:
        menu_dict = send_tickets(tg_id, checker_id, direction_info, tickets_matches)
        cache.set(checker_id, menu_dict, TG_MENUS_EXPIRE_TIME)
    else:
        logger.info(f"{direction_info} - оновлень не виявлено!")

    checker_task = CheckerTask.objects.filter(id=checker_id).first()
    checker_task.updated_at = timezone.now()
    checker_task.save()
