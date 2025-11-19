from pathlib import Path
from dotenv import load_dotenv
import os

env_path = Path(__file__).resolve().parent.parent / ".env.local"
load_dotenv(env_path, override=True)  

class Settings:
    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = int(os.getenv('DB_PORT', 5432))
    DB_NAME: str = os.getenv('DB_NAME') #type: ignore
    DB_USER: str = os.getenv('DB_USER') #type: ignore
    DB_PASSWORD: str = os.getenv('DB_PASSWORD') #type: ignore
    SECRET_KEY: str = os.getenv('SECRET_KEY') #type: ignore
    ALGORITHM:str = os.getenv('ALGORITHM') #type: ignore

settings = Settings()

def get_db_url():
    return (f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@"
            f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")

def get_auth_data():
    return {'secret_key':settings.SECRET_KEY, 'algorithm':settings.ALGORITHM}