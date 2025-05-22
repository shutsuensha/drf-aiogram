import os

from celery import Celery

from config import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")

app = Celery("src")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.broker_url = settings.REDIS_URL_CELERY_BROKER
app.conf.result_backend = settings.REDIS_URL_CELERY_RESULT
app.conf.redbeat_redis_url = settings.REDIS_URL_CELERY_REDBEAT


app.conf.beat_scheduler = "redbeat.RedBeatScheduler"
app.conf.redbeat_lock_key = None
