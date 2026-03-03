# app/core/celery_app.py
from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "rag_worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=['app.worker'] # Explicitly include the worker module
)

celery_app.conf.update(
    task_ignore_result=False,
    result_persistent=True,
)
