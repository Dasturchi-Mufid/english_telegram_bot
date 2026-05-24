from aiogram.fsm.state import State, StatesGroup

class AdminStates(StatesGroup):
    # Kategoriya qo'shish jarayoni
    waiting_for_category_name = State()

    # Material (fayl) qo'shish jarayoni
    waiting_for_file = State()
    waiting_for_material_level = State() # Material darajasini aniqlash uchun
    waiting_for_title = State()
    waiting_for_material_category = State()
    
    # Savol (test) qo'shish jarayoni
    waiting_for_question_text = State()
    waiting_for_options = State()
    waiting_for_correct_answer = State()
    waiting_for_test_level = State() # Savol darajasini aniqlash uchun

class UserStates(StatesGroup):
    # Foydalanuvchi test topshirayotgan holati
    taking_quiz = State()
    # Darajani tanlash (agar kerak bo'lsa)
    waiting_for_level = State()

class BroadcastState(StatesGroup):
    waiting_for_message = State()

