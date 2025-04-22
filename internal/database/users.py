from internal.database.database import users_collection
from internal.models.user import User
from pymongo.errors import DuplicateKeyError
from typing import Optional
from bson import ObjectId


async def create_user(user: User) -> Optional[User]:
    user_data = user.model_dump(by_alias=True)
    try:
        result = await users_collection.insert_one(user_data)
        if result.inserted_id:
            return user
    except DuplicateKeyError:
        return None
    return None


async def get_user_by_id(user_id: str) -> Optional[User]:
    user_data = await users_collection.find_one({"_id": user_id})
    return User(**user_data) if user_data else None


async def get_user_by_email(email: str) -> Optional[User]:
    user_data = await users_collection.find_one({"email": email})
    return User(**user_data) if user_data else None


async def get_penalty_users_count() -> int:
    return await users_collection.count_documents({"penalties.0": {"$exists": True}})


async def update_user(user: User) -> bool:
    user_data = user.model_dump(by_alias=True)
    result = await users_collection.update_one(
        {"_id": user.id}, {"$set": user_data}
    )
    return result.modified_count > 0


async def delete_user(user_id: str) -> bool:
    result = await users_collection.delete_one({"_id": ObjectId(user_id)})
    return result.deleted_count > 0
