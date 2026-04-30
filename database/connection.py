import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

# .env dan ma'lumotlarni olish (main.py da load_dotenv() qilinadi)
def get_engine():
    db_url = f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    return create_async_engine(db_url, echo=False)

def get_sessionmaker(engine):
    return async_sessionmaker(engine, expire_on_commit=False)