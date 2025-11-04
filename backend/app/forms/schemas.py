from pydantic import BaseModel, ConfigDict

class Forms(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    pass
