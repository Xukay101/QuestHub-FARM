from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException

from app.models import Answer, User
from app.database import QuestionController, AnswerController
from app.auth.dependencies import get_current_user
from app.answers.dependencies import validate_answer, validate_object_id

router = APIRouter(
    prefix='/answers', 
    tags=['answers'], 
    responses={404: {"description": "Not found"}}
)

@router.post('/', status_code=201, response_model=Answer)
async def create_answer(
        answer: Answer = Depends(validate_answer),
        user: User = Depends(get_current_user)
):
    question = await QuestionController.get_by_id(answer.question_id)
    if not question:
        raise HTTPException(400, 'The question does not exist.')

    if question['author_id'] == user.id:
        raise HTTPException(409, 'You cannot answer your own question.')

    answer.author_id = user.id
    response = await AnswerController.create(answer.model_dump())
    if response:
        return response

    raise HTTPException(400, 'Something went wrong.')


@router.patch('/{id}', status_code=200, response_model=Answer)
async def update_answer(
    answer: Answer,
    id: str = Depends(validate_object_id),
    user: User = Depends(get_current_user)
):
    response = await AnswerController.get_by_id(id)
    if not response:
        raise HTTPException(404, 'Answer not found.')

    update_data = answer.model_dump(exclude_unset=True)
    update_data['updated_at'] = datetime.now()
    response = await AnswerController.update(id, update_data)
    if response:
        return response

    raise HTTPException(status_code=500, detail='Failed to update answer data.')

@router.delete('/{id}', status_code=204)
async def delete_answer(
    id: str = Depends(validate_object_id),
    user: User = Depends(get_current_user)
):
    answer = await QuestionController.get_by_id(id)
    if not answer:
        raise HTTPException(404, 'Answer not found.')

    if answer['author_id'] != user.id:
        raise HTTPException(status_code=403, detail="You do not have permission to delete this answer.")

    response = await AnswerController.delete(id)
    if response:
        return None

    raise HTTPException(status_code=500, detail='Failed to delete answer data.')

@router.get('/{id}/votes', status_code=200, response_model=Answer)
async def manage_votes(
    id: str = Depends(validate_object_id),
    vote: str | None = None,
    user: User = Depends(get_current_user)
):
    answer_found = await AnswerController.get_by_id(id)
    if not answer_found:
        raise HTTPException(404, 'Answer not found.')

    if vote in ('up', 'down'):
        response = await AnswerController.add_vote(id, user.id, vote)
        if response:
            return response
        raise HTTPException(422, 'The request could not be processed.')
    elif vote == 'remove':
        response = await AnswerController.remove_vote(id, user.id)
        if response:
            return response
        raise HTTPException(422, 'The request could not be processed.')

    raise HTTPException(status_code=400, detail="Invalid vote value")