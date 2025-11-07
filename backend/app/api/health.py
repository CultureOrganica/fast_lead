"""Health check endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import redis.asyncio as aioredis

from app.core.database import get_db
from app.core.config import settings

router = APIRouter()


@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    """
    Health check endpoint.

    Checks database and Redis connectivity.
    Returns status of all dependencies.
    """
    status = {
        "status": "healthy",
        "version": settings.app_version,
        "environment": settings.environment,
        "database": "unknown",
        "redis": "unknown",
    }

    # Check database
    try:
        result = await db.execute(text("SELECT 1"))
        result.fetchone()
        status["database"] = "connected"
    except Exception as e:
        status["database"] = f"error: {str(e)}"
        status["status"] = "unhealthy"

    # Check Redis
    try:
        redis_client = aioredis.from_url(
            settings.redis_url_str,
            encoding="utf-8",
            decode_responses=True
        )
        await redis_client.ping()
        await redis_client.close()
        status["redis"] = "connected"
    except Exception as e:
        status["redis"] = f"error: {str(e)}"
        status["status"] = "degraded"  # Redis is not critical for basic operation

    return status


@router.get("/health/live")
async def liveness():
    """
    Liveness probe for Kubernetes.

    Simple check that the service is running.
    """
    return {"status": "alive"}


@router.get("/health/ready")
async def readiness(db: AsyncSession = Depends(get_db)):
    """
    Readiness probe for Kubernetes.

    Checks if the service is ready to handle requests.
    """
    try:
        # Check database
        await db.execute(text("SELECT 1"))
        return {"status": "ready"}
    except Exception:
        return {"status": "not_ready"}
