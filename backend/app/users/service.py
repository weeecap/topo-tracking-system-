from sqlalchemy import select 
from backend.app.users.dao.base import BaseDAO
from backend.app.models import User 
from backend.app.database import async_session_maker

class UserDAO(BaseDAO):
    model = User

        
    