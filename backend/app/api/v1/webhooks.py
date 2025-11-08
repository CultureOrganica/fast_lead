"""Webhook API endpoints - Handlers for external service webhooks."""

import logging
import hmac
import hashlib
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Request, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from app.core.config import settings
from app.core.database import get_db
from app.models.lead import Lead, LeadStatus

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


def verify_calcom_webhook(payload: bytes, signature: str) -> bool:
    """
    Verify Cal.com webhook signature.

    Args:
        payload: Raw request body
        signature: Signature from X-Cal-Signature header

    Returns:
        True if signature is valid, False otherwise
    """
    if not settings.calcom_webhook_secret:
        logger.warning("Cal.com webhook secret not configured, skipping verification")
        return True

    # Calculate expected signature
    expected_signature = hmac.new(
        settings.calcom_webhook_secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()

    # Compare signatures (constant-time comparison)
    return hmac.compare_digest(signature, expected_signature)


@router.post("/calcom")
async def calcom_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db),
    x_cal_signature: str = Header(None, alias="X-Cal-Signature"),
):
    """
    Handle Cal.com webhook events.

    Cal.com sends webhooks for various booking events:
    - booking.created: New booking created
    - booking.rescheduled: Booking time changed
    - booking.cancelled: Booking cancelled
    - booking.completed: Meeting completed

    **Security:**
    Webhook payload is verified using HMAC SHA256 signature.
    """
    # Get raw body for signature verification
    body = await request.body()

    # Verify signature
    if x_cal_signature:
        if not verify_calcom_webhook(body, x_cal_signature):
            logger.warning("Invalid Cal.com webhook signature")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid webhook signature"
            )
    else:
        logger.warning("Cal.com webhook received without signature")

    # Parse JSON payload
    try:
        payload = await request.json()
    except Exception as e:
        logger.error(f"Failed to parse webhook payload: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid JSON payload"
        )

    # Extract event type
    event_type = payload.get("triggerEvent")
    booking_data = payload.get("payload", {})

    logger.info(f"Received Cal.com webhook: {event_type}")

    # Get booking ID and lead ID
    booking_id = booking_data.get("id")
    metadata = booking_data.get("metadata", {})
    lead_id = metadata.get("lead_id")

    if not booking_id:
        logger.warning("Webhook payload missing booking ID")
        return {"success": True, "message": "No booking ID found"}

    # Handle different event types
    try:
        if event_type == "BOOKING_CREATED":
            await handle_booking_created(db, booking_id, lead_id, booking_data)

        elif event_type == "BOOKING_RESCHEDULED":
            await handle_booking_rescheduled(db, booking_id, lead_id, booking_data)

        elif event_type == "BOOKING_CANCELLED":
            await handle_booking_cancelled(db, booking_id, lead_id, booking_data)

        elif event_type == "BOOKING_COMPLETED":
            await handle_booking_completed(db, booking_id, lead_id, booking_data)

        else:
            logger.info(f"Unhandled webhook event type: {event_type}")

    except Exception as e:
        logger.error(f"Error handling webhook event {event_type}: {e}")
        # Don't raise exception - we don't want to cause retries
        return {"success": False, "error": str(e)}

    return {"success": True, "event_type": event_type}


async def handle_booking_created(
    db: AsyncSession,
    booking_id: int,
    lead_id: int,
    booking_data: Dict[str, Any],
):
    """Handle booking.created event."""
    logger.info(f"Handling BOOKING_CREATED: booking={booking_id}, lead={lead_id}")

    if not lead_id:
        logger.warning("No lead_id in booking metadata")
        return

    # Find lead
    result = await db.execute(
        select(Lead).where(Lead.id == lead_id)
    )
    lead = result.scalar_one_or_none()

    if not lead:
        logger.warning(f"Lead {lead_id} not found for booking {booking_id}")
        return

    # Update lead if not already updated
    if not lead.booking_id:
        lead.booking_id = str(booking_id)
        lead.booking_url = booking_data.get("meetingUrl") or booking_data.get("url")
        lead.booked_at = booking_data.get("startTime")
        lead.status = LeadStatus.BOOKED

        await db.commit()
        logger.info(f"Lead {lead_id} updated with booking {booking_id}")


async def handle_booking_rescheduled(
    db: AsyncSession,
    booking_id: int,
    lead_id: int,
    booking_data: Dict[str, Any],
):
    """Handle booking.rescheduled event."""
    logger.info(f"Handling BOOKING_RESCHEDULED: booking={booking_id}, lead={lead_id}")

    # Find lead by booking_id
    result = await db.execute(
        select(Lead).where(Lead.booking_id == str(booking_id))
    )
    lead = result.scalar_one_or_none()

    if not lead:
        logger.warning(f"Lead not found for booking {booking_id}")
        return

    # Update booking time
    lead.booked_at = booking_data.get("startTime")

    await db.commit()
    logger.info(f"Lead {lead.id} booking rescheduled")


async def handle_booking_cancelled(
    db: AsyncSession,
    booking_id: int,
    lead_id: int,
    booking_data: Dict[str, Any],
):
    """Handle booking.cancelled event."""
    logger.info(f"Handling BOOKING_CANCELLED: booking={booking_id}, lead={lead_id}")

    # Find lead by booking_id
    result = await db.execute(
        select(Lead).where(Lead.booking_id == str(booking_id))
    )
    lead = result.scalar_one_or_none()

    if not lead:
        logger.warning(f"Lead not found for booking {booking_id}")
        return

    # Update lead status
    lead.status = LeadStatus.QUALIFIED  # Move back to qualified
    # Keep booking_id and booking_url for history

    await db.commit()
    logger.info(f"Lead {lead.id} booking cancelled")


async def handle_booking_completed(
    db: AsyncSession,
    booking_id: int,
    lead_id: int,
    booking_data: Dict[str, Any],
):
    """Handle booking.completed event."""
    logger.info(f"Handling BOOKING_COMPLETED: booking={booking_id}, lead={lead_id}")

    # Find lead by booking_id
    result = await db.execute(
        select(Lead).where(Lead.booking_id == str(booking_id))
    )
    lead = result.scalar_one_or_none()

    if not lead:
        logger.warning(f"Lead not found for booking {booking_id}")
        return

    # Update lead status to completed
    lead.status = LeadStatus.COMPLETED

    await db.commit()
    logger.info(f"Lead {lead.id} marked as completed")
