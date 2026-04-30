from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from old.database import async_session, User
from sqlalchemy import select
from old.config import ADMIN_IDS

router = Router()

# --- ADMIN FILTRI ---
def is_admin(message: types.Message):
    return message.from_user.id in ADMIN_IDS

# --- ADMIN PANEL ---
@router.message(Command("admin"), is_admin)
async def admin_panel(message: types.Message):
    kb = InlineKeyboardBuilder()
    kb.row(types.InlineKeyboardButton(text="📢 Xabar tarqatish", callback_data="broadcast"))
    kb.row(types.InlineKeyboardButton(text="📊 Statistika", callback_data="stats"))
    await message.answer("Admin panelga xush kelibsiz:", reply_markup=kb.as_markup())

# --- FILE ID TUTIB OLUVCHI (ADMIN UCHUN) ---
# Admin kanalga yoki botga fayl tashlasa, bot unga file_id sini beradi
@router.message(is_admin, F.document | F.audio | F.video | F.voice)
async def get_file_id_handler(message: types.Message):
    file_id = ""
    file_type = ""
    
    if message.document:
        file_id = message.document.file_id
        file_type = "Document (PDF/Doc)"
    elif message.audio:
        file_id = message.audio.file_id
        file_type = "Audio (MP3)"
    elif message.video:
        file_id = message.video.file_id
        file_type = "Video"
    elif message.voice:
        file_id = message.voice.file_id
        file_type = "Voice"

    text = (
        f"✅ **Fayl qabul qilindi!**\n\n"
        f"📂 Turi: {file_type}\n"
        f"🆔 ` {file_id} `\n\n"
        f"Ushbu ID-ni kodda yoki bazada ishlating."
    )
    await message.reply(text, parse_mode="Markdown")

# --- STATISTIKA ---
@router.callback_query(F.data == "stats", is_admin)
async def show_stats(callback: types.CallbackQuery):
    async with async_session() as session:
        result = await session.execute(select(User))
        count = len(result.scalars().all())
    await callback.message.answer(f"Botdagi jami foydalanuvchilar: {count} ta")
    await callback.answer()

# --- XABAR TARQATISH (BROADCAST) ---
@router.callback_query(F.data == "broadcast", is_admin)
async def start_broadcast(callback: types.CallbackQuery):
    await callback.message.answer("Tarqatmoqchi bo'lgan xabaringizni yuboring (matn, rasm yoki fayl):")
    # Bu yerda FSM (Finite State Machine) ishlatish kerak, 
    # lekin MVP uchun sodda tushuntiraman.
    await callback.answer()

@router.message(Command("start"))
async def start_handler(message: types.Message):
    async with async_session() as session:
        # Foydalanuvchini bazaga qo'shish
        user = await session.execute(select(User).where(User.tg_id == message.from_user.id))
        if not user.scalars().first():
            new_user = User(tg_id=message.from_user.id, full_name=message.from_user.full_name)
            session.add(new_user)
            await session.commit()
    
    kb = InlineKeyboardBuilder()
    kb.row(types.InlineKeyboardButton(text="📚 Materiallar", callback_data="materials"))
    kb.row(types.InlineKeyboardButton(text="📊 Darajani aniqlash", callback_data="test"))
    
    await message.answer(f"Salom {message.from_user.full_name}! IELTS tayyorlov botiga xush kelibsiz.", 
                         reply_markup=kb.as_markup())

@router.callback_query(F.data == "materials")
async def show_materials(callback: types.CallbackQuery):
    kb = InlineKeyboardBuilder()
    # Bu yerda materiallar bo'limlarini chiqaramiz
    kb.row(types.InlineKeyboardButton(text="🎧 Listening Practice", callback_data="get_listening"))
    await callback.message.edit_text("Kerakli bo'limni tanlang:", reply_markup=kb.as_markup())

@router.callback_query(F.data == "get_listening")
async def send_listening(callback: types.CallbackQuery):
    # MUHIM: Faylni bir marta kanalga tashlab, file_id sini oling
    # Bu yerda o'sha file_id qo'yiladi (server trafigini tejash uchun)
    FILE_ID = "BQACAgIAAxkBAAEJ..." 
    await callback.message.answer_document(document=FILE_ID, caption="IELTS Listening Mock Test #1")
    await callback.answer()