from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from databases.models import User
from fastapi import HTTPException

class GetRecords:
    async def get_user_by_username(self, db: AsyncSession, username: str) -> User:
        query = select(User).options(joinedload(User.role)).where(User.username == username)
        result = await db.execute(query)
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid username or password")
        return user


async def get_records():
    return GetRecords()