import enum
from sqlalchemy import text, Enum
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.database import Base, int_pk

class Role_While_Auth(str, enum.Enum):
    cartographer = 'Картограф' 
    validator = 'Редактор'
    admin = 'Руководство'
    superuser = 'superuser'




class User_Auth(Base):
    __tablename__ = 'users_auth'

    id:Mapped[int_pk]
    name:Mapped[str]
    surname:Mapped[str]
    role:Mapped[Role_While_Auth]

    is_user:Mapped[bool] = mapped_column(default=True, server_default=text('true'), nullable=False)
    is_admin:Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    is_super_admin:Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)

    extend_existing = True

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id})"