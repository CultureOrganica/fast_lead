#!/bin/bash

# Fast Lead - Celery Worker Startup Script

set -e

echo "Starting Celery worker..."

# Activate virtual environment if exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run Celery worker
celery -A app.core.celery_app:celery_app worker \
    --loglevel=info \
    --concurrency=4 \
    --queues=leads,sms \
    --hostname=worker@%h

# Options explained:
# -A app.core.celery_app:celery_app - Celery app location
# --loglevel=info - Logging level
# --concurrency=4 - Number of worker processes
# --queues=leads,sms - Queues to consume from
# --hostname=worker@%h - Worker hostname
