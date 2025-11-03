from datetime import datetime, timezone
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import List, Optional

from backend.app.models import TaskStatus

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









