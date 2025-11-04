from fastapi import APIRouter, Depends, Query, HTTPException 
from typing import List, Optional

from backend.app.users.service import UserDAO
from backend.app.users.models import UserRole
from backend.app.users.rb import RBUser
from backend.app.users.schemas import SSUser, SSUserWithTasks, SSUser_Add, User_Update


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