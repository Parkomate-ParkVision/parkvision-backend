from celery import Celery
from celery import shared_task
from django.conf import settings
import os
from datetime import timedelta, time

from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('django_template', )
app = Celery('tasks', broker=settings.CELERY_BROKER_URL, backend='rpc://')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'run-every-afternoon': {
        'task': 'vehicle.tasks.send_number_plate_verification_email',
        'schedule': crontab(minute=0, hour=0),
        'args': (),
        'options': {
            'expires': 20,
        },
    },
    'run-every-month-1st': {
        'task': 'vehicle.tasks.send_dashboard_email',
        'schedule': crontab(minute=1, hour=0, day_of_month=4),
        'args': (),
        'options': {
            'expires': 20,
        },
    },
}



@shared_task
def debug_task(self):
    print("done")
