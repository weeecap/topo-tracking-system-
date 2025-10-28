from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .forms.router import router as router 

import uvicorn
import os

app = FastAPI (
    title = 'Мониторинг топографической документации',
    version='0.1'
)
app.include_router(router)
# app.include_router(auth.route, prefix='/api', tags=['Аутентификация'])

@app.get('/')
async def root():
    return {'Корень приложения мониторинга'}

if __name__ == '__main__':    
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("ENVIRONMENT") == "development"
    
    print(f" Запуск сервера на {host}:{port}")
    print(f" Документация: http://{host}:{port}/docs")
    print(f" Окружение: {os.getenv('ENVIRONMENT', 'development')}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )


# from fastapi import FastAPI
# from fastapi.responses import FileResponse
# from schemas import UserRegistration, Task, Forms

# app = FastAPI(
#     title='Мониторинг топографической документации',
#     version='0.1'
# )


# @app.get('/login')
# async def log(user: UserRegistration):
#     return {'message': 'User registration succesfully', 'user': user}

# @app.get('/tasks')
# async def tasks(tasks:Task):
#     # необходимо создать модель базы
#     # через алхимика, привязать конкретные таски 
#     # к конкретному исполнителю, начальник должен видеть всё
#     return None 

# @app.get('/forms')
# async def forms(forms:Forms):
#     # создать модель формуляра, связать её редактирование через онлайн ворд (предварительно написав его)
#     # предусмотреть редактирование, сохранение, ассайн 
#     # через алхимик
#     return None

# @app.get('/kanban')
# async def kanban():
#     # создать модель доски, связать её с текущими задачами 
#     # для каждого исполнителя, предусмотреть весь функционал
#     return None 

