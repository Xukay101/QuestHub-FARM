from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

from app.config import settings
from app.models import User

# Conections
client = AsyncIOMotorClient(settings.MONGODB_URI)
database = client[settings.MONGODB_NAME]

# Controllers
class UserController():
    collection = database['users']

    @classmethod
    async def get_by_id(cls, id: str):
        user = await cls.collection.find_one({'_id': ObjectId(id)})
        return user

    @classmethod
    async def get_by_username(cls, username: str):
        user = await cls.collection.find_one({'username': username})
        return user

    @classmethod
    async def get_users(cls):
        users = []
        cursor = cls.collection.find({})
        async for doc in cursor:
            users.append(User(**doc))
        return users

    @classmethod
    async def create(cls, user):
        new_user = await cls.collection.insert_one(user)
        created_user = await cls.collection.find_one({'_id': new_user.inserted_id})
        created_user['_id'] = str(created_user['_id'])
        return created_user

    @classmethod
    async def update(cls, id: str, user):
        await cls.collection.update_one({'_id': id}, {'$set': user})
        document = await cls.collection.find_one({'_id': id})
        return document 

    @classmethod
    async def delete(cls, id: str):
        await cls.collection.delete_one({'_id': id})
        return True 


