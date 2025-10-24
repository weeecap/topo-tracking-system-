import enum
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship

Base = declarative_base()

class TaskStatus(str, enum.Enum):
    TODO = "TODO" 
    in_progress = "В работе"
    review = 'В проверке'
    done = 'Выполнено'

class UserRole(str, enum.Enum):
    cartographer = 'Картограф'
    validator = 'Редактор'

class User(Base):
    __tablename__ = 'Users' 

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String(50), nullable = False, unique= True)
    surname = Column(String(50), nullable = False, unique= True)
    role = Column(Enum(UserRole), default=None)
    hash_pswrd = Column(String(255), nullable = False)

    # relationships
    tasks = relationship("Task", back_populates="assignee")


class Forms(Base):
    __tablename__ = 'Forms'

    id = Column(Integer, primary_key=True, nullable=False, unique=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text)

    # relationships
    task = relationship("Task", back_populates='task')


class Task(Base):
    __tablename__ = 'Tasks'

    id = Column(Integer, primary_key=True, nullable=False, unique=True, index=True)
    title = Column(String, nullable = False)
    content = Column(Text)
    status = Column(Enum(TaskStatus), default=TaskStatus.TODO) 
    priority = Column(Integer, default = 1)
    assignee_id = Column(Integer, ForeignKey(User.id))
    created_by_id = Column(Integer, ForeignKey(User.id))
    due_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now()) 

    # relationships
    assignee = relationship("Users", foreign_keys=[assignee_id], back_populates='assigned_tasks')   
    creator = relationship("Users", foreign_keys=[created_by_id], back_populates='created_tasks')


    