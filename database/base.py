from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

import settings

Base = declarative_base()
engine = create_async_engine(
    settings.database.database_url,
    future=True,
    echo=settings.database.echo,
)
session_factory = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    future=True,
)


@asynccontextmanager
async def get_session():
    async with session_factory() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
