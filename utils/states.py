from aiogram.fsm.state import State, StatesGroup

class AdminStates(StatesGroup):
    waiting_for_file = State()       # Admin fayl yuborishini kutish
    waiting_for_title = State()      # Fayl nomini kiritishni kutish
    waiting_for_category = State()   # Kategoriyani tanlashni kutish
    waiting_for_category_name = State() # Yangi kategoriya nomi

class UserStates(StatesGroup):
    waiting_for_level = State()      # Darajasini tanlashni kutish