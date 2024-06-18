from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.config import settings

DATABASE_URL = f"postgresql+asyncpg://" \
               f"{settings.DB_USER}:" \
               f"{settings.DB_PASS}@" \
               f"{settings.DB_HOST}:" \
               f"{settings.DB_PORT}/" \
               f"{settings.DB_NAME}"

engine = create_async_engine(url=DATABASE_URL)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
