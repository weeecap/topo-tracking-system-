from typing import Optional

class RBUser:
    def __init__(self,
                id: Optional[int] = None,
                name: Optional[str] = None,
                surname: Optional[str] = None,
                role: Optional[str] = None,
                hash_pswrd: Optional[str] = None
            ) -> None:
        self.id=id
        self.name=name
        self.surname=surname
        self.role=role
        self.hash_pswrd=hash_pswrd

    def to_dict(self) -> dict:
        data = {'id':self.id, 
                'name':self.name,
                'surname':self.surname, 
                'role':self.role,
                'hash_pswrd':self.hash_pswrd}
        filtered = {key: value for key, value in data.items() if value is not None}
        return filtered
