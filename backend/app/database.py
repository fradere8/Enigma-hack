from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Получаем URL БД из переменных окружения (в docker-compose пропишем позже)
# Пример: postgresql+asyncpg://user:password@db/support_db
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost/support_db")

engine = create_async_engine(DATABASE_URL, echo=True)

# Фабрика сессий
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

# Функция для получения сессии в эндпоинтах (Dependency Injection)
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session