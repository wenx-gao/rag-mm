from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "rag_worker",
    # We use the variable here:
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

# celery_app.conf.task_routes = {"app.worker.process_document": "main-queue"}
