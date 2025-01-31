from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CategoryTrend(BaseModel):
    id: int
    name: str
    description: str
    average_stars: float
    total_reviews: int

class ReviewResponse(BaseModel):
    id: int
    text: Optional[str]
    stars: int
    review_id: str
    created_at: datetime
    tone: Optional[str]
    sentiment: Optional[str]
    category_id: int

    class Config:
        from_attributes = True 