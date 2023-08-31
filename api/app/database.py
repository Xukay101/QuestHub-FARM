from typing import List

from pydantic import BaseModel
from bson import ObjectId
from motor.motor_asyncio import (
    AsyncIOMotorClient, 
    AsyncIOMotorCollection, 
    AsyncIOMotorCursor
)

from app.config import settings
from app.models import User, Question, Answer, Tag

# Conections
client = AsyncIOMotorClient(settings.MONGODB_URI)
database = client[settings.MONGODB_NAME]

# Controllers
class BaseController:
    model: BaseModel
    collection: AsyncIOMotorCollection

    @classmethod
    async def get_by_id(cls, id: str) -> dict:
        document = await cls.collection.find_one({'_id': ObjectId(id)})
        return document

    @classmethod
    async def get_all(cls) -> List[BaseModel]:
        documents = []
        cursor: AsyncIOMotorCursor = cls.collection.find({})
        async for doc in cursor:
            documents.append(cls.model(**doc))
        return documents

    @classmethod
    async def create(cls, data: dict) -> dict:
        new_document = await cls.collection.insert_one(data)
        created_document = await cls.collection.find_one({'_id': new_document.inserted_id})
        created_document['_id'] = str(created_document['_id'])
        return created_document

    @classmethod
    async def update(cls, id: str, data: dict) -> dict:
        await cls.collection.update_one({'_id': id}, {'$set': data})
        document = await cls.collection.find_one({'_id': id})
        return document

    @classmethod
    async def delete(cls, id: str) -> bool:
        result = await cls.collection.delete_one({'_id': id})
        return result.deleted_count > 0

class UserController(BaseController):
    model = User
    collection = database['users']

    @classmethod
    async def get_by_username(cls, username: str) -> dict:
        user = await cls.collection.find_one({'username': username})
        return user

class QuestionController(BaseController):
    model = Question
    collection = database['questions']

    @classmethod
    async def get_answers(cls) -> List[Answer]:
        pass

class AnswerController(BaseController):
    model = Answer
    collection = database['answers']

class TagController(BaseController):
    model = Tag
    collection = database['tags']

    @classmethod
    async def get_questions(cls) -> List[Question]:
        pass