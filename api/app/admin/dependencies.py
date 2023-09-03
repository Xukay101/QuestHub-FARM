from datetime import datetime
from typing import Union, Any

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from jose import jwt

from app.config import settings
from app.models import Admin
from app.database import AdminController
from app.auth.schemas import TokenPayload


reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/admin/login",
    scheme_name="JWT"
)

async def get_current_admin(token: str = Depends(reuseable_oauth)) -> Admin:
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
        
    admin: Union[dict[str, Any], None] = await AdminController.get_by_username(token_data.sub)

    if admin is None:
        raise HTTPException(
            status_code=404,
            detail="Could not find admin",
        )
    
    return Admin(**admin)