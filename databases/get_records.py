from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from databases.models import User, Request
from fastapi import HTTPException

class GetRecords:
    async def get_user_by_username(self, db: AsyncSession, username: str) -> User:
        query = select(User).options(joinedload(User.role)).where(User.username == username)
        result = await db.execute(query)
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid username or password")
        return user

    async def get_all_requests(self, db: AsyncSession) -> list[Request]:
        query = select(Request).options(joinedload(Request.user))
        result = await db.execute(query)
        requests = result.scalars().all()
        if not requests:
            raise HTTPException(status_code=404, detail="No requests found")
        return requests

    async def get_requests_by_role(self, db: AsyncSession, current_user: User) -> list[Request]:
        query = select(Request).where(
            Request.user_id.in_(
                select(User.id).where(User.role_id == current_user.role_id)
            )
        ).options(joinedload(Request.user))
        
        result = await db.execute(query)
        requests = result.scalars().all()
        
        if not requests:
            raise HTTPException(status_code=404, detail="No requests found for this role")
        return requests

    async def get_user_requests(self, db: AsyncSession, current_user: User) -> list[Request]:
        query = select(Request).where(
            Request.user_id == current_user.id
        ).options(joinedload(Request.user))
        
        result = await db.execute(query)
        requests = result.scalars().all()
        
        if not requests:
            raise HTTPException(status_code=404, detail="No requests found for this user")
        return requests

async def get_records():
    return GetRecords()