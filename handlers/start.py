from aiogram import Router, types, F
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.models import User

start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: types.Message, session: AsyncSession):
    # Foydalanuvchini bazadan qidiramiz
    result = await session.execute(select(User).where(User.tg_id == message.from_user.id))
    user = result.scalars().first()

    if not user:
        # Yangi foydalanuvchini qo'shish
        new_user = User(
            tg_id=message.from_user.id,
            full_name=message.from_user.full_name
        )
        session.add(new_user)
        await session.commit()
        welcome_text = f"Salom, {message.from_user.full_name}! IELTS tayyorlov botiga xush kelibsiz."
    else:
        welcome_text = f"Sizni yana ko'rganimizdan xursandmiz, {user.full_name}!"

    # Asosiy menyu tugmalari
    kb = [
        [types.KeyboardButton(text="📚 Materiallar")],
        [types.KeyboardButton(text="📊 Darajamni aniqlash"), types.KeyboardButton(text="⚙️ Sozlamalar")]
    ]
    main_menu = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    
    await message.answer(welcome_text, reply_markup=main_menu)