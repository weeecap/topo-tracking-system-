from datetime import date 
from pydantic import BaseModel, Field

class User(BaseModel):
    name: str
    surname:str 
    email:str = Field(...,alias='email_addres')
    birth_date: date 


oleg=User(name='Oleg',
          surname='Pidr',
          email_addres='lox@mail.ru',
          birth_date=date(year=2004, month=9, day=7))

to_dict=oleg.model_dump()
to_json=oleg.model_dump_json()

print(to_dict, type(to_dict))
print(to_json, type(to_json))