import re

from typing import List

from pydantic import BaseModel
from bson import ObjectId
from motor.motor_asyncio import (
    AsyncIOMotorClient, 
    AsyncIOMotorCollection, 
    AsyncIOMotorCursor
)

from app.config import settings
from app.models import User, UserSettings, Question, Answer, Tag, Admin

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
            cursor = cls.collection.find({'tag': tag}).sort('created_at', -1)
        else:
            cursor = cls.collection.find({'tag': tag}).sort('created_at', -1).limit(limit)

        questions = []
        async for doc in cursor:
            questions.append(cls.model(**doc))
        return questions

    @classmethod
    async def get_by_author(cls, author_id: str, limit: int | None = None) -> List[Question]:
        if not limit:
            cursor = cls.collection.find({'author_id': author_id}).sort('created_at', -1)
        else:
            cursor = cls.collection.find({'author_id': author_id}).sort('created_at', -1).limit(limit)

        questions = []
        async for doc in cursor:
            questions.append(cls.model(**doc))
        return questions

    @classmethod
    async def add_vote(cls, question_id: str, user_id: str, vote_type: str) -> dict:
        question = await cls.get_by_id(question_id)

        question['votes'][user_id] = vote_type 
        response = await cls.update(question_id, {'votes': question['votes']})
        if response:
            return response


    @classmethod
    async def remove_vote(cls, question_id: str, user_id: str) -> bool:
        question = await cls.get_by_id(question_id)

        if user_id in question['votes']:
            question['votes'].pop(user_id)
            response = await cls.update(question_id, {'votes': question['votes']})
            if response:
                return response

    @classmethod
    async def search_by_args(cls, q: str | None = None, tag: str | None = None, user: str | None = None):
        query = {}

        if q:
            words = q.split()
            regex_pattern = '|'.join(re.escape(word) for word in words)
            query['title'] = {'$regex': regex_pattern, '$options': 'i'} 

        if tag:
            query['tag'] = tag

        if user:
            user = await UserController.get_by_username(user)
            if user:
                query['author_id'] = user['id']

        questions = []
        cursor = cls.collection.find(query).sort('created_at', -1)
        async for doc in cursor:
            questions.append(cls.model(**doc))

        return questions

class AnswerController(BaseController):
    model = Answer
    collection = database['answers']

    @classmethod
    async def add_vote(cls, answer_id: str, user_id: str, vote_type: str) -> dict:
        question = await cls.get_by_id(answer_id)

        question['votes'][user_id] = vote_type 
        response = await cls.update(answer_id, {'votes': question['votes']})
        if response:
            return response

    @classmethod
    async def remove_vote(cls, answer_id: str, user_id: str) -> bool:
        question = await cls.get_by_id(answer_id)

        if user_id in question['votes']:
            question['votes'].pop(user_id)
            response = await cls.update(answer_id, {'votes': question['votes']})
            if response:
                return response

    @classmethod
    async def get_by_question(cls, question_id: str) -> List[Answer]:
        cursor = cls.collection.find({'question_id': question_id}).sort('created_at', -1)
        answers = []
        async for doc in cursor:
            answers.append(cls.model(**doc))
        return answers

    @classmethod
    async def get_by_author(cls, author_id: str, limit: int | None = None) -> List[Answer]:
        if not limit:
            cursor = cls.collection.find({'author_id': author_id}).sort('created_at', -1)
        else:
            cursor = cls.collection.find({'author_id': author_id}).sort('created_at', -1).limit(limit)

        answers = []
        async for doc in cursor:
            answers.append(cls.model(**doc))
        return answers

class TagController(BaseController):
    model = Tag
    collection = database['tags']

    @classmethod
    async def get_by_name(cls, name: str) -> dict:
        tag = await cls.collection.find_one({'name': name})
        return tag

class AdminController(BaseController):
    model = Admin
    collection = database['admins']

    @classmethod
    async def get_by_username(cls, username: str) -> dict:
        user = await cls.collection.find_one({'username': username})
        return user

class UserSettingsController(BaseController):
    model = UserSettings 
    collection = database['users_settings']