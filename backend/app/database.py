from datetime import datetime
from typing import Annotated

from sqlalchemy import func 
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncAttrs
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase, mapped_column

from backend.app.config import get_db_url

DATABASE_URL = get_db_url()

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

#annotations 
int_pk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]

def import_all_models():

    import backend.app.users.models 
    import backend.app.forms.models

    import backend.app.tasks.models
    import backend.app.auth.models

class Base(AsyncAttrs, DeclarativeBase):
    pass

Base = declarative_base()
import_all_models()