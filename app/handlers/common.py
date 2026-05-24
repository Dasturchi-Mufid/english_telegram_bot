from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

common_router = Router()

# @common_router.message(F.text.casefold() == "bekor qilish")
@common_router.message(F.text.casefold() == "/cancel")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer(
        "🚫 Amal bekor qilindi.",
    )