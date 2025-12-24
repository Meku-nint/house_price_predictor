import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prediction.settings')

app = Celery('prediction')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# SIMPLE 2-hour schedule
app.conf.beat_schedule = {
    'retrain-every-2-hours': {
        'task': 'predict.tasks.retrain_model',
        'schedule': 7200.0,  # 2 hours in seconds
    },
}