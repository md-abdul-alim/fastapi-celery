from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# Define the CeleryTask model inside `main.py` or import it from another file
from sqlalchemy import Column, Integer, String, DateTime
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
    task_id = Column(String, unique=True, index=True)
    status = Column(String)
    result = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Create the tables in the PostgreSQL database
Base.metadata.create_all(bind=engine)
