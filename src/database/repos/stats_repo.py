from database.models.models_list import GameHistory, UserData
from database.session import AsyncSessionLocal
from sqlalchemy import select, func, case


async def get_user_stats(user_id: int, game_type: str):
    async with AsyncSessionLocal() as session:
        stmt = (
            select(GameHistory.user_id, func.count(GameHistory.game_result))
            .where(GameHistory.user_id == user_id, GameHistory.game_type == game_type)
            .group_by(GameHistory.game_result)
        )
        result = await session.execute(stmt)
        result = result.all()
        print(result)
        try:
            total_games = result[0][1] + result[1][1]
            wins = result[1][1]
            winrate = wins / total_games * 100
            return total_games, wins, winrate
        except IndexError:
            total_games = result[0][1]
            wins = result[0][1]
            winrate = wins / total_games * 100
            return total_games, wins, winrate


async def get_leaderboard_stats(game_type: str):
    async with AsyncSessionLocal() as session:
        wins = func.sum(case((GameHistory.game_result.is_(True), 1), else_=0)).label(
            "wins"
        )
        total_games = func.count(GameHistory.id).label("total_games")
        stmt = (
            select(UserData.username, wins, total_games)
            .join(GameHistory, UserData.tg_id == GameHistory.user_id)
            .filter(GameHistory.game_type == game_type)
            .group_by(UserData.tg_id, UserData.username)
            .order_by(wins.desc())
            .limit(10)
        )
        result = (await session.execute(stmt)).all()
        return result
