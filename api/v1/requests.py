from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from databases.models import Request, User
from utils.telegram import send_telegram_message
from core.jwt import get_current_user
from .schemas import RequestData, DataResponse
from databases.get_records import GetRecords, get_records
from databases.create_records import CreateRecords, get_create_records

router = APIRouter()

@router.post("/request", tags=["Requests"], response_model=DataResponse)
async def process_request(
    request_data: RequestData,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    create_records: CreateRecords = Depends(get_create_records)
):
    try:
        response = await send_telegram_message(request_data.bottoken, request_data.chatid, request_data.message)
        response_text = response.get("result", {}).get("text", "No response text")

        await create_records.create_request(db=db, bottoken=request_data.bottoken, chatid=request_data.chatid, message=request_data.message, response_text=response_text, current_user=current_user)
            
        return DataResponse(status='success', response=response_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/request", tags=["Requests"])
async def get_request(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    get_records: GetRecords = Depends(get_records)
):
    try:
        if current_user.role_id == 1:
            logs = await get_records.get_all_requests(db)
        elif current_user.role_id == 3:
            logs = await get_records.get_requests_by_role(db, current_user)
        elif current_user.role_id == 2:
            logs = get_records.get_user_requests(db, current_user)
        else:
            raise HTTPException(status_code=403, detail="Role does not have access")
        
        return logs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))