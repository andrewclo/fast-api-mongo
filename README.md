# FastAPI MongoDB Project

A FastAPI application with MongoDB integration using Motor (async MongoDB driver).

## Features

- FastAPI framework for building APIs
- MongoDB integration with Motor
- Pydantic models for data validation
- CRUD operations for User model
- CORS middleware configured
- Environment-based configuration

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
# or if using poetry:
poetry install
```

2. Ensure your MongoDB Atlas cluster is running and accessible.

3. Create a `.env` file based on the configuration in `config.py`:
```
MONGODB_URL=mongodb+srv://your-username:your-password@cluster0.wytszzt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
DATABASE_NAME=fastapi_mongo
APP_NAME=FastAPI MongoDB App
DEBUG=true
HOST=0.0.0.0
PORT=8000
```

**Note:** Replace `your-username` and `your-password` with your actual MongoDB Atlas credentials.

4. Run the application:
```bash
python main.py
# or with uvicorn directly:
uvicorn main:app --reload
```

## API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /bikes` - Create a new bike
- `GET /bikes` - Get all bikes (with pagination)
- `GET /bikes/{bike_id}` - Get a specific bike
- `PUT /bikes/{bike_id}` - Update a bike
- `DELETE /bikes/{bike_id}` - Delete a bike

## Project Structure

```
fast-api-mongo/
├── main.py              # Main FastAPI application
├── config.py            # Configuration settings
├── database.py          # MongoDB connection handling
├── models.py            # Pydantic models
├── pyproject.toml       # Project dependencies (Poetry)
└── README.md           # This file
```

## Development

The application uses:
- **FastAPI**: Modern, fast web framework for building APIs
- **Motor**: Async MongoDB driver for Python
- **Pydantic**: Data validation and serialization
- **Uvicorn**: ASGI server for running FastAPI

## Testing the API

You can test the API using tools like:
- curl
- Postman
- HTTPie
- FastAPI's built-in documentation at `http://localhost:8000/docs`

Example curl commands:

```bash
# Create a bike
curl -X POST "http://localhost:8000/bikes" \
     -H "Content-Type: application/json" \
     -d '{"name": "Mountain Bike", "model": "Trek X-Caliber", "year": 2023}'

# Get all bikes
curl -X GET "http://localhost:8000/bikes"

# Get a specific bike
curl -X GET "http://localhost:8000/bikes/{bike_id}"
```
