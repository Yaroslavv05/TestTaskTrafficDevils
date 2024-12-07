from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from databases.models import User, Role, Request
from fastapi import HTTPException
from utils.security import hash_password

class CreateRecords:
    async def create_user(self, db: AsyncSession, username: str, password: str, role_name: str) -> User:
        role_query = select(Role).where(Role.name == role_name)
        role_result = await db.execute(role_query)
        role = role_result.scalars().first()
        if not role:
            raise HTTPException(status_code=400, detail="Invalid role")

        user_query = select(User).where(User.username == username)
        user_result = await db.execute(user_query)
        existing_user = user_result.scalars().first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already registered")

        hashed_password = hash_password(password)
        new_user = User(username=username, password_hash=hashed_password, role_id=role.id)
        db.add(new_user)
        await db.commit()
        return new_user

    async def create_request(self, db: AsyncSession, bottoken: str, chatid: str, message: str, response_text: str, current_user: User):
        try:
            log_entry = Request(
                bottoken=bottoken,
                chatid=chatid,
                message=message,
                telegram_response=response_text,
                user_id=current_user.id,
            )
            db.add(log_entry)
            await db.commit()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error logging request: {str(e)}")

async def get_create_records():
    return CreateRecords()