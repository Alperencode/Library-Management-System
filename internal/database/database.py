from motor.motor_asyncio import AsyncIOMotorClient
from config.config import get_config

MONGODB_URI = get_config("mongodb_uri")
DB_NAME = get_config("mongodb_database")

client = AsyncIOMotorClient(MONGODB_URI)
database = client[DB_NAME]

# Collections
users_collection = database["users"]
