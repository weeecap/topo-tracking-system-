import enum
from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Integer, DateTime, Text, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database import Base

if TYPE_CHECKING:
    from backend.app.users.models import User
    from backend.app.forms.models import Forms



class TaskStatus(str, enum.Enum):
    TODO = "TODO" 
    in_progress = "В работе"
    review = 'В проверке'
    done = 'Выполнено'


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus), default=TaskStatus.TODO)
    priority: Mapped[int] = mapped_column(Integer, default=1)
    assignee_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('users.id'))
    created_by_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('users.id'))
    form_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('forms.form_id'))
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
        foreign_keys=[form_id],
        back_populates='task'
    )
