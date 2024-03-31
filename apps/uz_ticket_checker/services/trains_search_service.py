from datetime import timedelta, datetime

from loguru import logger

from apps.uz_ticket_checker.parsers.trains_parser import get_all_train_numbers_by_date, get_current_search_tickets
from apps.uz_ticket_checker.parsers.trains_parser import get_checker_matches_by_train_number
from apps.uz_ticket_checker.tasks import run_tickets_search_task


def get_search_result_tickets(from_station, to_station, from_date, to_date):
    dates_result = {}
    search_summary = []

    start_date = datetime.strptime(from_date, "%Y-%m-%d")
    end_date = datetime.strptime(to_date, "%Y-%m-%d")

    current_date = start_date
    while current_date <= end_date:
        current_search_results, search_direction = (
            get_current_search_tickets(from_station, to_station, current_date.strftime("%Y-%m-%d")))

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

        if not search_summary:
            search_summary = search_direction
        current_date += timedelta(days=1)

    if start_date == end_date:
        search_summary += f" ({start_date.strftime("%Y-%m-%d")})"
    else:
        search_summary += f" ({start_date.strftime("%Y-%m-%d")} - {end_date.strftime("%Y-%m-%d")})"

    return dates_result, search_summary
    # return run_tickets_search_task.delay(
    #     from_station=from_station, to_station=to_station, from_date=from_date, to_date=to_date)


def get_checker_matches(train_checker_info):
    start_date = datetime.strptime(train_checker_info['start_date'], "%Y-%m-%d")
    end_date = datetime.strptime(train_checker_info['end_date'], "%Y-%m-%d")

    tickets_matches = []
    current_date = start_date
    while current_date <= end_date:
        # if train_checker_info['train_number'] is None:
        if len(train_checker_info['train_number']) == 0:
            train_numbers = get_all_train_numbers_by_date(
                train_checker_info['departure_station'],
                train_checker_info['arrival_station'],
                current_date.strftime("%Y-%m-%d")
            )
            for train_number in train_numbers:
                tickets_matches += get_checker_matches_by_train_number(train_checker_info, current_date, train_number)
        else:
            for train_number in train_checker_info['train_number']:
                tickets_matches += get_checker_matches_by_train_number(train_checker_info, current_date, train_number)
        current_date += timedelta(days=1)
    return tickets_matches
