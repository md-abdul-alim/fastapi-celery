from celery import shared_task

from .main import CeleryTask, get_db
from celery import Task
from sqlalchemy.orm import Session

# Define a function to save task details in the database
def save_task_to_db(task: Task, status: str, result: str, db: Session):
    db_task = CeleryTask(
        task_id=task.request.id,
        status=status,
        result=result
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@shared_task
def run_process():
    # Task logic here
    return "Task completed"
