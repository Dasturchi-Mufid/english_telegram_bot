from aiogram import Router, types, F
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.models import User

user_router = Router()

@user_router.message(CommandStart())
async def cmd_start(message: types.Message, session: AsyncSession):
    # Foydalanuvchini bazadan tekshirish
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
        text = f"Xush kelibsiz {message.from_user.full_name}! Ro'yxatdan o'tdingiz."
    else:
        text = f"Sizni yana ko'rganimizdan xursandmiz, {user.full_name}!"

    await message.answer(text)