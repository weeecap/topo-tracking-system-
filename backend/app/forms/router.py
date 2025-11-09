from fastapi import APIRouter, Depends, Query, HTTPException 
from typing import Optional, List

from backend.app.forms.schemas import Forms, Form_Update, Form_Add
from backend.app.forms.service import FormsDAO
from backend.app.forms.rb import RBForms

router = APIRouter(prefix='/forms')

async def get_forms_filter(
    form_id: Optional[int] = Query(None),
    title: Optional[str] = Query(None),
    content: Optional[str] = Query(None)
) -> RBForms:
    return RBForms(form_id=form_id, title=title, content=content)

@router.get('/', response_model=Forms)
async def get_forms(request_body:RBForms=Depends(get_forms_filter)) -> List[Forms]:
    forms =  await FormsDAO.find_all(**request_body.to_dict())
    return [Forms.model_validate(form) for form in forms]

@router.get('/{id}', response_model=Forms)
async def get_forms_by_id(form_id:int) -> Forms:
    form = await FormsDAO.find_by_id(data_id=form_id)
    if not form:
        raise HTTPException(status_code=404, detail='Form not found')
    else:
        return Forms.model_validate(form)
    

@router.post('/add')
async def add_forms(form:Form_Add) -> dict:
    form_data = form.model_dump()
    check = await FormsDAO.add_data(**form_data)

    if check: 
        return {'message':'Формуляр добавлен'}
    else:
        return  {'message': 'Ошибка при добавлении формуляра'}
    
@router.delete('/delete')
async def delete_forms(form_id:int) -> dict:
    check = await FormsDAO.delete_data(id=form_id)

    if check:
        return {'messge':'Формуляр удален'}
    else:
        return {'message': 'Ошибка удаления'}
    
@router.put('/update')
async def update_form_data(update_data:Form_Update, id=int) -> dict:
    filter_by = {"id":id}
    update_values = {k: v for k, v in update_data.model_dump().items() if v is None}

    if not update_values:
        raise HTTPException(status_code=400, detail='No data provided for update')

    data = await FormsDAO.update_data(filter_by, **update_values)

    if data == 0:
        raise HTTPException(status_code=400, detail='Form not found')
    
    return {"status": "success", "updated_fields": list(update_values.keys())}