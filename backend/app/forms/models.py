from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database import Base

if TYPE_CHECKING:
    from backend.app.tasks.models import Task 

class Forms(Base):
    __tablename__ = 'forms'

    form_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[Optional[str]] = mapped_column(Text)

    # Relationship
    task: Mapped[Optional["Task"]] = relationship(
        "backend.app.tasks.models.Task", 
        back_populates='form', 
        uselist=False
    )
    #TODO: create relations 