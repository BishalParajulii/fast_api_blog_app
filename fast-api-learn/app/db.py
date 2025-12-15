from collections.abc import AsyncGenerator
import uuid
from datetime import datetime

from sqlalchemy import String, Text, DateTime , Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

DATABASE_URL = "sqlite+aiosqlite:///./db.sqlite3"


# ✅ Create Base (MANDATORY)
class Base(DeclarativeBase):
    pass


# ✅ Model
class Post(Base): 
    __tablename__ = "posts" 
    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4) 
    caption = Column(Text) 
    url = Column(String) 
    file_type = Column(String, nullable=False) 
    file_name = Column(String,nullable=False) 
    created_at = Column(DateTime, default=datetime.utcnow)


# ✅ Engine
engine = create_async_engine(DATABASE_URL, echo=True)

# ✅ Session maker (DO NOT shadow name)
AsyncSessionLocal = async_sessionmaker(
    engine, expire_on_commit=False
)


# ✅ Create tables
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# ✅ Dependency
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
