"""
DB Session script
"""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, \
    AsyncEngine
from core.config import settings

async_engine: AsyncEngine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True, future=True,
    echo=True)


async def get_session(engine: AsyncEngine = async_engine):
    """
    Get connection session to the database
    :return session: Async session for database connection
    :rtype session: AsyncSession
    """
    async with AsyncSession(
            bind=engine, expire_on_commit=False) as async_session:
        return async_session
