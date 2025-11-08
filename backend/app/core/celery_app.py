"""Celery application configuration."""

from celery import Celery

from app.core.config import settings

# Create Celery app
celery_app = Celery(
    "fast_lead",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["app.tasks.sms_tasks", "app.tasks.email_tasks", "app.tasks.lead_tasks"],
)

# Configure Celery
celery_app.conf.update(
    # Task settings
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Europe/Moscow",
    enable_utc=True,

    # Task execution
    task_track_started=True,
    task_time_limit=300,  # 5 minutes hard limit
    task_soft_time_limit=240,  # 4 minutes soft limit

    # Result backend
    result_expires=3600,  # Results expire after 1 hour
    result_extended=True,

    # Worker settings
    worker_prefetch_multiplier=4,
    worker_max_tasks_per_child=1000,

    # Retry settings
    task_acks_late=True,  # Acknowledge task after completion
    task_reject_on_worker_lost=True,

    # Monitoring
    worker_send_task_events=True,
    task_send_sent_event=True,
)

# Task routes (optional - for task-specific queues)
celery_app.conf.task_routes = {
    "app.tasks.sms_tasks.*": {"queue": "sms"},
    "app.tasks.lead_tasks.*": {"queue": "leads"},
}

# Beat schedule for periodic tasks (optional)
celery_app.conf.beat_schedule = {
    # Example: Check SMS delivery status every 5 minutes
    # "check-sms-status": {
    #     "task": "app.tasks.sms_tasks.check_pending_sms_status",
    #     "schedule": 300.0,  # 5 minutes
    # },
}
