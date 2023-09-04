from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends
from fastapi_pagination import Page, paginate

from app.models import User, Question
from app.database import QuestionController, TagController
from app.dependencies import validate_object_id
from app.auth.dependencies import get_current_user

router = APIRouter(
    prefix='/questions', 
    tags=['questions'], 
    responses={404: {"description": "Not found"}}
)

@router.get('/', status_code=200, response_model=Page[Question])
async def get_questions(limit: int = 1000, tag: str | None = None):
    if limit <= 0:
        raise HTTPException(400, "The 'limit' parameter cannot be a negative number.")

    if tag:
        response = await TagController.get_by_name(tag)
        if not response:
            raise HTTPException(400, 'The tag does not exist.')

        questions = await QuestionController.get_by_tag(tag, limit)
    else:
        questions = await QuestionController.get_all(limit)

    return paginate(questions)
    

@router.get('/{id}', status_code=200, response_model=Question)
async def get_question(id: str = Depends(validate_object_id)):
    question = await QuestionController.get_by_id(id) 
    if question:
        return question
    
    raise HTTPException(404, 'Question not found.')

@router.get('/{id}/votes', status_code=200, response_model=Question)
async def manage_votes(
    id: str = Depends(validate_object_id),
    vote: str | None = None,
    user: User = Depends(get_current_user)
):
    question_found = await QuestionController.get_by_id(id)
    if not question_found:
        raise HTTPException(404, 'Question not found.')

    if vote in ('up', 'down'):
        response = await QuestionController.add_vote(id, user.id, vote)
        if response:
            return response
        raise HTTPException(422, 'The request could not be processed.')
    elif vote == 'remove':
        response = await QuestionController.remove_vote(id, user.id)
        if response:
            return response
        raise HTTPException(422, 'The request could not be processed.')

    raise HTTPException(status_code=400, detail="Invalid vote value")

@router.post('/ask', status_code=201, response_model=Question)
async def create_question(
    question: Question,
    user: User = Depends(get_current_user)
):
    response = await TagController.get_by_name(question.tag)
    if not response:
        raise HTTPException(400, 'The tag does not exist.')

    question.author_id = user.id
    question = question.model_dump()

    response = await QuestionController.create(question)
    if response:
        return response

    raise HTTPException(400, 'Something went wrong')


@router.patch('/{id}', status_code=200, response_model=Question)
async def update_question(
    question: Question,
    id: str = Depends(validate_object_id),
    user: User = Depends(get_current_user)
):
    response = await QuestionController.get_by_id(id)
    if not response:
        raise HTTPException(404, 'Question not found.')

    update_data = question.model_dump(exclude_unset=True)
    update_data['updated_at'] = datetime.now()
    response = await QuestionController.update(id, update_data)
    if response:
        return response

    raise HTTPException(status_code=500, detail='Failed to update question data.')

@router.delete('/{id}', status_code=204)
async def delete_question(
    id: str = Depends(validate_object_id),
    user: User = Depends(get_current_user)
):
    question = await QuestionController.get_by_id(id)
    if not question:
        raise HTTPException(404, 'Question not found.')

    if question['author_id'] != user.id:
        raise HTTPException(status_code=403, detail="You do not have permission to delete this question.")

    response = await QuestionController.delete(id)
    if response:
        return None

    raise HTTPException(status_code=500, detail='Failed to delete question data.')

@router.get('/{id}/answers', status_code=200) # Incompleted
async def get_answers(id: str = Depends(validate_object_id)):
    return {'message': 'Hello World'}