import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_api.settings')

app = Celery('shop_api')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "send_daily_report": {
        "task": "users.tasks.send_daily_report",
        "schedule": crontab(minute=30),  # каждый час в 30-й минуте
    },
    "clear_old_logs_daily": {
        "task": "users.tasks.clear_old_logs",
        "schedule": crontab(hour=3, minute=0),  # каждый день в 3:00 ночи
    },
}
