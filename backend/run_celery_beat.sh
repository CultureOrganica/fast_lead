#!/bin/bash

# Fast Lead - Celery Beat Startup Script (Periodic Tasks Scheduler)

set -e

echo "Starting Celery beat..."

# Activate virtual environment if exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run Celery beat
celery -A app.core.celery_app:celery_app beat \
    --loglevel=info \
    --schedule=/tmp/celerybeat-schedule

# Options explained:
# -A app.core.celery_app:celery_app - Celery app location
# --loglevel=info - Logging level
# --schedule=/tmp/celerybeat-schedule - Schedule database location
