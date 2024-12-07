from fastapi import APIRouter, HTTPException, Depends
from core.database import get_db
from databases.create_records import CreateRecords, get_create_records
from  databases.get_records import GetRecords, get_records
from sqlalchemy.ext.asyncio import AsyncSession
from utils.security import verify_password
from core.jwt import create_access_token
from .schemas import RegisterRequest, TokenResponse, RegisterResponse, ChangePasswordRequest, ChangeUsernameRequest
from fastapi.security import OAuth2PasswordRequestForm
from databases.models import User
from core.jwt import get_current_user
from databases.models import User
from databases.get_records import GetRecords, get_records
from utils.security import hash_password

router = APIRouter()


@router.post("/register", tags=['Auth'], response_model=RegisterResponse)
async def register_user(
    request: RegisterRequest, 
    create_records: CreateRecords = Depends(get_create_records),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    get_records: GetRecords = Depends(get_records)
):
    """
    Allows Admins and Managers to register new users. Managers can only register users with the 'User' role.
    """
    try:
        role_name = await get_records.get_role_name_by_id(db=db, role_id=current_user.role_id)
        if role_name not in ["Admin", "Manager"]:
            raise HTTPException(status_code=403, detail="Only Admins and Managers can register new users")
        
        new_user_role = await get_records.get_role_by_name(db, request.role)

        if role_name == "Manager":
            if new_user_role.name != "User":
                raise HTTPException(status_code=403, detail="Managers can only register users")
    
        await create_records.create_user(db=db, username=request.username, password=request.password, role_name=request.role, current_user_id=current_user.id, owner_role_name=role_name)

        return RegisterResponse(message="User registered successfully")
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login", tags=['Auth'], response_model=TokenResponse)
async def login_user(
    request: OAuth2PasswordRequestForm = Depends(),
    get_records: GetRecords = Depends(get_records),
    db: AsyncSession = Depends(get_db),
):
    """
    Authenticates a user and returns an access token upon successful login.
    """
    try:
        user = await get_records.get_user_by_username(db, request.username)
        if not verify_password(request.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid username or password")

        access_token = create_access_token(data={"sub": user.username, "role": user.role.name})
        return TokenResponse(access_token=access_token)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/change-password", tags=["Auth"], response_model=RegisterResponse)
async def change_password(
    request: ChangePasswordRequest, 
    db: AsyncSession = Depends(get_db),
    get_records: GetRecords = Depends(get_records),
    current_user: User = Depends(get_current_user),
):
    """
    Allows the currently logged-in user to change their password by verifying the previous password first.
    """
    try:
        user = await get_records.get_user_by_username(db, current_user.username)

        if not verify_password(request.previous_password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid password")

        user.password_hash = hash_password(request.new_password)
        db.add(user)
        await db.commit()

        return RegisterResponse(message="Password changed successfully")
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/change-username", tags=["Auth"], response_model=RegisterResponse)
async def change_username(
    request: ChangeUsernameRequest,
    db: AsyncSession = Depends(get_db),
    get_records: GetRecords = Depends(get_records),
    current_user: User = Depends(get_current_user),
):
    """
    Allows the currently logged-in user to change their username.
    """
    try:
        user = await get_records.get_user_by_username(db, current_user.username)

        user.username = request.new_username
        db.add(user)
        await db.commit()

        return RegisterResponse(message="Username changed successfully")
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))