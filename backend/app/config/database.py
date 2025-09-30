from motor.motor_asyncio import AsyncIOMotorClient
from app.config.settings import settings
import structlog

logger = structlog.get_logger()


class Database:
    client: AsyncIOMotorClient = None
    database = None


db = Database()


async def connect_to_mongo():
    try:
        db.client = AsyncIOMotorClient(settings.mongodb_url)
        db.database = db.client[settings.database_name]
        logger.info("Connected to MongoDB Atlas")
    except Exception as e:
        logger.error(f"Could not connect to MongoDB: {e}")
        raise


async def close_mongo_connection():
    if db.client:
        db.client.close()
        logger.info("MongoDB connection closed")


def get_database():
    return db.database
