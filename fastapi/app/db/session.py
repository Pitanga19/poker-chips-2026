from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator
from app.core.config import settings
from app.db.base import Base

# Motor asíncrono de SQLAlchemy
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
)

# Sesión asíncrona de SQLAlchemy
SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Función para obtener la sesión de la base de datos
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
