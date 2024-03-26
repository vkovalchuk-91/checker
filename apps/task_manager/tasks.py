from datetime import timedelta

from celery import Task

from apps.celery import celery_app as app


class BaseTaskWithRetry(Task):
    autoretry_for = (Exception,)
    max_retries = 3
    retry_backoff = True
    retry_backoff_max = 300
    retry_jitter = False


task_list = {
    "task1": "path.to.task1",
    "task2": "path.to.task2",
    # Add more tasks as needed
}

app.conf.beat_schedule = {
    "update_every_5_seconds": {
        "task": task_list,
        "schedule": timedelta(seconds=5),
    },
}


@app.task(base=BaseTaskWithRetry)
def aaa():
    ...