from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional

from backend.app.tasks.schemas import Task

class SSUser(BaseModel):
    model_config=ConfigDict(from_attributes=True, extra='ignore')

    id:int
    name:str = Field(...,min_length=1, max_length=50, description='Имя сотрудника')
    surname:str = Field(...,min_length=1, max_length=50, description='Фамилия сотрудника')
    role:str = Field(...,min_length=1,max_length=50, description='Должность')
    password:str = Field(exclude=True)

class SSUser_Add(BaseModel):
    model_config=ConfigDict(from_attributes=True)

    id:int
    name:str = Field(..., min_length=1, max_length=50, description='Имя сотрудника' )
    surname:str = Field(...,min_length=1, max_length=50, description='Фамилия сотрудника')
    role:str = Field(...,min_length=1,max_length=50, description='Должность')
    password:str

class User_Update(BaseModel):
    model_config=ConfigDict(from_attributes=True)

    name:Optional[str] = Field(None, min_length=1, max_length=50)
    surname:Optional[str] = Field(None ,min_length=1, max_length=50)
    role:Optional[str] = Field(None ,min_length=1,max_length=50)
    password:Optional[str]

class SSUserWithTasks(SSUser):

    assigned_tasks: List[Task] = []
    created_tasks: List[Task] = []

class Registration(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id:int
    name:str = Field(...,min_length=1, max_length=50, description='Имя сотрудника')
    surname:str = Field(...,min_length=1, max_length=50, description='Фамилия сотрудника')
    role:str = Field(...,min_length=1,max_length=50, description='Должность')
    password:str = Field(...,min_length=5, max_length=20, description='Пароль, не менее 5 символов')

class SSAuth(BaseModel):

    name:str = Field(...,description ='Имя сотрудника')
    surname:str = Field(...,description ='Фамилия сотрудника')
    password:str = Field(...,min_length=5, max_length=20, description='Пароль, не менее 5 символов')



