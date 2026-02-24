from database.session import AsyncSessionLocal
from sqlalchemy import insert
from database.models.models_list import GameHistory
from datetime import datetime, UTC


async def add_game_to_history(
    user_id: int, game_type: str, game_result: bool, chat_id: int
):
    async with AsyncSessionLocal() as session:
        stmt = insert(GameHistory).values(
            user_id=user_id,
            game_type=game_type,
            game_result=game_result,
            chat_id=chat_id,
            created_at=datetime.now(UTC),
        )
        await session.execute(stmt)

        await session.commit()
