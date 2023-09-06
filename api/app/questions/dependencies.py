from fastapi import HTTPException
from bson import ObjectId

async def validate_object_id(id: str) -> str:
    if not ObjectId.is_valid(id):
        raise HTTPException(404, 'Question not found.')
    return id