from database.session import AsyncSessionLocal
from database.models.models_list import UserData
from sqlalchemy.dialects.sqlite import insert
from datetime import datetime, UTC


async def add_user(tg_id: int, username: str):
    async with AsyncSessionLocal() as session:
        stmt = (
            insert(UserData)
            .values(tg_id=tg_id, username=username, created_at=datetime.now(UTC))
            .on_conflict_do_nothing()
        )
        await session.execute(stmt)
        await session.commit()
