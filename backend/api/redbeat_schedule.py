from datetime import timedelta

from redbeat import RedBeatSchedulerEntry

from src.celery import app


def setup_redbeat_schedule():
    entry = RedBeatSchedulerEntry(
        name="check_tasks_deadline",
        task="api.tasks.check_tasks_deadline",
        schedule=timedelta(minutes=1),
        app=app,
    )
    entry.save()
