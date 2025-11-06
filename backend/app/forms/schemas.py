from pydantic import BaseModel, ConfigDict
from typing import Optional

class Forms(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    form_id:int
    title:str
    content:Optional[str]
