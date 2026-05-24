from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
import os

class AdminCheckMiddleware(BaseMiddleware):
    def __init__(self):
        # Adminlar ro'yxatini middleware yaratilayotganda bir marta o'qiymiz
        self.admin_ids = [int(id) for id in os.getenv("ADMIN_IDS", "").split(",") if id]
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        # Faqat Message turidagi eventlarni tekshiramiz (CallbackQuery uchun ham kerak bo'lishi mumkin)
        user_id = event.from_user.id
        
        if user_id not in self.admin_ids:
            # Agar bu xabar (Message) bo'lsa, javob qaytaramiz
            if isinstance(event, Message):
                await event.answer("⛔️ Bu bo'lim faqat adminlar uchun!")
            return # Handlerga o'tkazilmaydi

        return await handler(event, data)