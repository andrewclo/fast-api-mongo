#!/usr/bin/env python3
"""
Simple runner script for the FastAPI MongoDB application.
"""
import uvicorn
from config import settings

if __name__ == "__main__":
    print("🚀 Starting FastAPI MongoDB application...")
    print(f"📡 Server will be available at: http://{settings.host}:{settings.port}")
    print(f"📚 API documentation at: http://{settings.host}:{settings.port}/docs")
    print(f"🔄 Debug mode: {settings.debug}")

    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    )
