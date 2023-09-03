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
    async def get_all(cls, limit: int | None = None) -> List[BaseModel]:
        documents = []

        if not limit:
            cursor: AsyncIOMotorCursor = cls.collection.find({}).sort('created_at', -1)
        else:
            cursor: AsyncIOMotorCursor = cls.collection.find({}).sort('created_at', -1).limit(limit)

        async for doc in cursor:
            documents.append(cls.model(**doc))
        return documents

    @classmethod
    async def create(cls, data: dict) -> dict:
        new_document = await cls.collection.insert_one(data)
        id = new_document.inserted_id
        created_document = await cls.update(str(id), {'id': str(id)})
        created_document['_id'] = str(created_document['_id'])
        return created_document

    @classmethod
    async def update(cls, id: str, data: dict) -> dict:
        await cls.collection.update_one({'_id': ObjectId(id)}, {'$set': data})
        document = await cls.collection.find_one({'_id': ObjectId(id)})
        return document

    @classmethod
    async def delete(cls, id: str) -> bool:
        result = await cls.collection.delete_one({'_id': ObjectId(id)})
        return result.deleted_count > 0

    @classmethod
    async def get_collection(cls) -> AsyncIOMotorCollection:
        return cls.collection


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
    async def get_by_tag(cls, tag: str, limit: int | None = None) -> List[Question]:
        if not limit:
            cursor = cls.collection.find({'tags': {'$in': [tag]}}).sort('created_at', -1)
        else:
            cursor = cls.collection.find({'tags': {'$in': [tag]}}).sort('created_at', -1).limit(limit)

        questions = []
        async for doc in cursor:
            questions.append(cls.model(**doc))
        return questions

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
    async def get_by_name(cls, name: str) -> dict:
        tag = await cls.collection.find_one({'name': name})
        return tag