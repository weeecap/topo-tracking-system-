from fastapi import APIRouter, Depends, Query, HTTPException, Response, status
from typing import List, Optional

from backend.app.users.service import UserDAO
from backend.app.users.models import UserRole
from backend.app.users.rb import RBUser
from backend.app.users.auth import authentification_user, create_acces_token, get_password_hash
from backend.app.users.schemas import Registration, SSAuth, SSUser, SSUser_Add, SSUserWithTasks, User_Update



router = APIRouter(prefix='/users')

async def get_users_filter(
        name: Optional[str] = Query(None),
        surname: Optional[str] = Query(None),
        role: Optional[UserRole] = Query(None)
    ) -> RBUser:
        return RBUser(name=name, surname=surname, role=role)


@router.get('/', response_model=List[SSUser])
async def get_users(request_body:RBUser=Depends(get_users_filter)) -> List[SSUser]:
        users = await UserDAO.find_all(**request_body.to_dict())
        return [SSUser.model_validate(user) for user in users]

@router.get('/{id}', response_model=SSUser)
async def get_user_by_id(id: int) -> SSUser:
    user = await UserDAO.find_by_id(data_id=id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return SSUser.model_validate(user)

@router.get('/{id}/tasks')
async def get_users_tasks(id:int) -> SSUserWithTasks:
      tasks = await UserDAO.find_task_data(user_id=id)
      if not tasks:
            raise HTTPException(status_code=404, detail="No tasks found")
      return tasks

@router.post('/add/')
async def add_user(user:SSUser_Add) -> dict:
      check = await UserDAO.add_data(**user.model_dump())
      if check:
            return {'messagee':'Пользователь добавлен'}
      else:
            return {'messagee':'Ошибка при добавлении пользователя'}
      
@router.delete('/delete/')
async def delete_user(user_id:int) -> dict:
      check = await UserDAO.delete_data(id=user_id)
      if check:
            return {'messagee':'Пользовательские данные удалены'}
      else:
            return {'messagee':'Ошибка удалении'}
      
@router.put('/update/')
async def update_user_data(id:int, update_data:User_Update) -> dict:
      filter_by = {'id':id}
      update_values = {k: v for k, v in update_data.model_dump().items() if v is not None}

      if not update_values:
            raise HTTPException(status_code=400, detail='No data provided for update')
      
      data =  await UserDAO.update_data(filter_by, **update_values)

      if data == 0:
            raise HTTPException(status_code=400, detail='User not found')
      
      return {"status": "success", "updated_fields": list(update_values.keys())}

@router.post("/register")
async def register(user_data:Registration) -> dict:
    user = await UserDAO.original_user(name=user_data.name, surname=user_data.surname)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Такой пользователь уже зарегестирован')
    user_dict = user_data.model_dump()
    user_dict['password'] = get_password_hash(user_data.password)
    await UserDAO.add_data(**user_dict)
    return {'message':f'Регистрация прошла успешно'}

@router.post('/login')
async def auth_user(response:Response, user_data:SSAuth):
    check = await authentification_user(name=user_data.name, surname=user_data.surname, password=user_data.password)
    if check is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Неверные данные для входа в аккаунт')
    acces_token = create_acces_token({"sub": str(check.id)})
    response.set_cookie(key='user_access_token', value=acces_token, httponly=True)
    return {'acces_token': acces_token, 'refresh_token': None}