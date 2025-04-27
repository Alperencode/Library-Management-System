from internal.database.database import admins_collection
from internal.models.admin import Admin
from pymongo.errors import DuplicateKeyError
from typing import Optional
from bson import ObjectId


async def create_admin(admin: Admin) -> Optional[Admin]:
    admin_data = admin.model_dump(by_alias=True)
    try:
        result = await admins_collection.insert_one(admin_data)
        if result.inserted_id:
            return admin
    except DuplicateKeyError:
        return None
    return None


async def get_admin_by_id(admin_id: str) -> Optional[Admin]:
    admin_data = await admins_collection.find_one({"_id": admin_id})
    return Admin(**admin_data) if admin_data else None


async def get_admin_by_email(email: str) -> Optional[Admin]:
    admin_data = await admins_collection.find_one({"email": email})
    return Admin(**admin_data) if admin_data else None


async def get_admin_by_username(username: str) -> Optional[Admin]:
    admin_data = await admins_collection.find_one({"username": username})
    return Admin(**admin_data) if admin_data else None


async def update_admin(admin: Admin) -> bool:
    admin_data = admin.model_dump(by_alias=True)
    result = await admins_collection.update_one(
        {"_id": admin.id}, {"$set": admin_data}
    )
    return result.modified_count > 0


async def delete_admin(admin_id: str) -> bool:
    result = await admins_collection.delete_one({"_id": ObjectId(admin_id)})
    return result.deleted_count > 0
