import os
from celery import Celery
from dotenv import load_dotenv


load_dotenv()

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "amqp://guest:guest@rabbitmq:5672//")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")

celery = Celery(
    "worker",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=["app.tasks"]
)

celery.conf.update(
    task_routes={"generate_and_process_numbers": {"queue": "default"}},
    task_track_started=True,
    task_send_sent_event=True,
    result_backend="redis://redis:6379/0",
    result_expires=3600,
    task_serializer='json',
    result_serializer='json',
    accept_content=['json']
)
