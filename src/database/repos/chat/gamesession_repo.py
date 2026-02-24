from database.session import AsyncSessionLocal
from database.models.models_list import GameSessions
from sqlalchemy import select, delete, update
from typing import Any


async def add_game_session(
    game_type: str,
    chat_id: int,
    session_info: dict = {},
):
    async with AsyncSessionLocal() as session:
        game_session = GameSessions(
            chat_id=chat_id,
            game_type=game_type,
            session_info=session_info,
        )
        session.add(game_session)
        await session.commit()


async def get_game_session(
    game_type: str,
    chat_id: int,
) -> dict[str, Any]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(GameSessions.session_info).where(
                GameSessions.chat_id == chat_id, GameSessions.game_type == game_type
            )
        )
        return result.scalar_one()


async def clear_game_session(chat_id: int, game_type: str):
    async with AsyncSessionLocal() as session:
        await session.execute(
            delete(GameSessions).where(
                GameSessions.chat_id == chat_id, GameSessions.game_type == game_type
            )
        )
        await session.commit()


async def update_game_session(chat_id: int, game_type: str, session_info: dict):
    async with AsyncSessionLocal() as session:
        await session.execute(
            update(GameSessions)
            .where(GameSessions.chat_id == chat_id, GameSessions.game_type == game_type)
            .values(session_info=session_info)
        )
        await session.commit()
