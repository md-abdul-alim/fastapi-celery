from celery import Celery
from app.tasks import run_process

# Create Celery application
celery_app = Celery(
    'celery_app',
    broker='redis://localhost:6379/10',   # Redis as the broker
    backend='db+postgresql://postgres:1234@localhost/ct',  # PostgreSQL for task results
)

# Celery configuration
celery_app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    beat_schedule_filename='celerybeat-schedule',
    result_backend='db+postgresql://postgres:1234@localhost/ct',
    task_track_started=True,
    worker_max_tasks_per_child=100,  # For worker restarts after certain tasks
    task_acks_late=True,  # Only acknowledge tasks after completion
    result_expires=3600  # Results expire after 1 hour
)

# Celery Beat: Periodic task schedule

celery_app.conf.beat_schedule = {
    'check-chat-everyday-15-minutes': {
        'task': run_process,
        'schedule': 10.0,  # Run every 10 seconds
    },
}

# celery_app.conf.task_routes = {run_process: {'queue': 'default'}}
# print('----4----')

# # Load the task definitions
# celery_app.autodiscover_tasks([run_process])
# print('----5----')
# Load task modules from all registered Django apps.
celery_app.autodiscover_tasks()