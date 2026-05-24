import os
import asyncio
from aiogram import Router, types, F
from aiogram.filters import Command, BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from dotenv import load_dotenv

# Yangi loyiha strukturasi bo'yicha importlar
from app.models import Category, Material, Question, User, QuizResult
from app.utils.states import AdminStates,BroadcastState

load_dotenv()

# Adminlarni tekshirish uchun ro'yxat
ADMIN_IDS = [int(id) for id in os.getenv("ADMIN_IDS", "").split(",") if id]

admin_router = Router()

# --- ADMIN FILTRI (Custom Filter) ---
class IsAdminFilter(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        return message.from_user.id in ADMIN_IDS

def get_admin_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    
    # Tugmalarni qo'shamiz
    builder.button(text="📂 Kategoriya qo'shish")
    builder.button(text="📝 Savol qo'shish")
    builder.button(text="📁 Material yuklash")
    builder.button(text="📊 Statistika")
    builder.button(text="📢 Xabar yuborish")
    
    # Tugmalarni qatorma-qator 2 tadan qilib joylashtirish
    builder.adjust(2)
    
    # resize_keyboard=True - tugmalar ekranga moslashib, ixcham turishi uchun
    return builder.as_markup(resize_keyboard=True)

# Bu router ichidagi barcha handlerlar uchun ushbu filtr majburiy bo'ladi
admin_router.message.filter(IsAdminFilter())
admin_router.callback_query.filter(IsAdminFilter())

@admin_router.message(Command("admin"))
async def admin_start(message: types.Message):
    await message.answer(
        "👨‍💻 **Admin paneliga xush kelibsiz!**\n\nBoshqaruv menyusidan kerakli bo'limni tanlang:",
        reply_markup=get_admin_keyboard(),
        parse_mode="Markdown"
    )

# Barcha admin router komandalariga filtirni qo'llash
admin_router.message.filter(IsAdminFilter())
admin_router.callback_query.filter(IsAdminFilter())

# --- KATEGORIYA QO'SHISH ---
@admin_router.message(Command("add_category"))
@admin_router.message((F.text == "📂 Kategoriya qo'shish"))
async def add_category_start(message: types.Message, state: FSMContext):
    await message.answer("🆕 Yangi kategoriya nomini kiriting (masalan: Writing):")
    await state.set_state(AdminStates.waiting_for_category_name)

@admin_router.message(AdminStates.waiting_for_category_name)
async def add_category_finish(message: types.Message, state: FSMContext, session: AsyncSession):
    new_cat = Category(name=message.text)
    session.add(new_cat)
    await session.commit()
    await message.answer(f"✅ '{message.text}' kategoriyasi muvaffaqiyatli qo'shildi.")
    await state.clear()

# --- MATERIAL (FAYL) QO'SHISH ---
@admin_router.message(Command("add_material"))
@admin_router.message((F.text == "📁 Material yuklash"))
async def add_material_start(message: types.Message, state: FSMContext):
    await message.answer("📎 Material faylini yuboring (PDF, Audio yoki Video):")
    await state.set_state(AdminStates.waiting_for_file)

@admin_router.message(AdminStates.waiting_for_file, F.document | F.audio | F.video)
async def process_file(message: types.Message, state: FSMContext):
    if message.document:
        f_id, f_type = message.document.file_id, "document"
    elif message.audio:
        f_id, f_type = message.audio.file_id, "audio"
    else:
        f_id, f_type = message.video.file_id, "video"

    await state.update_data(file_id=f_id, file_type=f_type)

    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Beginner 🟢", callback_data="matlvl_Beginner")],
        [types.InlineKeyboardButton(text="Intermediate 🟡", callback_data="matlvl_Intermediate")],
        [types.InlineKeyboardButton(text="Advanced 🔴", callback_data="matlvl_Advanced")]
    ])
    await message.answer("📊 Ushbu material qaysi darajaga mos?", reply_markup=kb)
    await state.set_state(AdminStates.waiting_for_test_level)

@admin_router.callback_query(AdminStates.waiting_for_test_level, F.data.startswith("matlvl_"))
async def process_material_level(callback: types.CallbackQuery, state: FSMContext):
    level = callback.data.split("_")[1]
    await state.update_data(material_level=level)
    
    await callback.message.edit_text(f"✅ Tanlangan daraja: {level}\n\n📝 Endi ushbu material uchun sarlavha (title) kiriting:")
    await state.set_state(AdminStates.waiting_for_title)
    await callback.answer()

