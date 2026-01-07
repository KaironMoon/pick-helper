from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config import settings


def get_database_url() -> str:
    return f"postgresql+asyncpg://{settings.db.user}:{settings.db.password}@{settings.db.host}:{settings.db.port}/{settings.db.name}"


engine = create_async_engine(get_database_url(), echo=False)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    async with async_session() as session:
        yield session
