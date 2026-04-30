from aiogram import Router, types, F
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.models import Category, Material

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
    
    # Tanlangan kategoriyadagi barcha materiallarni olish
    result = await session.execute(
        select(Material).where(Material.category_id == category_id)
    )
    materials = result.scalars().all()

    if not materials:
        await callback.answer("Bu bo'limda hozircha materiallar yo'q.", show_alert=True)
        return

    # Materiallar ro'yxatini chiqarish
    # Bu yerda har bir material uchun alohida tugma yoki ro'yxat chiqarish mumkin
    kb_builder = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=m.title, callback_data=f"send_file_{m.id}")]
        for m in materials
    ])
    kb_builder.inline_keyboard.append([types.InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_categories")])

    await callback.message.edit_text("Materialni tanlang:", reply_markup=kb_builder)

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