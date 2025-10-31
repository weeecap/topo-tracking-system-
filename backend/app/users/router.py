from fastapi import APIRouter, Depends, Query, HTTPException 
from backend.app.users.service import UserDAO
from backend.app.models import UserRole
from backend.app.users.rb import RBUser
from backend.app.users.schemas import SSUser, SSUserWithTasks
from typing import List, Optional


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