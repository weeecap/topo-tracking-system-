from sqlalchemy import select
from sqlalchemy.orm import joinedload
from typing import Optional

from backend.app.dao.base import BaseDAO
from backend.app.models import User 
from backend.app.database import async_session_maker
from backend.app.users.schemas import SSUserWithTasks

class UserDAO(BaseDAO):
    model = User

    @classmethod 
    async def find_task_data(cls, user_id:int) -> Optional[SSUserWithTasks]:
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .options
                (joinedload(cls.model.assigned_tasks),
                 joinedload(cls.model.created_tasks))
                 .filter_by(id=user_id))
            result = await session.execute(query)
            user = result.unique().scalar_one_or_none()

            if not user:
                return None 
            
            user_with_tasks = SSUserWithTasks.model_validate(user)
            return user_with_tasks
        


        
    