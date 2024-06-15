from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config import config


Base = declarative_base()

engine = create_async_engine(
    config.DATABASE_URL,
    pool_timeout=config.POOL_TIMEOUT,
    pool_size=config.POOL_SIZE,
)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session
