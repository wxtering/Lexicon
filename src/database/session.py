from sqlalchemy.ext.asyncio.session import AsyncSession


from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from configuration.config import get_database_config

dbconfig = get_database_config()


engine = create_async_engine(dbconfig.db_url, echo=dbconfig.db_echo)

AsyncSessionLocal = async_sessionmaker[AsyncSession](engine, expire_on_commit=False)
