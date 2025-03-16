import sys
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from internal.utils.logger import logger
from config.config import get_config


MONGODB_URI = get_config("mongodb_uri")
DB_NAME = get_config("mongodb_database")

client = AsyncIOMotorClient(MONGODB_URI)
database = client[DB_NAME]


# Check the database connection at startup
async def _check_connection():
    await database.command("ping")

try:
    asyncio.run(_check_connection())
    logger.info("Successfully connected to the database.")
except Exception as e:
    logger.error(f"Failed to connect to the database. Details: {e}")
    sys.exit(1)

users_collection = database["users"]
