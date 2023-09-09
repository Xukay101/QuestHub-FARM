from fastapi import HTTPException

from app.database import UserController
from app.models import User

async def get_user_by_username(username: str):
    user = await UserController.get_by_username(username)
    if user:
        return User(**user)

    raise HTTPException(status_code=404, detail="Could not find user")