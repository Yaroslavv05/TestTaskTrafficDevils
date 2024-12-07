from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from databases.models import User
from utils.telegram import send_telegram_message
from core.jwt import get_current_user
from .schemas import RequestData, DataResponse
from databases.get_records import GetRecords, get_records
from databases.create_records import CreateRecords, get_create_records

router = APIRouter()

@router.post("/create_request", tags=["Requests"], response_model=DataResponse)
async def process_request(
    request_data: RequestData,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    create_records: CreateRecords = Depends(get_create_records)
):
    """
    Sends a message via Telegram and saves the request and its response to the database.
    """
    try:
        response = await send_telegram_message(request_data.bottoken, request_data.chatid, request_data.message)
        response_text = response.get("result", {}).get("text", "No response text")

        await create_records.create_request(db=db, bottoken=request_data.bottoken, chatid=request_data.chatid, message=request_data.message, response_text=response_text, current_user=current_user)
            
        return DataResponse(status='success', response=response_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get_requests", tags=["Requests"])
async def get_request(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    get_records: GetRecords = Depends(get_records)
):
    """
    Fetches requests based on user role: all for admins, specific users' requests for managers, and personal requests for regular users.
    """
    try:
        role_name = await get_records.get_role_name_by_id(db=db, role_id=current_user.role_id)
        if role_name == 'Admin':
            logs = await get_records.get_all_requests(db)
        elif role_name == 'Manager':
            logs = await GetRecords().get_requests_of_users_managed_by(db, current_user.id)
        elif role_name == 'User':
            logs = await get_records.get_user_requests(db, current_user)
        
        return logs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))