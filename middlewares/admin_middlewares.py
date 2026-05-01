from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
import os

class AdminCheckMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        # .env dan adminlar ro'yxatini olish
        admin_ids = [int(id) for id in os.getenv("ADMIN_IDS").split(",")]
        
        if event.from_user.id not in admin_ids:
            await event.answer("⛔️ Bu bo'lim faqat adminlar uchun! Sizga ruxsat berilmagan.")
            return # Handlerga o'tkazib yubormaymiz (bloklaymiz)
        
        return await handler(event, data)