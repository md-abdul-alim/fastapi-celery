from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# Define the CeleryTask model inside `main.py` or import it from another file
from sqlalchemy import Column, Integer, String, DateTime, JSON
from datetime import datetime

# Database configuration
DATABASE_URL = "postgresql://postgres:1234@localhost/ct"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Create the FastAPI app
app = FastAPI()

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class CeleryTask(Base):
    __tablename__ = 'celery_tasks'

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String, unique=True, index=True, nullable=True)
    task = Column(JSON, nullable=False)
    status = Column(String, nullable=True)
    result = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.now)

# Create the tables in the PostgreSQL database
Base.metadata.create_all(bind=engine)


# Pydantic model for the request body
class CeleryTaskCreate(BaseModel):
    task: dict = Field(..., description="Task details, required")  # Mandatory field
    # task_id: str = Field(None, description="Optional task ID")
    # status: str = Field(None, description="Optional task status")
    # result: str = Field(None, description="Optional task result")

    class Config:
        from_attributes = True


# POST API to create a new CeleryTask
@app.post("/tasks/create", response_model=CeleryTaskCreate)
def create_celery_task(task_data: CeleryTaskCreate, db: Session = Depends(get_db)):
    """
    API endpoint: 127.0.0.1:8000/tasks/create
    update IP/domain based on hosting
    """
    # Create an instance of the CeleryTask model
    db_task = CeleryTask(
        task=task_data.task,
        # task_id=task_data.task_id,
        # status=task_data.status,
        # result=task_data.result,
    )

    # Add the task to the session
    db.add(db_task)
    db.commit()
    db.refresh(db_task)  # Refresh the instance with the new data from the database

    return db_task