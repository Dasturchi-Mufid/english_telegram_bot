from aiogram.fsm.state import State, StatesGroup

class AdminStates(StatesGroup):
    waiting_for_file = State()       # Admin fayl yuborishini kutish
    waiting_for_title = State()      # Fayl nomini kiritishni kutish
    waiting_for_material_category = State()   # Kategoriyani tanlashni kutish
    waiting_for_category_name = State() # Yangi kategoriya nomi
    waiting_for_question_text = State()
    waiting_for_options = State()      # Variantlarni kiritish (A, B, C, D)
    waiting_for_correct_answer = State()
    waiting_for_test_level = State()

class UserStates(StatesGroup):
    waiting_for_level = State()      # Darajasini tanlashni kutish