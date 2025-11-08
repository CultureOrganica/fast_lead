"""Celery tasks for SMS operations."""

import asyncio
import logging
from typing import Optional

from celery import Task
from sqlalchemy import select, update

from app.core.celery_app import celery_app
from app.core.database import async_session_maker
from app.models.lead import Lead
from app.services.sms_service import SMSService, SMSServiceError

logger = logging.getLogger(__name__)


class SMSTask(Task):
    """Base task for SMS operations with retry logic."""

    autoretry_for = (SMSServiceError, ConnectionError)
    retry_kwargs = {"max_retries": 3}
    retry_backoff = True
    retry_backoff_max = 600  # 10 minutes
    retry_jitter = True


@celery_app.task(base=SMSTask, name="send_sms")
def send_sms_task(
    phone: str,
    message: str,
    lead_id: Optional[int] = None,
    sender: Optional[str] = None,
) -> dict:
    """
    Send SMS message via SMSC.ru.

    Args:
        phone: Phone number in international format
        message: Message text
        lead_id: Lead ID (optional, for tracking)
        sender: Sender name (optional)

    Returns:
        Dict with message_id, success status, and metadata
    """
    logger.info(f"Sending SMS to {phone} (Lead ID: {lead_id})")

    # Create SMS service
    sms_service = SMSService()

    # Send SMS (using asyncio.run for async function)
    try:
        result = asyncio.run(
            sms_service.send_sms(
                phone=phone,
                message=message,
                sender=sender,
            )
        )

        # Update lead if lead_id is provided
        if lead_id:
            asyncio.run(_update_lead_sms_status(lead_id, result))

        logger.info(f"SMS sent successfully. Message ID: {result['message_id']}")
        return result

    except SMSServiceError as e:
        logger.error(f"Failed to send SMS: {e}")
        # Update lead status to failed
        if lead_id:
            asyncio.run(_update_lead_sms_failed(lead_id, str(e)))
        raise


@celery_app.task(base=SMSTask, name="send_verification_code")
def send_verification_code_task(phone: str, code: str, lead_id: Optional[int] = None) -> dict:
    """
    Send verification code via SMS.

    Args:
        phone: Phone number
        code: Verification code (4-6 digits)
        lead_id: Lead ID (optional)

    Returns:
        Dict with message_id and status
    """
    message = f"Ваш код подтверждения: {code}\n\nFast Lead"

    return send_sms_task(phone=phone, message=message, lead_id=lead_id)


@celery_app.task(base=SMSTask, name="send_appointment_reminder")
def send_appointment_reminder_task(
    phone: str,
    appointment_time: str,
    lead_id: Optional[int] = None,
) -> dict:
    """
    Send appointment reminder via SMS.

    Args:
        phone: Phone number
        appointment_time: Appointment time (human-readable)
        lead_id: Lead ID (optional)

    Returns:
        Dict with message_id and status
    """
    message = (
        f"Напоминание: Ваша встреча назначена на {appointment_time}\n\n"
        f"С уважением, Fast Lead"
    )

    return send_sms_task(phone=phone, message=message, lead_id=lead_id)


@celery_app.task(name="check_sms_status")
def check_sms_status_task(message_id: int, phone: str, lead_id: Optional[int] = None) -> dict:
    """
    Check SMS delivery status.

    Args:
        message_id: SMSC message ID
        phone: Phone number
        lead_id: Lead ID (optional)

    Returns:
        Dict with status information
    """
    sms_service = SMSService()

    try:
        status = asyncio.run(sms_service.get_status(message_id, phone))

        # Update lead if status indicates delivery
        if lead_id and status.get("status") in [1, 2]:  # Delivered or read
            asyncio.run(_update_lead_sms_delivered(lead_id))

        return status

    except SMSServiceError as e:
        logger.error(f"Failed to check SMS status: {e}")
        return {"error": str(e)}


# Helper functions

async def _update_lead_sms_status(lead_id: int, sms_result: dict) -> None:
    """
    Update lead with SMS sending result.

    Args:
        lead_id: Lead ID
        sms_result: Result from SMS service
    """
    async with async_session_maker() as session:
        try:
            # Update lead payload with SMS info
            stmt = (
                update(Lead)
                .where(Lead.id == lead_id)
                .values(
                    payload=Lead.payload.concat(
                        {
                            "sms_message_id": sms_result.get("message_id"),
                            "sms_sent_at": asyncio.get_event_loop().time(),
                            "sms_status": "sent",
                        }
                    )
                )
            )
            await session.execute(stmt)
            await session.commit()

        except Exception as e:
            logger.error(f"Failed to update lead SMS status: {e}")
            await session.rollback()


async def _update_lead_sms_failed(lead_id: int, error: str) -> None:
    """
    Update lead with SMS failure info.

    Args:
        lead_id: Lead ID
        error: Error message
    """
    async with async_session_maker() as session:
        try:
            stmt = (
                update(Lead)
                .where(Lead.id == lead_id)
                .values(
                    payload=Lead.payload.concat(
                        {
                            "sms_status": "failed",
                            "sms_error": error,
                        }
                    )
                )
            )
            await session.execute(stmt)
            await session.commit()

        except Exception as e:
            logger.error(f"Failed to update lead SMS failure: {e}")
            await session.rollback()


async def _update_lead_sms_delivered(lead_id: int) -> None:
    """
    Update lead with SMS delivery confirmation.

    Args:
        lead_id: Lead ID
    """
    async with async_session_maker() as session:
        try:
            stmt = (
                update(Lead)
                .where(Lead.id == lead_id)
                .values(
                    payload=Lead.payload.concat(
                        {
                            "sms_status": "delivered",
                            "sms_delivered_at": asyncio.get_event_loop().time(),
                        }
                    )
                )
            )
            await session.execute(stmt)
            await session.commit()

        except Exception as e:
            logger.error(f"Failed to update lead SMS delivery: {e}")
            await session.rollback()
