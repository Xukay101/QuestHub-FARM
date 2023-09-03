from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.database import AdminController, TagController
from app.models import Admin, Tag
from app.auth.schemas import TokenSchema
from app.auth.utils import (
    get_hashed_password, 
    verify_password,
    create_access_token,
    create_refresh_token
)
from app.admin.dependencies import get_current_admin

router = APIRouter(
    prefix='/admin', 
    tags=['admin'], 
    responses={404: {"description": "Not found"}}
)

@router.on_event("startup")
async def startup_event():
    response = await AdminController.get_by_username('admin')
    if response:
        return None

    admin = Admin(username='admin', password=get_hashed_password('admin'), level=0)

    response = await AdminController.create(admin.model_dump())
    if response:
        return None

    raise HTTPException(500, 'Failed to created admin user.')

@router.post('/login', status_code=200, response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    admin = await AdminController.get_by_username(form_data.username)
    if not admin:
        raise HTTPException(401, 'Incorrect username or password')

    if not verify_password(form_data.password, admin['password']):
        raise HTTPException(401, 'Incorrect username or password')

    return {
        'access_token': create_access_token(admin['username']),
        'refresh_token': create_refresh_token(admin['username']),
    }

@router.post('/tag', status_code=200, response_model=Tag)
async def create_tag(tag: Tag, admin: Admin = Depends(get_current_admin)):
    response = await TagController.get_by_name(tag.name)
    if response:
        raise HTTPException(409, 'Tag already exists')

    response = await TagController.create(tag.model_dump())
    if response:
        return response
    
    raise HTTPException(400, 'Something went wrong')