from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from database.repos.user_repo import add_user
from typing import Callable, Any, Awaitable


class AddUserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user = data.get("event_from_user")
        if user:
            await add_user(user.id, user.username)
        return await handler(event, data)
