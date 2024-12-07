from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from databases.models import Base
from databases.models import Role, User
import os
from sqlalchemy.future import select
from databases.create_records import CreateRecords
from fastapi import HTTPException

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

async def init_db_roles_and_admin(db: AsyncSession):
    create_records = CreateRecords()

    roles = ["Manager", "User", "Admin"]
    for role_name in roles:
        try:
            await create_records.create_role(db, role_name)
        except HTTPException as e:
            if e.status_code != 400:
                raise e

    admin_role_query = select(Role).where(Role.name == "Admin")
    admin_role_result = await db.execute(admin_role_query)
    admin_role = admin_role_result.scalar()

    if admin_role:
        existing_admin_query = select(User).where(User.role_id == admin_role.id)
        existing_admin_result = await db.execute(existing_admin_query)
        if not existing_admin_result.scalar():
            await create_records.create_user(
                db=db,
                username=os.getenv('ADMIN_USERNAME'),
                password=os.getenv('ADMIN_PASSWORD'),
                role_name="Admin"
            )