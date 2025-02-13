import uvicorn
from fastapi import FastAPI
from app.routes.reviews import router as reviews_router

app = FastAPI(
    title="Review API",
    version="1.0.0"
)

app.include_router(reviews_router)

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000)