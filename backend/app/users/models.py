import enum
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Integer, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database import Base

if TYPE_CHECKING:
    from backend.app.tasks.models import Task

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