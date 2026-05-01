from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.models import Category, Material
from utils.states import AdminStates
# from config import ADMIN_IDS # config.py yoki .env dan olingan adminlar ro'yxati
from dotenv import load_dotenv
import os

load_dotenv()
ADMIN_IDS = [int(id) for id in os.getenv("ADMIN_IDS").split(",")]
admin_router = Router()

# Admin ekanligini tekshirish uchun filtr
def is_admin(message: types.Message):
    return message.from_user.id in ADMIN_IDS

# --- KATEGORIYA QO'SHISH ---
@admin_router.message(Command("add_category"))
async def add_category_start(message: types.Message, state: FSMContext):
    await message.answer("Yangi kategoriya nomini kiriting (masalan: Reading):")
    await state.set_state(AdminStates.waiting_for_category_name)

# @admin_router.message(Command("add_category")) # is_admin filtrsiz
# async def not_admin_warning(message: types.Message):
#     await message.answer("⛔️ Bu komanda faqat adminlar uchun!")

@admin_router.message(AdminStates.waiting_for_category_name)
async def add_category_finish(message: types.Message, state: FSMContext, session: AsyncSession):
    new_cat = Category(name=message.text)
    session.add(new_cat)
    await session.commit()
    await message.answer(f"✅ '{message.text}' kategoriyasi qo'shildi.")
    await state.clear()

# --- MATERIAL (FAYL) QO'SHISH ---
@admin_router.message(Command("add_material"))
async def add_material_start(message: types.Message, state: FSMContext):
    await message.answer("Material faylini yuboring (PDF, Audio yoki Video):")
    await state.set_state(AdminStates.waiting_for_file)

@admin_router.message(AdminStates.waiting_for_file, F.document | F.audio | F.video)
async def process_file(message: types.Message, state: FSMContext):
    # Fayl turini va ID sini aniqlash
    if message.document:
        f_id, f_type = message.document.file_id, "document"
    elif message.audio:
        f_id, f_type = message.audio.file_id, "audio"
    else:
        f_id, f_type = message.video.file_id, "video"

    await state.update_data(file_id=f_id, file_type=f_type)
    await message.answer("Ushbu material uchun nom kiriting:")
    await state.set_state(AdminStates.waiting_for_title)

@admin_router.message(AdminStates.waiting_for_title)
async def process_title(message: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(title=message.text)
    
    # Bazadan barcha kategoriyalarni olib, tugma qilib ko'rsatish
    result = await session.execute(select(Category))
    categories = result.scalars().all()
    
    if not categories:
        await message.answer("Avval kategoriya yarating! /add_category")
        await state.clear()
        return

    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=cat.name, callback_data=f"cat_{cat.id}")] for cat in categories
    ])
    
    await message.answer("Kategoriyani tanlang:", reply_markup=kb)
    await state.set_state(AdminStates.waiting_for_material_category)

@admin_router.callback_query(AdminStates.waiting_for_material_category, F.data.startswith("cat_"))
async def process_category_selection(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    cat_id = int(callback.data.split("_")[1])
    data = await state.get_data()
    
    new_material = Material(
        title=data['title'],
        file_id=data['file_id'],
        file_type=data['file_type'],
        category_id=cat_id
    )
    
    session.add(new_material)
    await session.commit()
    
    await callback.message.edit_text(f"✅ Material muvaffaqiyatli saqlandi!")
    await state.clear()
    await callback.answer()