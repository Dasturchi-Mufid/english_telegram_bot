from datetime import datetime
from aiogram import Router, types, F
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.models import QuizResult

# To'g'ri import yo'li
from app.models import User

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
            full_name=message.from_user.full_name,
            level="Beginner", # Default daraja
            created_at=datetime.now()
        )
        session.add(new_user)
        await session.commit()
        welcome_text = (
            f"👋 Salom, {message.from_user.full_name}!\n\n"
            f"IELTS tayyorlov botiga xush kelibsiz. Bu yerda siz o'z darajangizga mos "
            f"materiallarni topishingiz va bilimingizni sinab ko'rishingiz mumkin."
        )
    else:
        welcome_text = f"😊 Sizni yana ko'rganimizdan xursandmiz, {user.full_name}!"

    # Asosiy menyu tugmalari
    kb = [
        [types.KeyboardButton(text="📚 Materiallar"),
        types.KeyboardButton(text="📊 Darajamni aniqlash")], 
        [types.KeyboardButton(text="📊 Mening natijalarim"), 
        types.KeyboardButton(text="👤 Mening profilim")],
    ]
    main_menu = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    
    await message.answer(welcome_text, reply_markup=main_menu)

@start_router.message(F.text == "👤 Mening profilim")
async def show_profile(message: types.Message, session: AsyncSession):
    # Foydalanuvchi ma'lumotlarini bazadan olish
    result = await session.execute(
        select(User).where(User.tg_id == message.from_user.id)
    )
    user = result.scalar_one_or_none()

    if user:
        level = user.level if user.level else "Hali test topshirilmagan"
        
        # Ro'yxatdan o'tgan sanani chiroyli ko'rsatish
        date_str = user.created_at.strftime("%d.%m.%Y")
        
        text = (
            f"👤 **Sizning profilingiz:**\n\n"
            f"📝 **Ism:** {user.full_name}\n"
            f"📊 **Daraja:** {level}\n"
            f"🆔 **ID:** `{user.tg_id}`\n"
            f"📅 **Ro'yxatdan o'tgan sana:** {date_str}\n\n"
            f"🔄 Darajangizni yangilash uchun \"📊 Darajamni aniqlash\" tugmasini bosing."
        )
        await message.answer(text, parse_mode="Markdown")
    else:
        await message.answer("⚠️ Ma'lumotlaringiz topilmadi. Iltimos, /start buyrug'ini bosing.")

@start_router.message(F.text == "📊 Mening natijalarim")
async def show_my_results(message: types.Message, session: AsyncSession):
    # Foydalanuvchining oxirgi 5 ta testini olish
    stmt = select(QuizResult).where(
        QuizResult.user_id == message.from_user.id
    ).order_by(desc(QuizResult.created_at)).limit(5)
    
    result = await session.execute(stmt)
    results = result.scalars().all()

    if not results:
        await message.answer("Siz hali test topshirmagansiz. Test yordamida darajangizni aniqlang!")
        return

    text = "📊 **Sizning oxirgi natijalaringiz:**\n\n"
    for r in results:
        date_str = r.created_at.strftime("%d.%m.%Y")
        text += f"📅 {date_str} | 🎯 {r.score}/{r.total_questions} ({int(r.percentage)}%) | 🏆 {r.level_achieved}\n"

    await message.answer(text, parse_mode="Markdown")

