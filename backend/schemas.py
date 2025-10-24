from pydantic import BaseModel

class UserRegistration(BaseModel):
    user: str
    pswr: str 

class Task(BaseModel):
    pass

class Forms(BaseModel):
    pass
