from fastapi import APIRouter, Depends, Query, HTTPException 
from typing import List, Optional
from datetime import datetime

from backend.app.forms.schemas import Forms
from backend.app.forms.service import FormsDAO
from backend.app.tasks.rb import RBTask

router = APIRouter(prefix='/forms')

@router.post('/add')
async def add_forms(form:Forms) -> dict:
    form_data = form.model_dump()
    check = await FormsDAO.add_data(**form_data)

    if check: 
        return {'message':'Формуляр добавлен'}
    else:
        return  {'message': 'Ошибка при добавлении формуляра'}




