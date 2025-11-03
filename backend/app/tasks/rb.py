from typing import Optional
from datetime import datetime

class RBTask:
    def __init__(self,
                  id:Optional[int] = None,
                  title:Optional[str] = None,
                  content:Optional[str] = None,
                  status:Optional[str] = None,
                  priority:Optional[int] = None,
                  assignee_id:Optional[int] = None,
                  created_by_id:Optional[int] = None,
                  form_id:Optional[int] = None,
                  due_date:Optional[datetime] = None,
                  created_at:Optional[datetime] = None
                  ) -> None:
        self.id = id
        self.title = title
        self.content = content
        self.status = status
        self.priority = priority
        self.assignee_id = assignee_id
        self.created_by_id = created_by_id
        self.form_id = form_id
        self.due_date = due_date
        self.created_at = created_at

    def to_dict(self) -> dict:
        data = {
            'id':self.id,
            'title':self.title,
            'content':self.content,
            'status':self.status,
            'priority':self.priority,
            'assignee_id':self.assignee_id,
            'created_by_id':self.created_at,
            'form_id':self.form_id,
            'due_date':self.due_date,
            'created_at':self.created_at
            }
        filtered = {key: value for key, value in data.items() if value is not None}
        return filtered