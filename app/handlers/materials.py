from aiogram import Router, types, F
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

# To'g'ri import yo'llari
from app.models import Category, Material, User

materials_router = Router()

@materials_router.message(F.text == "📚 Materiallar")
async def show_categories(message: types.Message, session: AsyncSession):
    # Bazadan barcha kategoriyalarni olamiz
    result = await session.execute(select(Category))
    categories = result.scalars().all()

    if not categories:
        await message.answer("😔 Hozircha hech qanday bo'lim yaratilmagan.")
        return

    # Dinamik Inline tugmalar yaratish
    buttons = [
        [types.InlineKeyboardButton(text=cat.name, callback_data=f"user_cat_{cat.id}")] 
        for cat in categories
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    await message.answer("📂 Bo'limni tanlang:", reply_markup=keyboard)

@materials_router.callback_query(F.data.startswith("user_cat_"))
async def show_materials_by_category(callback: types.CallbackQuery, session: AsyncSession):
    category_id = int(callback.data.split("_")[-1])
    
    # 1. Foydalanuvchining darajasini bazadan olamiz
    user_res = await session.execute(select(User).where(User.tg_id == callback.from_user.id))
    user = user_res.scalar_one_or_none()
    
    # Darajasi hali aniqlanmagan bo'lsa Beginner deb hisoblaymiz
    user_level = user.level if user and user.level else "Beginner"
    
    # 2. Tanlangan kategoriyadagi VA foydalanuvchi darajasidagi materiallarni olish
    result = await session.execute(
        select(Material).where(
            Material.category_id == category_id,
            Material.level == user_level
        )
    )
    materials = result.scalars().all()

    if not materials:
        await callback.answer(f"⚠️ Bu bo'limda {user_level} darajasi uchun materiallar topilmadi.", show_alert=True)
        return

    # Materiallar ro'yxatini chiqarish
    buttons = [
        [types.InlineKeyboardButton(text=f"📖 {m.title}", callback_data=f"send_file_{m.id}")]
        for m in materials
    ]
    buttons.append([types.InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_categories")])
    
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    await callback.message.edit_text(
        f"✅ Sizning darajangiz: {user_level}\n📖 Kerakli materialni tanlang:", 
        reply_markup=keyboard
    )
    await callback.answer()

@materials_router.callback_query(F.data.startswith("send_file_"))
async def send_specific_file(callback: types.CallbackQuery, session: AsyncSession):
    material_id = int(callback.data.split("_")[-1])
    
    result = await session.execute(select(Material).where(Material.id == material_id))
    m = result.scalars().first()

    if m:
        # Faylni file_id orqali yuborish
        try:
            if m.file_type == "document":
                await callback.message.answer_document(document=m.file_id, caption=f"📄 {m.title}")
            elif m.file_type == "audio":
                await callback.message.answer_audio(audio=m.file_id, caption=f"🎧 {m.title}")
            elif m.file_type == "video":
                await callback.message.answer_video(video=m.file_id, caption=f"🎥 {m.title}")
        except Exception as e:
            await callback.message.answer("❌ Faylni yuborishda xatolik yuz berdi. Fayl ID eskirgan bo'lishi mumkin.")
    
    await callback.answer()

@materials_router.callback_query(F.data == "back_to_categories")
async def back_to_categories_handler(callback: types.CallbackQuery, session: AsyncSession):
    result = await session.execute(select(Category))
    categories = result.scalars().all()

    if not categories:
        await callback.answer("Kategoriyalar topilmadi.", show_alert=True)
        return

    buttons = [
        [types.InlineKeyboardButton(text=cat.name, callback_data=f"user_cat_{cat.id}")] 
        for cat in categories
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    await callback.message.edit_text("📂 Bo'limni tanlang:", reply_markup=keyboard)
    await callback.answer()