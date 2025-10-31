from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional
import re 

class UserRegistration(BaseModel):
    user: str
    pswr: str 

class Task(BaseModel):
     pass

class Forms(BaseModel):
    pass

class SSUser(BaseModel):
    model_config=ConfigDict(from_attributes=True, extra='ignore')

    id:int
    name:str = Field(...,min_length=1, max_length=50, description='Имя сотрудника')
    surname:str = Field(...,min_length=1, max_length=50, description='Фамилия сотрудника')
    role:str = Field(...,min_length=1,max_length=50, description='Должность')
    hash_pswrd:str = Field(exclude=True)



