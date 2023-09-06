from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page, paginate

from app.models import Tag, Question
from app.database import TagController, QuestionController

router = APIRouter(
    prefix='/tags', 
    tags=['tags'], 
    responses={404: {"description": "Not found"}}
)

@router.get('/', status_code=200, response_model=Page[Tag])
async def get_tags():
    tags = await TagController.get_all()
    return paginate(tags)

@router.get('/{tag}', status_code=200, response_model=Page[Question])
async def get_questions_by_tag(tag: str, limit: int = 1000):
    tag_found = await TagController.get_by_name(tag)
    if not tag_found:
        raise HTTPException(400, 'The tag does not exist.')

    if limit <= 0:
        raise HTTPException(400, "The 'limit' parameter cannot be a negative number.")

    questions = await QuestionController.get_by_tag(tag, limit)
    return paginate(questions)