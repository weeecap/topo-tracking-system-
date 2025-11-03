import enum
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import String, Integer, DateTime, Text, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database import Base

class TaskStatus(str, enum.Enum):
    TODO = "TODO" 
    in_progress = "В работе"
    review = 'В проверке'
    done = 'Выполнено'

class UserRole(str, enum.Enum):
    cartographer = 'Картограф' 
    validator = 'Редактор'

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    surname: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    role: Mapped[Optional[UserRole]] = mapped_column(Enum(UserRole), default=None)
    hash_pswrd: Mapped[str] = mapped_column(String(255), nullable=False)

    # Relationships
    assigned_tasks: Mapped[List["Task"]] = relationship(
        "Task", 
        foreign_keys="[Task.assignee_id]", 
        back_populates="assignee"
    )
    created_tasks: Mapped[List["Task"]] = relationship(
        "Task", 
        foreign_keys="[Task.created_by_id]", 
        back_populates="creator"
    )

class Forms(Base):
    __tablename__ = 'forms'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[Optional[str]] = mapped_column(Text)

    # Relationship
    task: Mapped[Optional["Task"]] = relationship(
        "Task", 
        back_populates='form', 
        uselist=False
    )
    #TODO: create relations 

class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus), default=TaskStatus.TODO)
    priority: Mapped[int] = mapped_column(Integer, default=1)
    assignee_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('users.id'))
    created_by_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('users.id'))
    # form_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('forms.id'))
    due_date: Mapped[Optional[datetime]] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    # Relationships
    assignee: Mapped[Optional["User"]] = relationship(
        "User", 
        foreign_keys=[assignee_id], 
        back_populates='assigned_tasks'
    )   
    creator: Mapped[Optional["User"]] = relationship(
        "User", 
        foreign_keys=[created_by_id], 
        back_populates='created_tasks'
    )
    form: Mapped[Optional["Forms"]] = relationship(
        "Forms", 
        back_populates='task'
    )

