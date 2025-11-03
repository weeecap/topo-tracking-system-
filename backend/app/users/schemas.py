from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional

from backend.app.tasks.schemas import Task

class UserRegistration(BaseModel):
    user: str
    pswr: str 

class Forms(BaseModel):
    pass

class SSUser(BaseModel):
    model_config=ConfigDict(from_attributes=True, extra='ignore')

    id:int
    name:str = Field(...,min_length=1, max_length=50, description='Имя сотрудника')
    surname:str = Field(...,min_length=1, max_length=50, description='Фамилия сотрудника')
    role:str = Field(...,min_length=1,max_length=50, description='Должность')
    hash_pswrd:str = Field(exclude=True)

class SSUser_Add(BaseModel):
    model_config=ConfigDict(from_attributes=True)

    id:int
    name:str = Field(..., min_length=1, max_length=50, description='Имя сотрудника' )
    name:str = Field(...,min_length=1, max_length=50, description='Имя сотрудника')
    surname:str = Field(...,min_length=1, max_length=50, description='Фамилия сотрудника')
    role:str = Field(...,min_length=1,max_length=50, description='Должность')
    hash_pswrd:str 
    


class SSUserWithTasks(SSUser):
    assigned_tasks: List[Task] = []
    created_tasks: List[Task] = []



