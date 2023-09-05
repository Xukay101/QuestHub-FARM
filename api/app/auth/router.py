from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.models import User
from app.database import UserController
from app.auth.schemas import TokenSchema
from app.auth.dependencies import get_current_user_refresh
from app.auth.utils import (
    get_hashed_password,
    create_access_token,
    create_refresh_token,
    verify_password
)

router = APIRouter(prefix='/auth', tags=['auth'], responses={404: {"description": "Not found"}})

@router.get('/')
async def root():
    return {'message': 'this is auth router'}

@router.post('/login', status_code=200, response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await UserController.get_by_username(form_data.username)
    if not user:
        raise HTTPException(401, 'Incorrect username or password')

    if not verify_password(form_data.password, user['password']):
        raise HTTPException(401, 'Incorrect username or password')

    return {
        'access_token': create_access_token(user['username']),
        'refresh_token': create_refresh_token(user['username']),
    }

@router.post('/signup', status_code=201, response_model=User)
async def signup(user: User):
    # Check if existing
    userFound = await UserController.get_by_username(user.username)
    if userFound:
        raise HTTPException(409, 'User already exists')

    # Convert Password
    user = user.model_dump()
    user['password'] = get_hashed_password(user['password'])

    # Create user
    response = await UserController.create(user)
    if response:
        return response

    raise HTTPException(400, 'Something went wrong')

# This endpoint renew access token
@router.post("/refresh-token")
async def refresh_token(user: User = Depends(get_current_user_refresh)):
    new_access_token = create_access_token(user.username) 
    return {"access_token": new_access_token}

@router.put('/change-password')
async def change_password():
    '''
    {
        "current_password": "contraseña_actual",
        "new_password": "nueva_contraseña"
    }
    '''
    return {'message': 'Password changed successfully.'}

