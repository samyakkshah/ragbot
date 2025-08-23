from typing import Literal
from collections.abc import AsyncGenerator
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import text
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from config import config
from local_logs.logger import logger
from models import Base


class DatabaseConfig(BaseModel):
    kind: Literal["postgres", "supabase"]
    dsn: str


class DBManager:
    def __init__(self, db_config: DatabaseConfig):
        # Async engine using psycopg3
        self.engine: AsyncEngine = create_async_engine(db_config.dsn, echo=config.DEBUG)
        self.session_factory = async_sessionmaker(
            bind=self.engine, expire_on_commit=False
        )

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session

    async def test_postgres(self) -> bool:
        try:
            async with self.engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            logger.error(f"Test Postgres Error: {e}")
            return False

    async def init_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
