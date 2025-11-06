from typing import Optional

class RBUser:
    def __init__(self,
                 form_id:int,
                 title:str,
                 content:Optional[str]) -> None:
        
        self.form_id=form_id
        self.title=title
        self.content=content

    def to_dict(self) -> dict:
        data = {
            'form_id':self.form_id,
            'title':self.title,
            'content':self.content
        }

        filtered = {key: value for key, value in data.items() if value is not None}
        return filtered


