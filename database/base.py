from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

import settings

Base = declarative_base()
engine = create_async_engine(
    settings.database_settings.database_url,
    future=True,
)
session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    future=True,
)
