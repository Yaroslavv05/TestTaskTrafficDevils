from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from databases.models import User, Request, Role
from fastapi import HTTPException

class GetRecords:
    async def get_user_by_username(self, db: AsyncSession, username: str) -> User:
        """
        Fetch user by username and ensure the user exists.
        Raises HTTPException if the user doesn't exist.
        """
        query = select(User).options(joinedload(User.role)).where(User.username == username)
        result = await db.execute(query)
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid username or password")
        return user

    async def get_all_requests(self, db: AsyncSession) -> list[Request]:
        """
        Retrieves all requests from the database.
        Raises HTTPException if no requests are found.
        """
        query = select(Request).options(joinedload(Request.user))
        result = await db.execute(query)
        requests = result.scalars().all()
        if not requests:
            raise HTTPException(status_code=404, detail="No requests found")
        return requests

    async def get_user_requests(self, db: AsyncSession, current_user: User) -> list[Request]:
        """
        Retrieves requests only for the currently logged-in user.
        Raises HTTPException if no requests are found for the user.
        """
        query = select(Request).where(
            Request.user_id == current_user.id
        ).options(joinedload(Request.user))
        
        result = await db.execute(query)
        requests = result.scalars().all()
        
        if not requests:
            raise HTTPException(status_code=404, detail="No requests found for this user")
        return requests
    
    async def get_role_name_by_id(self, db: AsyncSession, role_id: int) -> str:
        """
        Retrieves the name of a role based on its ID.
        Raises HTTPException if the role is not found.
        """
        query = select(Role.name).where(Role.id == role_id)
        result = await db.execute(query)
        role_name = result.scalar()
        if not role_name:
            raise HTTPException(status_code=404, detail=f"Role with ID {role_id} not found")
        return role_name

    async def get_role_by_name(self, db: AsyncSession, role_name: str) -> Role:
        """
        Fetches a role by its name.
        Raises HTTPException if the role does not exist.
        """
        query = select(Role).where(Role.name == role_name)
        result = await db.execute(query)
        role = result.scalar()
        if not role:
            raise HTTPException(status_code=400, detail="Invalid role specified")
        return role
    
    async def get_requests_of_users_managed_by(self, db: AsyncSession, manager_id: int) -> list[Request]:
        """
        Retrieves requests of users managed by the given manager.
        Raises HTTPException if no requests are found for those users.
        """
        query = (
            select(Request)
            .join(User, Request.user_id == User.id)
            .where(User.admin_id == manager_id) 
            .options(joinedload(Request.user)) 
        )
        result = await db.execute(query)
        requests = result.scalars().all()

        if not requests:
            raise HTTPException(status_code=404, detail="No requests found for users managed by this manager")

        return requests
    
    async def get_user_by_id(self, db: AsyncSession, user_id: int) -> User:
        """
        Fetches a user by their unique ID.
        Returns None if the user does not exist.
        """
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar()
        return user

async def get_records():
    return GetRecords()