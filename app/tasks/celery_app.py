from celery import Celery
from celery.schedules import crontab

from app.config import settings

celery = Celery(
    "tasks",
    broker=settings.REDIS_URL,
    include=[
        "app.tasks.tasks",
        "app.tasks.scheduled"
    ],
)

celery.conf.beat_schedule = {
    "print_12345": {
        "task": "periodic_task",
        "schedule": 5, # seconds
        # "schedule": crontab(minute="0", hour="12")
    }
}
