from sqlalchemy.future import select 
from sqlalchemy.orm import DeclarativeBase
from typing import Optional

from backend.app.database import async_session_maker

class BaseDAO:
    model = None  

    @classmethod
    async def find_all(cls, **filter_by):
        if cls.model is None:
            raise ValueError("Model is not defined for this DAO")
            
        async with async_session_maker() as session:
            query = select(cls.model)
            for key, value in filter_by.items():
                query = query.where(getattr(cls.model, key) == value)
            result = await session.execute(query)
            return result.scalars().all()
        
    @classmethod
    async def find_by_id(cls, data_id:int):
        if cls.model is None:
            raise ValueError("Model is not defined for this DAO")
        
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=data_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()
