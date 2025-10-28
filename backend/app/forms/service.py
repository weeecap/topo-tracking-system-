from sqlalchemy import select 
from backend.app.models import User 
from backend.app.database import async_session_maker

class UserDAO:
    @classmethod
    async def get_users(cls):
        async with async_session_maker() as session:
            query = select(User)
            result = await session.execute(query)
            users = result.scalar()
            return users