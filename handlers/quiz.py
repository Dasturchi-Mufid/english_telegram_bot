from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update
from database.models import Question, User
from utils.states import UserStates
import random

quiz_router = Router()

@quiz_router.message(F.text == "📊 Darajamni aniqlash")
async def start_placement_test(message: types.Message, state: FSMContext, session: AsyncSession):
    # Bazadan 10 ta tasodifiy savolni olish
    result = await session.execute(select(Question).order_by(func.random()).limit(10))
    questions = result.scalars().all()

    if len(questions) < 5:
        await message.answer("Kechirasiz, test tizimi hali tayyor emas (savollar yetarli emas).")
        return

    # Savollarni state-ga saqlab qo'yamiz
    q_list = []
    for q in questions:
        q_list.append({
            "id": q.id,
            "text": q.text,
            "options": [q.option_a, q.option_b, q.option_c, q.option_d],
            "correct": q.correct_option.lower()
        })

    await state.update_data(quiz_questions=q_list, current_q=0, score=0)
    await message.answer(f"Test boshlandi! Jami {len(questions)} ta savol. Omad!")
    await send_next_question(message, state)

async def send_next_question(message: types.Message, state: FSMContext):
    data = await state.get_data()
    q_idx = data['current_q']
    questions = data['quiz_questions']

    if q_idx < len(questions):
        q = questions[q_idx]
        
        # Tugmalarni yaratish
        kb = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text=q['options'][0], callback_data="ans_a")],
            [types.InlineKeyboardButton(text=q['options'][1], callback_data="ans_b")],
            [types.InlineKeyboardButton(text=q['options'][2], callback_data="ans_c")],
            [types.InlineKeyboardButton(text=q['options'][3], callback_data="ans_d")]
        ])

        await message.answer(f"Savol {q_idx + 1}: {q['text']}", reply_markup=kb)
    else:
        await finish_quiz(message, state)

@quiz_router.callback_query(F.data.startswith("ans_"))
async def process_answer(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    q_idx = data['current_q']
    questions = data['quiz_questions']
    score = data['score']
    
    user_answer = callback.data.split("_")[1] # a, b, c, d
    correct_answer = questions[q_idx]['correct']

    if user_answer == correct_answer:
        score += 1
    
    await state.update_data(current_q=q_idx + 1, score=score)
    await callback.message.delete()
    
    data = await state.get_data()
    if data['current_q'] < len(data['quiz_questions']):
        await send_next_question(callback.message, state)
    else:
        # BU YERDA session-ni uzatib yuboramiz:
        await finish_quiz(callback.message, state, session) 
    
    await callback.answer()


async def finish_quiz(message: types.Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    score = data.get('score', 0)
    questions = data.get('quiz_questions', [])
    max_score = len(questions) # Savollar sonidan kelib chiqib maksimal ball
    
    # Max_score 0 bo'lib qolmasligini tekshiramiz (bo'lishda xato chiqmasligi uchun)
    if max_score == 0:
        await message.answer("Xatolik: Savollar topilmadi.")
        await state.clear()
        return

    # Foizni hisoblaymiz
    success_percentage = (score / max_score) * 100
    
    # Darajani foizga qarab aniqlash
    if success_percentage < 40:
        level = "Beginner"
    elif success_percentage < 80:
        level = "Intermediate"
    else:
        level = "Advanced"

    # 1. Ma'lumotlar bazasida foydalanuvchi darajasini yangilash
    # message.chat.id orqali foydalanuvchini topamiz va levelni yangilaymiz
    stmt = (
        update(User)
        .where(User.tg_id == message.chat.id)
        .values(level=level)
    )
    await session.execute(stmt)
    await session.commit()

    # 2. Foydalanuvchiga natijani yuborish
    await message.answer(
        f"🏁 **Test yakunlandi!**\n\n"
        f"📊 Natija: {score} / {max_score} ({success_percentage:.1f}%)\n"
        f"🏆 Sizning darajangiz: **{level}**\n\n"
        f"Darajangiz bazada yangilandi. Endi sizga mos materiallarni ko'rishingiz mumkin!"
    )
    
    await state.clear()

