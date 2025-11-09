from typing import Optional

class RBForms:
    def __init__(self,
                 form_id:Optional[int] = None,
                 title:Optional[str] = None,
                 content:Optional[str] = None) -> None:
        
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


