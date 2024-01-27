from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DATABASE_URL = "sqlite+aiosqlite:///./ecommerce.db"
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True,
    connect_args={"check_same_thread": False},
)
engine.connect()
Base = declarative_base()

metadata = MetaData()


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


AsyncSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)
