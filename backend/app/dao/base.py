import sqlalchemy 
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

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
        
    @classmethod
    async def add_data(cls, **values):
        if cls.model is None:
            raise ValueError("Model is not defined")
        
        async with async_session_maker() as session:
            async with session.begin():                
                new_instance=cls.model(**values)
                session.add(new_instance)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return new_instance
            
    @classmethod
    async def delete_data(cls, delete_all: bool = False, **filter_by):
        if cls.model is None:
            raise ValueError("Model is not defined")
        
        if not delete_all and not filter_by:
            raise ValueError("Выбери хотя бы один пункт для удаления")
        
        async with async_session_maker() as session:
            async with session.begin():
                query = sqlalchemy.delete(cls.model)

                if not delete_all:
                    query=query.filter_by(**filter_by)
                
                result = await session.execute(query)
                count = getattr(result,'rowcount', None)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return count
    
    @classmethod
    async def update_data(cls, filter_by, **values):
        if cls.model is None:
            raise ValueError("Model is not defined")
        
        async with async_session_maker() as session:
            async with session.begin():
                query=(
                    sqlalchemy_update(cls.model)
                    .where (*[getattr(cls.model, k) == v for k, v in filter_by.items()])
                    .values(**values)
                    .execution_options(synchromized_session='fetch')
                ) 
                result = await session.execute(query)
                count = getattr(result,'rowcount', None)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return count


    
        
        

