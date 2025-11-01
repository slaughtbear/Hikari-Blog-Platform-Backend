from typing import Any
from bson import ObjectId
from src.database.connection import database
from src.schemas.users import user_schema

users_collection = database.Users

async def add_user(user_data: dict) -> dict[str, Any]:
    new_user = await users_collection.insert_one(user_data)
    return await users_collection.find_one({"_id": new_user.inserted_id})

async def get_users() -> list[dict]:
    users_list = []
    cursor = users_collection.find({})

    async for document in cursor:
        users_list.append(user_schema(document))

    return users_list

async def get_user(field: str, key: Any):
    return await users_collection.find_one({field: key})

async def patch_user(id: str, user_data: dict) -> dict[str, Any]:
    data = {k: v for k, v in user_data.items() if v is not None}
    result = await users_collection.update_one({"_id": ObjectId(id)}, {"$set": data})

    if result.matched_count == 0:
        return None
    
    return await get_user(field="_id", key=ObjectId(id))

async def del_user(id: str) -> bool:
    result = await users_collection.delete_one({"_id": ObjectId(id)})
    return result.deleted_count == 1