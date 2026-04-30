from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, BigInteger
from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")

# URL-ni yig'ish
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

Base = declarative_base()
engine = create_async_engine(
    DATABASE_URL, 
    echo=False, 
    pool_size=20,       # Bir vaqtda ochiq ulanishlar soni
    max_overflow=10     # Zarur bo'lsa qo'shimcha ochiladigan ulanishlar
    )
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger, unique=True)
    full_name = Column(String)
    level = Column(String, default="Unknown")

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)