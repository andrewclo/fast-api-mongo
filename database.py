from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.server_api import ServerApi
from config import settings

class Database:
    client: AsyncIOMotorClient = None
    database: AsyncIOMotorDatabase = None

db = Database()

async def connect_to_mongo():
    """Connect to MongoDB Atlas"""
    try:
        # Create a new client and connect to the server with server API
        db.client = AsyncIOMotorClient(
            settings.mongodb_url,
            server_api=ServerApi('1')
        )

        # Send a ping to confirm a successful connection
        await db.client.admin.command('ping')
        print("✅ Pinged your deployment. You successfully connected to MongoDB Atlas!")

        # Set up the database
        db.database = db.client[settings.database_name]
        print(f"📊 Connected to database: {settings.database_name}")

    except Exception as e:
        print(f"❌ Failed to connect to MongoDB Atlas: {e}")
        raise

async def close_mongo_connection():
    """Close MongoDB connection"""
    if db.client:
        db.client.close()
        print("🔌 Disconnected from MongoDB Atlas")

async def get_database() -> AsyncIOMotorDatabase:
    """Get database instance"""
    return db.database
