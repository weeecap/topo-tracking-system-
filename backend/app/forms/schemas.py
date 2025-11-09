from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class Forms(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    form_id:Optional[int] = None
    title:str  = Field(..., min_length=10, max_length=252)
    content:Optional[str] = None

class Form_Add(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    form_id:int = Field(exclude=True)
    title:str  = Field(..., min_length=10, max_length=252)
    content:Optional[str] = None

class Form_Update(BaseModel):
    model_config=ConfigDict(from_attributes=True)

    form_id:Optional[int] = None
    title:str  = Field(..., min_length=10, max_length=252)
    content:Optional[str] = None
