from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.core.app_settings import app_settings

engine_async = create_async_engine(
    app_settings.DB_URL_ASYNC,
    echo=False,
)

AsyncSessionLocal = sessionmaker(
    bind=engine_async,
    class_=AsyncSession,
    expire_on_commit=False
)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    from app.domain.models.role_model import RoleModel
    from app.domain.models.user_type_model import UserTypeModel
    from app.domain.models.user_model import UserModel

    async with engine_async.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
