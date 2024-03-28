import logging
from itertools import groupby

from celery import group

from apps.celery import celery_app as app
from apps.common.constants import RUN_CHECKER_INTERVAL_DEFAULT, EXPIRES_RUN_CHECKER_INTERVAL_DEFAULT
from apps.common.enums.checker_name import CheckerTypeName
from apps.hotline_ua.tasks import run_checkers as hotline_ua_checkers
from apps.task_manager.models import CheckerTask
from apps.tickets_ua.tasks import run_checkers as tickets_ua_checkers

logger = logging.getLogger('django')

#
# task_list = {
#     "task1": "path.to.task1",
#     "task2": "path.to.task2",
#     # Add more tasks as needed
# }
#
# app.conf.beat_schedule = {
#     "update_every_5_seconds": {
#         "task": task_list,
#         "schedule": timedelta(seconds=5),
#     },
# }

app.conf.beat_schedule = {
    'run_task_with_interval': {
        'task': 'run_with_interval_all_checkers',
        # 'task': 'tasks.check.run_with_interval_all_checkers',
        'schedule': RUN_CHECKER_INTERVAL_DEFAULT,
        'options': {'expires': EXPIRES_RUN_CHECKER_INTERVAL_DEFAULT},
    },
}


@app.task(name='run_with_interval_all_checkers')
def run_with_interval_all_checkers():
    logging.info(f"start")
    sorted_checker_tasks = sorted(CheckerTask.objects.all(), key=lambda x: x.checker_type)
    grouped_checker_tasks = groupby(sorted_checker_tasks, key=lambda x: x.checker_type)
    checker_tasks_dict = {checker_type: list(tasks) for checker_type, tasks in grouped_checker_tasks}

    hotline_ua_ids = get_checker_ids(checker_tasks_dict, CheckerTypeName.HOTLINE_UA.value)
    tickets_ua_ids = get_checker_ids(checker_tasks_dict, CheckerTypeName.TICKETS_UA.value)
    result = group(
        hotline_ua_checkers.s(hotline_ua_ids),
        tickets_ua_checkers.s(tickets_ua_ids),

    )
    result.apply_async(link_error=error_handler_task.s())


def get_checker_ids(checker_tasks_dict, checker_type):
    if checker_tasks_dict.get(checker_type):
        return [task.checker_id for task in checker_tasks_dict[checker_type]]
    else:
        return []


@app.task
def error_handler_task(request, exc, traceback):
    logging.error(f"Error occurred: {exc}")
