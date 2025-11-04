from backend.app.dao.base import BaseDAO
from backend.app.tasks.models import Task

class TaskDAO(BaseDAO):
    model = Task