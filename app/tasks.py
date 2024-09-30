from celery_app import celery_app
import time

from main import CeleryTask, get_db
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


@celery_app.task(bind=True)
def run_process(self, a: int, b: int):
    result = a + b
    
    # Get a database session
    db = next(get_db())
    
    # Save the task result in the database
    save_task_to_db(self, 'SUCCESS', str(result), db)
    
    return result
