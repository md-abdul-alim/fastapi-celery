from celery.schedules import crontab
from celery_app import celery_app

celery_app.conf.beat_schedule = {
    'say-hello-every-minute': {
        'task': 'app.tasks.run_process',
        'schedule': crontab(minute='*/1'),  # Execute every minute
    },
}
