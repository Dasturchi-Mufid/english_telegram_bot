from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update
from app.models import QuizResult, User
import random

# Yangi import yo'llari
from app.models import Question, User
from app.utils.states import UserStates

quiz_router = Router()

@quiz_router.message(F.text == "📊 Darajamni aniqlash")
async def start_placement_test(message: types.Message, state: FSMContext, session: AsyncSession):
    # Bazadan 10 ta tasodifiy savolni olish
    # Postgres uchun func.random() ishlatiladi
    result = await session.execute(select(Question).order_by(func.random()).limit(10))
    questions = result.scalars().all()

    if len(questions) < 5:
        await message.answer("⚠️ Kechirasiz, test tizimi hali tayyor emas (savollar yetarli emas).")
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
    await message.answer(f"🚀 Test boshlandi! Jami {len(questions)} ta savol. Omad!")
    await send_next_question(message, state)

async def send_next_question(message: types.Message, state: FSMContext):
    data = await state.get_data()
    q_idx = data.get('current_q', 0)
    questions = data.get('quiz_questions', [])

    if q_idx < len(questions):
        q = questions[q_idx]
        
        # Variantlarni chalkashtirib (shuffle) chiqarish ham mumkin, 
        # lekin bazada qat'iy tartib bo'lsa, quyidagicha qoladi:
        kb = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text=q['options'][0], callback_data="ans_a")],
            [types.InlineKeyboardButton(text=q['options'][1], callback_data="ans_b")],
            [types.InlineKeyboardButton(text=q['options'][2], callback_data="ans_c")],
            [types.InlineKeyboardButton(text=q['options'][3], callback_data="ans_d")]
        ])

        await message.answer(f"❓ **Savol {q_idx + 1}:**\n\n{q['text']}", reply_markup=kb, parse_mode="Markdown")
    else:
        # Agar qandaydir sabab bilan savol tugasa-yu, finish chaqirilmagan bo'lsa
        await message.answer("Test yakunlanmoqda...")

@quiz_router.callback_query(F.data.startswith("ans_"))
async def process_answer(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    q_idx = data.get('current_q')
    questions = data.get('quiz_questions')
    score = data.get('score')
    
    if questions is None or q_idx >= len(questions):
        await callback.answer("Xatolik yuz berdi.")
        return

    user_answer = callback.data.split("_")[1] # a, b, c, d
    correct_answer = questions[q_idx]['correct']

    if user_answer == correct_answer:
        score += 1
    
    new_idx = q_idx + 1
    await state.update_data(current_q=new_idx, score=score)
    
    # Eskisini o'chiramiz yoki tahrirlaymiz
    try:
        await callback.message.delete()
    except:
        pass # Ba'zida xabar o'chib ketgan bo'ladi
    
    if new_idx < len(questions):
        await send_next_question(callback.message, state)
    else:
        await finish_quiz(callback.message, state, session) 
    
    await callback.answer()


async def finish_quiz(message: types.Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    score = data.get('score', 0)
    questions = data.get('quiz_questions', [])
    max_score = len(questions)
    
    if max_score == 0:
        await message.answer("❌ Xatolik: Savollar topilmadi.")
        await state.clear()
        return

    success_percentage = (score / max_score) * 100
    
    # Darajani aniqlash mantiqi
    if success_percentage < 40:
        level = "Beginner"
    elif success_percentage < 80:
        level = "Intermediate"
    else:
        level = "Advanced"

    # 1. Natijani tarix (quiz_results) jadvaliga saqlash
    new_result = QuizResult(
        user_id=message.chat.id,
        score=score,
        total_questions=max_score,
        percentage=float(success_percentage),
        level_achieved=level
    )
    session.add(new_result)

    # 2. Bazada foydalanuvchining asosiy darajasini yangilash
    stmt = (
        update(User)
        .where(User.tg_id == message.chat.id)
        .values(level=level)
    )
    await session.execute(stmt)
    
    # Tranzaksiyani yakunlash
    await session.commit()

    # Foydalanuvchiga xabar yuborish
    await message.answer(
        f"🏁 **Test yakunlandi!**\n\n"
        f"📊 Natijangiz: **{score} / {max_score}**\n"
        f"📈 Foiz: **{success_percentage:.1f}%**\n"
        f"🏆 Sizning darajangiz: **{level}**\n\n"
        f"✅ Ma'lumotlaringiz saqlandi. \"Mening natijalarim\" bo'limida tarixingizni kuzatishingiz mumkin!"
    )
    
    await state.clear()
    