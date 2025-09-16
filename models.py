from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId

# Simple Bike model for MongoDB
class Bike(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")  # MongoDB ObjectId as string
    brand: str = Field(..., min_length=1, max_length=100)
    model: str = Field(..., min_length=1, max_length=100)
    trim: Optional[str] = Field(None, min_length=1, max_length=100)
    year: Optional[int] = Field(None, ge=1900, le=2030)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "json_encoders": {ObjectId: str},
        "json_schema_extra": {
            "example": {
                "brand": "Specialized",
                "model": "Stumpjumper 15",
                "trim": "Shimano XTR Di2, FOX Factory",
                "year": 2025
            }
        }
    }

# Bike update model (all fields optional)
class BikeUpdate(BaseModel):
    brand: Optional[str] = Field(None, min_length=1, max_length=100)
    model: Optional[str] = Field(None, min_length=1, max_length=100)
    trim: Optional[str] = Field(None, min_length=1, max_length=100)
    year: Optional[int] = Field(None, ge=1900, le=2030)

    model_config = {
        "json_schema_extra": {
            "example": {
                "brand": "Specialized",
                "model": "Stumpjumper 15",
                "trim": "Shimano XTR Di2, FOX Factory",
                "year": 2025
            }
        }
    }
