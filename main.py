import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from database.connection import get_engine, get_sessionmaker
from middlewares.db_middlewares import DbSessionMiddleware
from handlers.start import start_router
from handlers.admin import admin_router
from handlers.materials import materials_router

async def main():
    load_dotenv()
    
    engine = get_engine()
    session_pool = get_sessionmaker(engine)

    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()

    # Middleware barcha routerlardan oldin bo'lishi kerak
    dp.update.middleware(DbSessionMiddleware(session_pool))
    
    # Routerlarni ulash (tartib muhim: avval admin, keyin user)
    dp.include_router(admin_router)
    dp.include_router(start_router)
    dp.include_router(materials_router)

    print("Bot ishga tushdi! 🚀")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())