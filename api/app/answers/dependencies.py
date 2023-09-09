from fastapi import HTTPException
from bson import ObjectId

from app.models import Answer

async def validate_object_id(id: str) -> str:
    if not ObjectId.is_valid(id):
        raise HTTPException(404, 'Answer not found.')
    return id

async def validate_answer(answer: Answer) -> Answer:
    if not ObjectId.is_valid(answer.question_id):
        raise HTTPException(404, 'Question id not found.')

    return answer 