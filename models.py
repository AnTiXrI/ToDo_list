from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    priority = Column(String, nullable=False)
    done = Column(Boolean, default=False)

class TaskCreate(BaseModel):
    title: str
    priority: str

class TaskUpdate(BaseModel):
    title: str = None
    priority: str = None
    done: bool = None