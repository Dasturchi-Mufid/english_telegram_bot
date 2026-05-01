import asyncio
import os
import sys
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

# Loyiha papkasini tanitish
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from database.models import Base
from database.connection import get_engine, get_sessionmaker
from middlewares.db_middlewares import DbSessionMiddleware
from handlers.start import start_router
from handlers.admin import admin_router
from handlers.materials import materials_router
from middlewares.admin_middlewares import AdminCheckMiddleware

async def main():
    load_dotenv()
    
    # 1. Baza ulanishini sozlash
    engine = get_engine()
    session_pool = get_sessionmaker(engine)

    # 2. MUHIM: Jadvallarni yaratish (bu qism xatolikni yo'qotadi)
    print("🚀 Jadvallar tekshirilmoqda...")
    async with engine.begin() as conn:
        # Bu buyruq Base modelidagi barcha jadvallarni (User, Category, Material) yaratadi
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Jadvallar tayyor!")

    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()

    # Middleware
    dp.update.middleware(DbSessionMiddleware(session_pool))
    
    admin_router.message.middleware(AdminCheckMiddleware())
    
    # Routerlar
    dp.include_router(admin_router)
    dp.include_router(start_router)
    dp.include_router(materials_router)


    print("🤖 Bot ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🔴 Bot to'xtatildi")