from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional

from backend.app.tasks.models import TaskStatus

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


class SSTask(BaseModel):
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

class SSUpdateTask(BaseModel):
    model_config=ConfigDict(from_attributes=True)

    title:Optional[str] = Field(None, min_length=1, max_length=50)
    content:Optional[str] = Field(None, min_length=1, max_length=1028)
    status:Optional[TaskStatus]
    priority: Optional[int] = Field(None, ge=1, le=5)
    assignee_id:Optional[int]
    form_id: Optional[int]
    due_date: Optional[datetime]










