from typing import Union, Any
from datetime import datetime

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError, BaseModel

from app.database import UserController
from app.models import User
from app.config import settings
from app.auth.schemas import TokenPayload

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
    scheme_name="JWT"
)

async def get_current_user(token: str = Depends(reuseable_oauth)) -> User:
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM_TOKEN]
        )
        token_data = TokenPayload(**payload)
        
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=401,
                detail="Access Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=403,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    user: Union[dict[str, Any], None] = await UserController.get_by_username(token_data.sub)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Could not find user",
        )
    
    return User(**user)

async def get_current_user_refresh(token: str = Depends(reuseable_oauth)) -> User:
    try:
        payload = jwt.decode(
            token, settings.JWT_REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM_TOKEN]
        )
        token_data = TokenPayload(**payload)
        
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=401,
                detail="Refresh Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=403,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    user: Union[dict[str, Any], None] = await UserController.get_by_username(token_data.sub)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Could not find user",
        )
    
    return User(**user)

    
    