# test_db_connection.py
import asyncio
import asyncpg
import os
from dotenv import load_dotenv
from pathlib import Path


load_dotenv()

async def test_connection():
    env_path = Path(__file__).resolve().parent.parent.parent / ".env.local"
    DB_HOST = os.getenv('DB_HOST')
    print(f"Testing connection to: {DB_HOST}")
    
    try:
        # Parse the URL to extract components
        if DB_HOST.startswith('postgresql+asyncpg://'):
            db_url = DB_HOST.replace('postgresql+asyncpg://', 'postgresql://')
        else:
            db_url = DB_HOST
            
        conn = await asyncpg.connect(db_url)
        print("✅ Database connection successful!")
        
        # Test a simple query
        version = await conn.fetchval('SELECT version();')
        print(f"Database version: {version}")
        
        await conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_connection())