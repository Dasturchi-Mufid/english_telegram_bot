from aiogram import Router, types, F
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.models import Category, Material, User

materials_router = Router()

@materials_router.message(F.text == "📚 Materiallar")
async def show_categories(message: types.Message, session: AsyncSession):
    # Bazadan barcha kategoriyalarni olamiz
    result = await session.execute(select(Category))
    categories = result.scalars().all()

    if not categories:
        await message.answer("Hozircha hech qanday material yuklanmagan.")
        return

    # Dinamik Inline tugmalar yaratish
    builder = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=cat.name, callback_data=f"user_cat_{cat.id}")] 
        for cat in categories
    ])

    await message.answer("Bo'limni tanlang:", reply_markup=builder)

@materials_router.callback_query(F.data.startswith("user_cat_"))
async def show_materials_by_category(callback: types.CallbackQuery, session: AsyncSession):
    category_id = int(callback.data.split("_")[-1])
    
    # 1. Foydalanuvchining darajasini bazadan olamiz
    user_res = await session.execute(select(User).where(User.tg_id == callback.from_user.id))
    user = user_res.scalar_one_or_none()
    
    # Darajasi yo'q bo'lsa, Beginner deb hisoblaymiz
    user_level = user.level if user and user.level else "Beginner"
    
    # 2. Tanlangan kategoriyadagi VA foydalanuvchi darajasidagi materiallarni olish
    result = await session.execute(
        select(Material).where(
            Material.category_id == category_id,
            Material.level == user_level # FILTR QO'SHILDI
        )
    )
    materials = result.scalars().all()

    if not materials:
        await callback.answer(f"Ushbu bo'limda {user_level} darajasi uchun materiallar yo'q.", show_alert=True)
        return

    kb_builder = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=m.title, callback_data=f"send_file_{m.id}")]
        for m in materials
    ])
    kb_builder.inline_keyboard.append([types.InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_categories")])

    await callback.message.edit_text(f"📖 {user_level} darajasi uchun materiallar:", reply_markup=kb_builder)
    await callback.answer()

@materials_router.callback_query(F.data.startswith("send_file_"))
async def send_specific_file(callback: types.CallbackQuery, session: AsyncSession):
    material_id = int(callback.data.split("_")[-1])
    
    result = await session.execute(select(Material).where(Material.id == material_id))
    m = result.scalars().first()

    if m:
        # Faylni file_id orqali yuborish (server trafigini tejaydi)
        if m.file_type == "document":
            await callback.message.answer_document(document=m.file_id, caption=f"📄 {m.title}")
        elif m.file_type == "audio":
            await callback.message.answer_audio(audio=m.file_id, caption=f"🎧 {m.title}")
        elif m.file_type == "video":
            await callback.message.answer_video(video=m.file_id, caption=f"🎥 {m.title}")
    
    await callback.answer()

@materials_router.callback_query(F.data == "back_to_categories")
async def back_to_categories_handler(callback: types.CallbackQuery, session: AsyncSession):
    # Bu funksiya show_categories funksiyasi bilan deyarli bir xil, 
    # faqat u yangi xabar yubormaydi, mavjud xabarni tahrirlaydi.
    
    result = await session.execute(select(Category))
    categories = result.scalars().all()

    if not categories:
        await callback.answer("Kategoriyalar topilmadi.", show_alert=True)
        return

    builder = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=cat.name, callback_data=f"user_cat_{cat.id}")] 
        for cat in categories
    ])

    await callback.message.edit_text("Bo'limni tanlang:", reply_markup=builder)
    await callback.answer()