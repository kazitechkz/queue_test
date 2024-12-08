from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.app_settings import app_settings, AppSettings
from app.core.seed_database import seed_database


engine_async = create_async_engine(
    app_settings.DB_URL_ASYNC,
    echo=False,
    pool_size=app_settings.DB_POOL_SIZE,
    max_overflow=app_settings.DB_MAX_OVERFLOW,
    pool_timeout=app_settings.DB_POOL_TIMEOUT,
    pool_recycle=app_settings.DB_POOL_RECYCLE,
)

AsyncSessionLocal = sessionmaker(
    bind=engine_async, class_=AsyncSession, expire_on_commit=False
)


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


class Base(DeclarativeBase):
    pass


async def init_db() -> None:
    async with engine_async.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        await seed_database(session)
