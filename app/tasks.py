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
    db = next(get_db())
    print('db: ', db)
    # Fetch all CeleryTask objects where task_id is NULL and status is False
    tasks_to_update = db.query(CeleryTask).filter(CeleryTask.status == False).all()

    # Iterate over each task and update the status to True
    for task in tasks_to_update:
        print("task.task: ", task.task)
        task.status = True
        db.add(task)  # Mark the task as modified

    # Commit all changes at once
    print('running')
    db.commit()
    return "Task completed"

# celery -A celery_app beat --loglevel=info

# celery -A celery_app worker --loglevel=info

# uvicorn app.main:app --reload
