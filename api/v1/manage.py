from fastapi import APIRouter, HTTPException, Depends
from core.database import get_db
from  databases.get_records import GetRecords, get_records
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import RegisterResponse
from databases.models import User
from core.jwt import get_current_user
from databases.models import User
from databases.get_records import GetRecords, get_records
from databases.delete_records import DeleteRecords, get_delete_records

router = APIRouter()

@router.delete("/delete-user/{user_id}", tags=["Manage"], response_model=RegisterResponse)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    get_records: GetRecords = Depends(get_records),
    current_user: User = Depends(get_current_user),
    delete_records: DeleteRecords = Depends(get_delete_records)
):
    """
    Allows admins to delete any user and managers to delete only users they created.
    """
    try:
        user_to_delete = await get_records.get_user_by_id(db, user_id)
        if not user_to_delete:
            raise HTTPException(status_code=404, detail="User not found")

        role_name = await get_records.get_role_name_by_id(db=db, role_id=current_user.role_id)

        if role_name == "Admin":
            await delete_records.delete_user(db, user_id)
            return RegisterResponse(message="User deleted successfully")

        if role_name == "Manager":
            if user_to_delete.admin_id != current_user.id:
                raise HTTPException(status_code=403, detail="Managers can only delete users they created")
            
            await delete_records.delete_user(db, user_id) 
            return RegisterResponse(message="User deleted successfully")

        raise HTTPException(status_code=403, detail="You do not have permission to delete this user")

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))