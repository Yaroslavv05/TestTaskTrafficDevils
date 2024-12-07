from datetime import datetime, timedelta
from typing import Optional
import jwt
from dotenv import load_dotenv
import os
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from sqlalchemy.future import select
from databases.models import User

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        return None


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=401, detail="Could not validate credentials"
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    username = payload.get("sub")
    if username is None:
        raise credentials_exception

    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if not user:
        raise credentials_exception

    return user