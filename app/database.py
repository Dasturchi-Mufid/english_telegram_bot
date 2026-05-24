import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

# .env faylini yuklash
load_dotenv()

# Ma'lumotlar bazasi URL manzili
# Agar .env faylida biron narsa topilmasa, xatolikni oldini olish uchun default qiymat yoki tekshiruv
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

if not all([DB_USER, DB_PASS, DB_HOST, DB_NAME]):
    # Agar .env bo'sh bo'lsa, xatolikni aniq ko'rsatish
    raise ValueError("DB_USER, DB_PASS, DB_HOST yoki DB_NAME .env faylida topilmadi!")

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

# Engine va Session
engine = create_async_engine(DATABASE_URL, echo=False) # Loglar juda ko'payib ketmasligi uchun echo=False qildim
async_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

# DB Middleware yoki Dependency uchun yordamchi
async def get_session() -> AsyncSession: # type: ignore
    async with async_session() as session:
        yield session