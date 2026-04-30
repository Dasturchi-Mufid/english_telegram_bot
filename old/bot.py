import asyncio
from aiogram import Bot, Dispatcher
from old.handlers import router
from old.database import init_db

TOKEN = "7866971008:AAGgOR2ubR9SwTdF1OZ_5_ua9OyRAkTi8ZU"

async def main():
    await init_db() # Bazani yaratish
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())