@admin_router.message(AdminStates.waiting_for_title)
async def process_title(message: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(title=message.text)
    
    result = await session.execute(select(Category))
    categories = result.scalars().all()
    
    if not categories:
        await message.answer("⚠️ Avval kategoriya yarating! /add_category")
        await state.clear()
        return

    kb_builder = []
    for cat in categories:
        kb_builder.append([types.InlineKeyboardButton(text=cat.name, callback_data=f"admincat_{cat.id}")])
    
    kb = types.InlineKeyboardMarkup(inline_keyboard=kb_builder)
    await message.answer("📂 Kategoriyani tanlang:", reply_markup=kb)
    await state.set_state(AdminStates.waiting_for_material_category)

@admin_router.callback_query(AdminStates.waiting_for_material_category, F.data.startswith("admincat_"))
async def process_category_selection(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    cat_id = int(callback.data.split("_")[1])
    data = await state.get_data()
    
    new_material = Material(
        title=data['title'],
        file_id=data['file_id'],
        file_type=data['file_type'],
        category_id=cat_id,
        level=data['material_level']
    )
    
    session.add(new_material)
    await session.commit()
    
    await callback.message.edit_text(
        f"✅ Material saqlandi!\n"
        f"🔹 Nom: {data['title']}\n"
        f"🔹 Daraja: {data['material_level']}"
    )
    await state.clear()
    await callback.answer()

# --- SAVOL QO'SHISH ---
@admin_router.message(Command("add_question"))
@admin_router.message((F.text == "📝 Savol qo'shish"))
async def add_question_start(message: types.Message, state: FSMContext):
    await message.answer("❓ Test savoli matnini kiriting:")
    await state.set_state(AdminStates.waiting_for_question_text)

@admin_router.message(AdminStates.waiting_for_question_text)
async def process_question_text(message: types.Message, state: FSMContext):
    await state.update_data(q_text=message.text)
    await message.answer(
        "📝 Variantlarni kiriting.\n"
        "Format: Variant1, Variant2, Variant3, Variant4\n"
        "*(Aralashtirib yubormang, 4 ta variant bo'lishi shart)*"
    )
    await state.set_state(AdminStates.waiting_for_options)

@admin_router.message(AdminStates.waiting_for_options)
async def process_options(message: types.Message, state: FSMContext):
    options = [opt.strip() for opt in message.text.split(",")]
    if len(options) != 4:
        await message.answer("🚫 Xato! Iltimos, 4 ta variantni vergul bilan ajratib yuboring.")
        return

    await state.update_data(opt_a=options[0], opt_b=options[1], opt_c=options[2], opt_d=options[3])
    
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text="A", callback_data="correct_a"),
            types.InlineKeyboardButton(text="B", callback_data="correct_b"),
            types.InlineKeyboardButton(text="C", callback_data="correct_c"),
            types.InlineKeyboardButton(text="D", callback_data="correct_d")
        ]
    ])
    await message.answer("🎯 To'g'ri javobni belgilang:", reply_markup=kb)
    await state.set_state(AdminStates.waiting_for_correct_answer)

@admin_router.callback_query(AdminStates.waiting_for_correct_answer, F.data.startswith("correct_"))
async def process_correct_answer(callback: types.CallbackQuery, state: FSMContext):
    correct_letter = callback.data.split("_")[1]
    await state.update_data(correct=correct_letter)
    
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Beginner", callback_data="qlevel_Beginner")],
        [types.InlineKeyboardButton(text="Intermediate", callback_data="qlevel_Intermediate")],
        [types.InlineKeyboardButton(text="Advanced", callback_data="qlevel_Advanced")]
    ])
    await callback.message.edit_text("📈 Ushbu savol qaysi darajaga mos?", reply_markup=kb)
    await state.set_state(AdminStates.waiting_for_test_level)

@admin_router.callback_query(AdminStates.waiting_for_test_level, F.data.startswith("qlevel_"))
async def save_question(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    lvl = callback.data.split("_")[1]
    data = await state.get_data()
    
    new_q = Question(
        text=data['q_text'],
        option_a=data['opt_a'],
        option_b=data['opt_b'],
        option_c=data['opt_c'],
        option_d=data['opt_d'],
        correct_option=data['correct'],
        level=lvl
    )
    
    session.add(new_q)
    await session.commit()
    
    await callback.message.edit_text(f"✅ Savol muvaffaqiyatli saqlandi! (Daraja: {lvl})")
    await state.clear()
    await callback.answer()


@admin_router.message(F.text == "📊 Statistika")
async def show_stats(message: types.Message, session: AsyncSession):
    # Foydalanuvchilar sonini hisoblash
    user_count = await session.execute(select(func.count(User.id)))
    # Test topshirganlar soni
    quiz_count = await session.execute(select(func.count(QuizResult.id)))
    
    await message.answer(
        f"📈 **Bot statistikasi:**\n\n"
        f"👤 Foydalanuvchilar: {user_count.scalar()}\n"
        f"📝 Topshirilgan testlar: {quiz_count.scalar()}"
    )

@admin_router.message(F.text == "📢 Xabar yuborish")
async def start_broadcast(message: types.Message, state: FSMContext):
    await message.answer("Barcha foydalanuvchilarga yubormoqchi bo'lgan xabaringizni yozing (matn, rasm yoki video bo'lishi mumkin):")
    await state.set_state(BroadcastState.waiting_for_message)

@admin_router.message(BroadcastState.waiting_for_message)
async def broadcast_to_users(message: types.Message, state: FSMContext, session: AsyncSession):
    users = await session.execute(select(User.tg_id))
    user_ids = users.scalars().all()
    
    count = 0
    for uid in user_ids:
        if uid in ADMIN_IDS:
            continue
        try:
            await message.copy_to(chat_id=uid)
            count += 1
            await asyncio.sleep(0.05) # Telegram limitidan oshib ketmaslik uchun
        except Exception:
            pass
    
    await message.answer(f"✅ Xabar {count} ta foydalanuvchiga muvaffaqiyatli yuborildi!")
    await state.clear()

