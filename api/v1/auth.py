from fastapi import APIRouter, HTTPException, Depends
from core.database import get_db
from databases.create_records import CreateRecords, get_create_records
from  databases.get_records import GetRecords, get_records
from sqlalchemy.ext.asyncio import AsyncSession
from utils.security import verify_password
from core.jwt import create_access_token
from .schemas import RegisterRequest, TokenResponse, RegisterResponse
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/register", tags=['Auth'], response_model=RegisterResponse)
async def register_user(
    request: RegisterRequest, 
    create_records: CreateRecords = Depends(get_create_records),
    db: AsyncSession = Depends(get_db)
):
    try:
        await create_records.create_user(db, request.username, request.password, request.role)
        return RegisterResponse(message="User registered successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login", tags=['Auth'], response_model=TokenResponse)
async def login_user(
    request: OAuth2PasswordRequestForm = Depends(),
    get_records: GetRecords = Depends(get_records),
    db: AsyncSession = Depends(get_db),
):
    try:
        user = await get_records.get_user_by_username(db, request.username)
        if not verify_password(request.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid username or password")

        access_token = create_access_token(data={"sub": user.username, "role": user.role.name})
        return TokenResponse(access_token=access_token)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))