from celery import Task


class BaseTaskWithRetry(Task):
    autoretry_for = (Exception,)
    max_retries = 3
    retry_backoff = True
    retry_backoff_max = 300
    retry_jitter = False
