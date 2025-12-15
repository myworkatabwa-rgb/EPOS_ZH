# Z_pos/celery.py (project)
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Z_pos.settings')
app = Celery('Z_pos')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Schedule: run our management-command-wrapping task every 5 minutes
app.conf.beat_schedule = {
    'fetch_woocommerce_orders_every_5_min': {
        'task': 'zh_pos.run_fetch_orders_cmd',   # name from task decorator
        'schedule': crontab(minute='*/5'),
        'options': {'queue': 'default'},
    },
}
