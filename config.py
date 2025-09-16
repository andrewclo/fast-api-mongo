from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # MongoDB settings
    mongodb_password: str = "your_password_here"  # Will be overridden by environment variable
    database_name: str = "fastapi_mongo"

    # Application settings
    app_name: str = "FastAPI MongoDB App"
    debug: bool = True

    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000

    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignore extra environment variables

    @property
    def mongodb_url(self) -> str:
        """Construct MongoDB Atlas URL with password"""
        return f"mongodb+srv://aclough:{self.mongodb_password}@cluster0.wytszzt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

settings = Settings()
