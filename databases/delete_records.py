from sqlalchemy.ext.asyncio import AsyncSession
from databases.models import User
from sqlalchemy.sql import delete

class DeleteRecords:
    async def delete_user(self, db: AsyncSession, user_id: int):
        """
        Deletes a user by their ID from the database.
        """
        await db.execute(delete(User).where(User.id == user_id))
        await db.commit()

async def get_delete_records():
    return DeleteRecords()