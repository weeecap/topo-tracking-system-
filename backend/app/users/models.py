import enum
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Integer, Enum, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database import Base
from backend.app.database import Base


if TYPE_CHECKING:
    from backend.app.tasks.models import Task

class UserRole(str, enum.Enum):
    cartographer = 'Картограф' 
    validator = 'Редактор'

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=False, nullable=False)
    surname: Mapped[str] = mapped_column(String(50), unique=False, nullable=False)
    role: Mapped[Optional[UserRole]] = mapped_column(Enum(UserRole), default=None)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    is_user:Mapped[bool] = mapped_column(default=True, server_default=text('true'), nullable=False)
    is_admin:Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    is_super_admin:Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)

    extend_existing = True


    # Relationships
    assigned_tasks: Mapped[Optional[List["Task"]]] = relationship(
        "Task", 
        foreign_keys="[Task.assignee_id]", 
        back_populates="assignee"
    )
    created_tasks: Mapped[Optional[List["Task"]]] = relationship(
        "Task", 
        foreign_keys="[Task.created_by_id]", 
        back_populates="creator"
    )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id})"
