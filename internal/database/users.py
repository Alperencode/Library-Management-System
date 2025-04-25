from internal.database.database import users_collection
from internal.models.user import User
from pymongo.errors import DuplicateKeyError
from typing import Optional, List, Dict, Any
from bson import ObjectId
from pymongo import ASCENDING
from internal.models.request import RequestStatus
from datetime import datetime


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


async def get_all_users() -> List[User]:
    cursor = users_collection.find()
    return [User(**doc) async for doc in cursor]


async def ban_user(user_id: str) -> bool:
    result = await users_collection.update_one(
        {"_id": user_id},
        {"$set": {"banned": True}}
    )
    return result.modified_count > 0


async def unban_user(user_id: str) -> bool:
    result = await users_collection.update_one(
        {"_id": user_id},
        {"$set": {"banned": False}}
    )
    return result.modified_count > 0


async def iter_all_requests(skip: int, limit: int) -> List[Dict[str, Any]]:
    pipeline = [
        {"$unwind": "$requested_books"},
        {"$project": {
            "_id": 0,
            "user_id": "$_id",
            "username": 1,
            "email": 1,
            "request": "$requested_books",
        }},
        {"$sort": {"request.requested_at": ASCENDING}},
        {"$skip": skip},
        {"$limit": limit},
    ]
    return await users_collection.aggregate(pipeline).to_list(length=limit)


async def update_request_status_for_all(request_id: str, new_status: RequestStatus) -> bool:
    result = await users_collection.update_many(
        {"requested_books.id": request_id},
        {
            "$set": {
                "requested_books.$[elem].status": new_status,
                "requested_books.$[elem].status_updated_at": datetime.now(),
            }
        },
        array_filters=[{"elem.id": request_id}]
    )
    return result.modified_count > 0


async def delete_request_from_all_users(request_id: str) -> bool:
    result = await users_collection.update_many(
        {"requested_books": {"$type": "array"}},
        {"$pull": {"requested_books": {"id": request_id}}}
    )
    return result.modified_count > 0
