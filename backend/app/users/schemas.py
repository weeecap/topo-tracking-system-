from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import List, Optional
from backend.app.models import TaskStatus

class UserRegistration(BaseModel):
    user: str
    pswr: str 

class Task(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id: int 
    title: str = Field(..., min_length=1, max_length=50, description='Название')
    content: str = Field(..., min_length=1, max_length=1028, description='Описание задачи')
    status: TaskStatus
    priority: int = Field(..., ge=1, le=5)
    assignee_id:Optional[int]
    created_by_id: Optional[int] 
    form_id: Optional[int]
    due_date: Optional[datetime]
    created_at: datetime



class Forms(BaseModel):
    pass

class SSUser(BaseModel):
    model_config=ConfigDict(from_attributes=True, extra='ignore')

    id:int
    name:str = Field(...,min_length=1, max_length=50, description='Имя сотрудника')
    surname:str = Field(...,min_length=1, max_length=50, description='Фамилия сотрудника')
    role:str = Field(...,min_length=1,max_length=50, description='Должность')
    hash_pswrd:str = Field(exclude=True)

class SSUserWithTasks(SSUser):
    assigned_tasks: List[Task] = []
    created_tasks: List[Task] = []



