from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional
from datetime import datetime
from openai import OpenAI

from app.config.config import openai_model
from core.database import get_db
from app.models.models import ReviewHistory, Category
from app.tasks import log_access
from app.serializer.schemas import ReviewResponse, CategoryTrend

router = APIRouter(
    prefix="/reviews",
    tags=["reviews"]
)

client = OpenAI()

@router.get("/trends", response_model=List[CategoryTrend])
async def get_trends(db: Session = Depends(get_db)):
    latest_reviews = db.query(
        ReviewHistory.category_id,
        func.max(ReviewHistory.created_at).label('max_created_at')
    ).group_by(ReviewHistory.review_id, ReviewHistory.category_id).subquery()

    trends = db.query(
        Category.id,
        Category.name,
        Category.description,
        func.avg(ReviewHistory.stars).label('average_stars'),
        func.count(ReviewHistory.id).label('total_reviews')
    ).join(
        latest_reviews,
        Category.id == latest_reviews.c.category_id
    ).join(
        ReviewHistory,
        (ReviewHistory.category_id == latest_reviews.c.category_id) &
        (ReviewHistory.created_at == latest_reviews.c.max_created_at)
    ).group_by(
        Category.id
    ).order_by(
        desc('average_stars')
    ).limit(5).all()

    log_access.delay("GET /reviews/trends")

    return trends

@router.get("/", response_model=List[ReviewResponse])
async def get_reviews(
    category_id: int,
    cursor: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    query = db.query(ReviewHistory).filter(
        ReviewHistory.category_id == category_id
    ).order_by(desc(ReviewHistory.created_at))

    if cursor:
        query = query.filter(ReviewHistory.created_at < cursor)

    reviews = query.limit(15).all()

    for review in reviews:
        if review.tone is None or review.sentiment is None:
            analysis = analyze_review(review.text, review.stars)
            review.tone = analysis['tone']
            review.sentiment = analysis['sentiment']
            db.commit()

    log_access.delay(f"GET /reviews/?category_id={category_id}")

    return reviews

def analyze_review(text: str, stars: int) -> dict:
    prompt = f"""
    Analyze the following review (text and rating) and provide its tone and sentiment:
    Text: {text}
    Rating: {stars}/10
    
    Return the analysis in the following format:
    tone: (professional/casual/angry/etc)
    sentiment: (positive/negative/neutral)
    """

    response = client.chat.completions.create(
        model=openai_model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    print(response.choices[0].message.content.strip())

    return {
        "tone": "professional",
        "sentiment": "positive" if stars > 5 else "negative"
    } 