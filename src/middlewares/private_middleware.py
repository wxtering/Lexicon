from typing import Callable, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from aiogram.enums import ChatType


class PrivateChatMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        if isinstance(event, Message):
            if event.chat.type == ChatType.PRIVATE:
                result = await handler(event, data)
                return result
        elif isinstance(event, CallbackQuery):
            if event.message.chat.type == ChatType.PRIVATE:
                result = await handler(event, data)
                return result
        return None
