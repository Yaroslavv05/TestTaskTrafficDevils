from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from databases.models import Base
import os

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_async_engine(DATABASE_URL, future=True, echo=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)