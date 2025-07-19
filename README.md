# Items REST API

A simple, production-ready REST API built with FastAPI for managing items with SQLite database.

## Features

- **FastAPI Framework**: Modern, fast web framework with automatic API documentation
- **SQLite Database**: Lightweight database with SQLAlchemy ORM
- **Interactive Documentation**: Automatically generated Swagger UI and ReDoc
- **Input Validation**: Pydantic models for request/response validation
- **Error Handling**: Comprehensive error handling with proper HTTP status codes
- **Logging**: Structured logging to file and console
- **Type Hints**: Full type annotations for better code quality

## API Endpoints

- `GET /` - Root endpoint with API information
- `GET /items` - Retrieve all items
- `POST /items` - Create a new item
- `GET /items/{item_id}` - Retrieve a specific item by ID
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation (ReDoc)

## Database Schema

### Item Table
- `id` (Integer, Primary Key) - Auto-incrementing item ID
- `name` (String, Required) - Item name (1-100 characters)
- `description` (Text, Optional) - Item description (max 1000 characters)
- `created_at` (DateTime) - Timestamp of creation

## Setup Instructions

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Installation

1. **Clone or download the project files**
   ```bash
   # Navigate to the project directory
   cd 250719_API_Project
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # Activate virtual environment
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python main.py
   ```
   
   Or use uvicorn directly:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Access the API**
   - API Base URL: http://localhost:8000
   - Interactive Documentation: http://localhost:8000/docs
   - Alternative Documentation: http://localhost:8000/redoc

## Usage Examples

### Using curl

#### 1. Get all items
```bash
curl -X GET "http://localhost:8000/items" \
     -H "accept: application/json"
```

#### 2. Create a new item
```bash
curl -X POST "http://localhost:8000/items" \
     -H "accept: application/json" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Sample Item",
       "description": "This is a sample item description"
     }'
```

#### 3. Get a specific item by ID
```bash
curl -X GET "http://localhost:8000/items/1" \
     -H "accept: application/json"
```

### Using Python requests

```python
import requests
import json

base_url = "http://localhost:8000"

# Get all items
response = requests.get(f"{base_url}/items")
print("All items:", response.json())

# Create a new item
new_item = {
    "name": "Python Item",
    "description": "Created using Python requests"
}
response = requests.post(f"{base_url}/items", json=new_item)
print("Created item:", response.json())

# Get specific item
item_id = 1
response = requests.get(f"{base_url}/items/{item_id}")
print(f"Item {item_id}:", response.json())
```

## Testing

### Manual Testing with Interactive Documentation
1. Start the application
2. Open http://localhost:8000/docs in your browser
3. Use the "Try it out" feature to test endpoints interactively

### API Response Examples

#### Successful GET /items response:
```json
[
  {
    "id": 1,
    "name": "Sample Item",
    "description": "This is a sample item",
    "created_at": "2024-01-01T12:00:00.000000"
  }
]
```

#### Successful POST /items response:
```json
{
  "id": 1,
  "name": "New Item",
  "description": "Description of the new item",
  "created_at": "2024-01-01T12:00:00.000000"
}
```

#### Error response example:
```json
{
  "detail": "Item with name 'Duplicate Item' already exists",
  "status_code": 409
}
```

## Project Structure

```
250719_API_Project/
├── main.py              # FastAPI application and endpoints
├── database.py          # Database models and connection
├── schemas.py           # Pydantic models for validation
├── config.py            # Configuration and logging setup
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── items.db            # SQLite database (created automatically)
└── app.log             # Application logs (created automatically)
```

## Configuration

The application uses the following configuration (in `config.py`):
- **Database**: SQLite database stored as `items.db`
- **Logging**: Both file (`app.log`) and console logging
- **API Documentation**: Available at `/docs` and `/redoc`

## Error Handling

The API includes comprehensive error handling:
- **400 Bad Request**: Invalid input data
- **404 Not Found**: Item not found
- **409 Conflict**: Duplicate item name
- **422 Unprocessable Entity**: Validation errors
- **500 Internal Server Error**: Server-side errors

All errors return JSON responses with descriptive messages.

## Production Considerations

- **Database**: For production, consider using PostgreSQL or MySQL
- **Environment Variables**: Use environment variables for sensitive configuration
- **Authentication**: Add authentication and authorization as needed
- **Rate Limiting**: Implement rate limiting for API endpoints
- **CORS**: Configure CORS if frontend is on different domain
- **Monitoring**: Add health checks and monitoring endpoints

## Dependencies

- **FastAPI**: Modern web framework for APIs
- **Uvicorn**: ASGI server for running FastAPI
- **SQLAlchemy**: ORM for database operations
- **Pydantic**: Data validation and serialization
- **Python-multipart**: For handling form data (if needed)

## License

This project is provided as-is for demonstration purposes.