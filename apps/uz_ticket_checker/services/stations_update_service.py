from apps.uz_ticket_checker.tasks import run_stations_scraping_task

UKRAINIAN_ALPHABET = ['А', 'Б', 'В', 'Г', 'Ґ', 'Д', 'Е', 'Є', 'Ж', 'З', 'И', 'І', 'Ї', 'Й', 'К', 'Л', 'М', 'Н', 'О',
                      'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ь', 'Ю', 'Я']


def run_all_stations_update():
    run_stations_scraping_task.delay(phrase="ГОРО")
    # for letter1 in UKRAINIAN_ALPHABET:
    #     for letter2 in UKRAINIAN_ALPHABET:
    #         run_stations_scraping_task.delay(phrase=letter1+letter2)
