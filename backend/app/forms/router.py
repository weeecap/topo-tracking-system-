from fastapi import APIRouter
from backend.app.forms.service import UserDAO

router = APIRouter(prefix='/users')

@router.get('/', summary='Получить пользователей')
async def get_users():
    return await UserDAO.get_users()

