from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

from app.config import settings
from app.models import User

# Conections
client = AsyncIOMotorClient(settings.DATABASE_URI)
database = client[settings.DATABASE_NAME]

# Collections
users_collection = database['users']

# Operations
async def get_user_id(id: str):
    user = await users_collection.find_one({'_id': ObjectId(id)})
    return user

async def get_user_username(username: str):
    user = await users_collection.find_one({'username': username})
    return user

async def get_users():
    users = []
    cursor = users_collection.find({})
    async for doc in cursor:
        users.append(User(**doc))
    return users

async def create_user(user):
    new_user = await users_collection.insert_one(user)
    created_user = await users_collection.find_one({'_id': new_user.inserted_id})
    created_user['_id'] = str(created_user['_id'])
    return created_user

async def update_user(id: str, user):
    await users_collection.update_one({'_id': id}, {'$set': user})
    document = await users_collection.find_one({'_id': id})
    return document 

async def delete_user(id: str):
    await users_collection.delete_one({'_id': id})
    return True 


