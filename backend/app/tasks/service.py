from backend.app.dao.base import BaseDAO
from backend.app.models import Task

class TaskDAO(BaseDAO):
    model = Task