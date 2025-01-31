from celery import Celery

from app.config.config import redis_server
from app.models.models import AccessLog
from core.database import SessionLocal

celery = Celery('tasks', broker=redis_server, backend=redis_server)

@celery.task
def log_access(log_text: str):
    db = SessionLocal()
    try:
        access_log = AccessLog(text=log_text)
        db.add(access_log)
        db.commit()
    finally:
        db.close() 