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
session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    future=True,
)


@asynccontextmanager
async def get_session():
    async with session() as session_:
        try:
            yield session_
        except Exception as e:
            await session_.rollback()
            raise e
