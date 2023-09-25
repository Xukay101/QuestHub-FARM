from fastapi import APIRouter, HTTPException, Depends
from fastapi_pagination import Page, paginate

from app.database import QuestionController, AnswerController, UserSettingsController
from app.models import User, Question, Answer, UserSettings
from app.users.schemas import UserPublic
from app.users.dependencies import get_user_by_username, get_user_by_id
from app.auth.dependencies import get_current_user

router = APIRouter(
    prefix='/users', 
    tags=['users'], 
    responses={404: {"description": "Not found"}}
)

@router.get('/{username}', status_code=200, response_model=UserPublic)
async def get_public_profile(requested_user: User = Depends(get_user_by_username)):
    return requested_user 

@router.get('/{username}/questions', status_code=200, response_model=Page[Question])
async def get_user_questions(
    requested_user: User = Depends(get_user_by_username),
    limit: int = 1000
):
    questions = await QuestionController.get_by_author(requested_user.id, limit)
    return paginate(questions)

@router.get('/{username}/answers', status_code=200, response_model=Page[Answer])
async def get_user_answers(
    requested_user: User = Depends(get_user_by_username),
    limit: int = 1000
):
    answers = await AnswerController.get_by_author(requested_user.id, limit)
    return paginate(answers)

@router.get('/{username}/configuration', status_code=200, response_model=UserSettings)
async def get_user_settings(
    requested_user: User = Depends(get_user_by_username),
    current_user: User = Depends(get_current_user),
):
    if current_user.id != requested_user.id:
        raise HTTPException(403, "You do not have permission to access this setting.")

    user_settings = await UserSettingsController.get_by_id(current_user.settings_id)
    return user_settings

@router.get('/{id}/username', status_code=200)
async def get_username(requested_user: User = Depends(get_user_by_id)):
    username = requested_user.username
    return {'username': username}

