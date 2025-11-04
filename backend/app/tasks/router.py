from fastapi import APIRouter, Depends, Query, HTTPException 
from typing import List, Optional
from datetime import datetime

from backend.app.tasks.schemas import SSTask, SSUpdateTask
from backend.app.tasks.service import TaskDAO
from backend.app.tasks.rb import RBTask

router = APIRouter(prefix='/tasks')

async def get_tasks_filter(
        title:Optional[str] = Query(None),
        content: Optional[str] = Query(None),
        status: Optional[str] = Query(None),
        priority: Optional[int] = Query(None),
        assignee_id: Optional[int] = Query(None),
        created_by_id: Optional[int] = Query(None),
        form_id: Optional[int] = Query(None),
        due_date: Optional[datetime] = Query(None),
        created_at: Optional[datetime] = Query(None)
    ) -> RBTask:
        
        return RBTask(title=title, 
                      content=content, 
                      status=status, 
                      priority=priority,
                      assignee_id=assignee_id,
                      created_by_id=created_by_id,
                      form_id=form_id,
                      due_date=due_date,
                      created_at=created_at)

@router.get('/', response_model=List[SSTask])
async def get_tasks(request_body:RBTask=Depends(get_tasks_filter)) -> List[SSTask]:
        tasks = await TaskDAO.find_all(**request_body.to_dict())
        return [SSTask.model_validate(task) for task in tasks]

@router.post('/add/')
async def add_task(task:SSTask) -> dict:
        task_data = task.model_dump()

        for field in ['due_date', 'created_at']:
                if field in task_data and task_data[field] is not None:
                        if isinstance(task_data[field], datetime) and task_data[field].tzinfo is not None:
                                task_data[field] = task_data[field].replace(tzinfo=None)

        check = await TaskDAO.add_data(**task_data)

        if check:
                return {'message': 'Задача добавлена'}
        else:
                return  {'message': 'Ошибка при добавлении задачи'}
        
@router.delete('/delete/')
async def delete_task(task_id:int) -> dict:
        check = await TaskDAO.delete_data(id=task_id)

        if check:
                return {'message': 'Задача удалена'}
        else:
                return  {'message': 'Ошибка при удалении задачи'}
        
      
@router.put('/update/')
async def update_user_data(id:int, update_data:SSUpdateTask) -> dict:
      filter_by = {'id':id}
      update_values = {k: v for k, v in update_data.model_dump().items() if v is not None}

      if not update_values:
            raise HTTPException(status_code=400, detail='No data provided for update')
      
      data =  await TaskDAO.update_data(filter_by, **update_values)

      if data == 0:
            raise HTTPException(status_code=400, detail='Task not found')
      
      return {"status": "success", "updated_fields": list(update_values.keys())}
                
        
        

