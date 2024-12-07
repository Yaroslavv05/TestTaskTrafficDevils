from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from databases.models import Base
from databases.models import Role
import os
from sqlalchemy.future import select

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


async def init_db_roles(db: AsyncSession):
    roles = ["Manager", "User", "Admin"]
    for role_name in roles:
        existing_role = await db.execute(select(Role).where(Role.name == role_name))
        if not existing_role.scalar():
            new_role = Role(name=role_name)
            db.add(new_role)
    await db.commit()