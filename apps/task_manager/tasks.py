import time
from contextlib import contextmanager
from datetime import timedelta

from celery import group, chord
from celery.utils.log import get_task_logger
from django.core.cache import cache
from django.utils import timezone

from apps.celery import celery_app as app
from apps.common.constants import LOCK_EXPIRE_DEFAULT, RUN_ALL_CHECKER_INTERVAL_DEFAULT, \
    RUN_VIP_CHECKER_INTERVAL_DEFAULT, RUN_UZ_TICKET_CELERY_BEAT_INTERVAL_DEFAULT
from apps.common.constants import TIME_SLEEP_DEFAULT
from apps.hotline_ua.tasks import run_checkers as hotline_ua_checkers
from apps.task_manager.models import CheckerTask
from apps.tickets_ua.tasks import run_checkers as tickets_ua_checkers

celery_logger = get_task_logger(__name__)

app.conf.beat_schedule = {
    'run_task_with_interval': {
        'task': 'run_with_interval_all_checkers',
        "schedule": timedelta(seconds=RUN_ALL_CHECKER_INTERVAL_DEFAULT),
        'options': {'expires': TIME_SLEEP_DEFAULT},
    },
    'run_vip_task_with_interval': {
        'task': 'run_with_interval_vip_checkers',
        "schedule": timedelta(seconds=RUN_VIP_CHECKER_INTERVAL_DEFAULT),
        'options': {'expires': TIME_SLEEP_DEFAULT},
    },
    'run_uz_ticket_task_with_interval': {
        'task': 'run_with_interval_uz_ticket_checkers',
        "schedule": timedelta(seconds=RUN_UZ_TICKET_CELERY_BEAT_INTERVAL_DEFAULT),
    },
}


@app.task(name='run_vip_hotline_ua_checkers')
def run_hotline_ua_vip_checkers():
    ids = CheckerTask.objects.filter(
        is_active=True,
        is_delete=False,
        task_param__hotline_ua_search_parameters__is_active=True,
        user__personal_setting__isnull=False,
        user__personal_setting__is_vip=True,
    ).values('task_param__hotline_ua_search_parameters__id')
    hotline_ua_checkers(ids)


@app.task(name='run_tickets_ua_vip_checkers')
def run_tickets_ua_vip_checkers():
    # tasks = CheckerTask.objects.filter(task_param__ticket_ua_search_parameters__is_active=True)
    ids = CheckerTask.objects.filter(
        is_active=True,
        is_delete=False,
        task_param__ticket_ua_search_parameters__is_active=True,
        user__personal_setting__isnull=False,
        user__personal_setting__is_vip=True,
    ).values('task_param__ticket_ua_search_parameters__id')
    tickets_ua_checkers(ids)


@app.task(name='run_hotline_ua_checkers')
def run_hotline_ua_checkers():
    ids = CheckerTask.objects.filter(
        is_active=True,
        is_delete=False,
        task_param__hotline_ua_search_parameters__is_active=True,
    ).values('task_param__hotline_ua_search_parameters__id')
    hotline_ua_checkers(ids)


@app.task(name='run_tickets_ua_checkers')
def run_tickets_ua_checkers():
    # tasks = CheckerTask.objects.filter(task_param__ticket_ua_search_parameters__is_active=True)
    ids = CheckerTask.objects.filter(
        is_active=True,
        is_delete=False,
        task_param__ticket_ua_search_parameters__is_active=True,
    ).values('task_param__ticket_ua_search_parameters__id')
    tickets_ua_checkers(ids)


@app.task(name='update_checker_task')
def update_checker_task(*args):
    for checker in CheckerTask.objects.filter(
            is_active=True,
            is_delete=False,
            task_param__ticket_ua_search_parameters__is_active=True,
    ):
        checker.updated_at = timezone.now()
        checker.save(update_fields=('updated_at',))
    celery_logger.info(f"checker task updated")


@app.task(name='update_vip_checker_task')
def update_vip_checker_task(*args):
    for checker in CheckerTask.objects.filter(
            is_active=True,
            is_delete=False,
            task_param__ticket_ua_search_parameters__is_active=True,
            user__personal_setting__isnull=False,
            user__personal_setting__is_vip=True,
    ):
        checker.updated_at = timezone.now()
        checker.save(update_fields=('updated_at',))
    celery_logger.info(f"checker task updated")


@contextmanager
def memcache_lock(lock_id, oid):
    timeout_at = time.monotonic() + LOCK_EXPIRE_DEFAULT - 3
    status = cache.add(lock_id, oid, LOCK_EXPIRE_DEFAULT)
    try:
        yield status
    finally:
        if time.monotonic() < timeout_at and status:
            cache.delete(lock_id)


@app.task(name='run_with_interval_all_checkers', bind=True)
def run_with_interval_all_checkers(self):
    celery_logger.info(f"start")
    lock_id = 'run_with_interval_all_checkers_lock'
    with memcache_lock(lock_id, self.app.oid) as acquired:
        if acquired:
            tasks_group = group(
                run_hotline_ua_checkers.s(),
                run_tickets_ua_checkers.s()
            )
            chord(tasks_group)(update_checker_task.s())

            time.sleep(TIME_SLEEP_DEFAULT)
        else:
            celery_logger.warning(f"run with interval steel work")
    celery_logger.info(f"finish")


@app.task(name='run_with_interval_vip_checkers', bind=True)
def run_with_interval_vip_checkers(self):
    celery_logger.info(f"vip start")
    lock_id = 'run_with_interval_vip_checkers_lock'
    with memcache_lock(lock_id, self.app.oid) as acquired:
        if acquired:
            tasks_group = group(
                run_hotline_ua_vip_checkers.s(),
                run_tickets_ua_vip_checkers.s()
            )
            chord(tasks_group)(update_checker_task.s())

            time.sleep(TIME_SLEEP_DEFAULT)
        else:
            celery_logger.warning(f"vip run with interval steel work")
    celery_logger.info(f"vip finish")
