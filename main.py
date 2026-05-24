import asyncio
import os
import sys
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

# Loyiha papkasini tanitish (Importlar adashmasligi uchun)
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.models import Base
from app.database import engine, async_session # Nomlarni mosladik
from app.middlewares.db_middlewares import DbSessionMiddleware
from app.middlewares.admin_middlewares import AdminCheckMiddleware
from app.handlers.start import start_router
from app.handlers.admin import admin_router
from app.handlers.common import common_router
from app.handlers.materials import materials_router
from app.handlers.quiz import quiz_router

async def main():
    load_dotenv()
    
    # Loggingni yoqish (xatolarni ko'rish uchun)
    logging.basicConfig(level=logging.INFO)

    # 1. Jadvallarni yaratish (Alembic ishlatmagan bo'lsangiz, bu shart)
    print("🚀 Jadvallar tekshirilmoqda...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Jadvallar tayyor!")

    # 2. Bot va Dispatcher
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher(storage=MemoryStorage())

    # 3. Middleware-larni ulash
    # Global DB middleware (hamma routerlar uchun)
    dp.update.middleware(DbSessionMiddleware(session_pool=async_session))
    
    # Faqat admin_router uchun adminlikni tekshirish
    admin_router.message.middleware(AdminCheckMiddleware())
    admin_router.callback_query.middleware(AdminCheckMiddleware())

    # 4. Routerlarni ulash (Tartib muhim: Admin va Start birinchi)
    dp.include_router(common_router)
    dp.include_router(admin_router)
    dp.include_router(start_router)
    dp.include_router(materials_router)
    dp.include_router(quiz_router)

    print("🤖 Bot ishga tushdi!")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🔴 Bot to'xtatildi")