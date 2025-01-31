# Review API Service

A FastAPI application that manages product reviews with version history, category management, and automated sentiment analysis.

## Features

- Review history tracking
- Category-based review organization
- Automated sentiment and tone analysis using OpenAI
- Asynchronous access logging with Celery and Redis
- Cursor-based pagination
- Top categories analytics

## Prerequisites

- Python 3.10+
- PostgreSQL
- Redis Server
- OpenAI API Key

## Installation

1. Clone the repository

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
uvicorn main:app --reload
```
5. Run the celery worker:
```bash
celery -A app.tasks.celery_worker worker --loglevel=info
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the application is running, you can access:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Available Endpoints

1. GET `/reviews/trends`
   - Returns top 5 categories based on average review stars
   - Includes total review count and average stars per category

2. GET `/reviews/?category_id={id}`
   - Returns paginated reviews for a specific category
   - Automatically analyzes sentiment and tone for reviews
   - Supports cursor-based pagination
   - Page size: 15 items

