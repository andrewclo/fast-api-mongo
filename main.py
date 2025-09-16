from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
from datetime import datetime

from database import connect_to_mongo, close_mongo_connection, get_database
from models import Bike, BikeUpdate
from config import settings

# MongoDB connection
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://aclough:MONGODB_PASSWORD@cluster0.wytszzt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongo()
    yield
    # Shutdown
    await close_mongo_connection()

app = FastAPI(
    title=settings.app_name,
    description="FastAPI application with MongoDB integration",
    version="1.0.0",
    debug=settings.debug,
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper function to get database
async def get_db() -> AsyncIOMotorDatabase:
    return await get_database()

# Routes
@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI with MongoDB"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Bike CRUD operations
@app.post("/bikes", response_model=Bike, status_code=status.HTTP_201_CREATED)
async def create_bike(bike: Bike):
    db = await get_db()
    bike_dict = bike.dict(by_alias=True, exclude={'id'})  # Exclude id field
    bike_dict['created_at'] = datetime.utcnow()
    bike_dict['updated_at'] = datetime.utcnow()

    result = await db.bikes.insert_one(bike_dict)
    created_bike = await db.bikes.find_one({"_id": result.inserted_id})

    if created_bike:
        # Convert MongoDB ObjectId to string
        created_bike['_id'] = str(created_bike['_id'])
        return Bike(**created_bike)
    raise HTTPException(status_code=500, detail="Bike creation failed")

@app.get("/bikes", response_model=List[Bike])
async def get_bikes(skip: int = 0, limit: int = 10):
    db = await get_db()
    bikes = await db.bikes.find().skip(skip).limit(limit).to_list(length=None)

    # Convert ObjectId to string for each bike
    for bike in bikes:
        bike['_id'] = str(bike['_id'])

    return [Bike(**bike) for bike in bikes]

@app.get("/bikes/{bike_id}", response_model=Bike)
async def get_bike(bike_id: str):
    db = await get_db()
    from bson import ObjectId
    try:
        bike = await db.bikes.find_one({"_id": ObjectId(bike_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid bike ID format")

    if bike:
        # Convert ObjectId to string
        bike['_id'] = str(bike['_id'])
        return Bike(**bike)
    raise HTTPException(status_code=404, detail="Bike not found")

@app.put("/bikes/{bike_id}", response_model=Bike)
async def update_bike(bike_id: str, bike_update: BikeUpdate):
    db = await get_db()
    from bson import ObjectId
    try:
        update_data = bike_update.dict(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")

        update_data["updated_at"] = datetime.utcnow()
        result = await db.bikes.update_one(
            {"_id": ObjectId(bike_id)},
            {"$set": update_data}
        )
    except:
        raise HTTPException(status_code=400, detail="Invalid bike ID format")

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Bike not found")

    updated_bike = await db.bikes.find_one({"_id": ObjectId(bike_id)})
    # Convert ObjectId to string
    updated_bike['_id'] = str(updated_bike['_id'])
    return Bike(**updated_bike)

@app.delete("/bikes/{bike_id}")
async def delete_bike(bike_id: str):
    db = await get_db()
    from bson import ObjectId
    try:
        result = await db.bikes.delete_one({"_id": ObjectId(bike_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid bike ID format")

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Bike not found")

    return {"message": "Bike deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
