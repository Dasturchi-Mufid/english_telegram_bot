import asyncio
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, BigInteger, String, select, text

# 1. .env faylidan ma'lumotlarni yuklash
load_dotenv()

DB_USER = os.getenv("DB_USER", "bot_user")
DB_PASS = os.getenv("DB_PASS", "bot_paroli_123")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "ielts_bot_db")
DB_PORT = os.getenv("DB_PORT", "5432")

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 2. Engine va Model tayyorlash
Base = declarative_base()
engine = create_async_engine(DATABASE_URL, echo=True) # echo=True orqali SQL so'rovlarni terminalda ko'rasiz
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class User(Base):
    __tablename__ = 'test_users'
    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger, unique=True)
    name = Column(String)

# 3. Tekshiruv funksiyasi
async def test_connection():
    try:
        print("🚀 Bazaga ulanishga urinish...")
        
        # Jadvallarni yaratish
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Jadvallar muvaffaqiyatli yaratildi!")

        # Ma'lumot qo'shib ko'rish
        async with async_session() as session:
            new_user = User(tg_id=1234567, name="Test User")
            session.add(new_user)
            await session.commit()
            print("✅ Test ma'lumot bazaga yozildi!")

            # Ma'lumotni qayta o'qish
            result = await session.execute(select(User).where(User.tg_id == 1234567))
            user = result.scalars().first()
            if user:
                print(f"✅ Bazadan o'qilgan ma'lumot: {user.name} (ID: {user.tg_id})")

    except Exception as e:
        print(f"❌ Xatolik yuz berdi: {e}")
    finally:
        await engine.dispose()
        print("🔌 Ulanish uzildi.")

if __name__ == "__main__":
    asyncio.run(test_connection())