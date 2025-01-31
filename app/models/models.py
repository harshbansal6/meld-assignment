from sqlalchemy import Column, Integer, String, Text, DateTime, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base

class ReviewHistory(Base):
    __tablename__ = "review_history"
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    text = Column(String, nullable=True)
    stars = Column(Integer)
    review_id = Column(String(255))
    tone = Column(String(255), nullable=True)
    sentiment = Column(String(255), nullable=True)
    category_id = Column(BigInteger, ForeignKey("public.category.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    category = relationship("Category", back_populates="reviews")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.stars is not None and (self.stars < 1 or self.stars > 10):
            raise ValueError("Stars must be between 1 and 10")

class Category(Base):
    __tablename__ = "category"
    __table_args__ = {'schema': 'public'}
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True)
    description = Column(Text)

    reviews = relationship("ReviewHistory", back_populates="category")

class AccessLog(Base):
    __tablename__ = "access_log"
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    text = Column(String) 