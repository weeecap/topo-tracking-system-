from pathlib import Path
from dotenv import load_dotenv
import os

env_path = Path(__file__).resolve().parent.parent.parent / ".env.local"
load_dotenv(env_path, override=True)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from .users.router import router as user_router
from .tasks.router import router as task_router
from .forms.router import router as forms_router

app = FastAPI (
    title = 'Мониторинг топографической документации',
    version='0.1'
)

env_path = Path(__file__).resolve().parent.parent.parent / ".env.local"
load_dotenv(env_path, override=True)

origins_str = os.getenv('origins')
origins = [origin.strip() for origin in origins_str.split(',')] if origins_str else []

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix='')
app.include_router(task_router, prefix='')
app.include_router(forms_router, prefix='')

from fastapi import APIRouter
router = APIRouter()

@router.get("/debug-db-url")
async def debug():
    from config import settings, get_db_url   # ← adjust import to your real settings path
    return get_db_url


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