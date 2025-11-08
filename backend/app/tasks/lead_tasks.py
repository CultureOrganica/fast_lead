"""Celery tasks for lead orchestration."""

import asyncio
import logging
from typing import Optional

from celery import Task
from sqlalchemy import select, update

from app.core.celery_app import celery_app
from app.core.database import async_session_maker
from app.models.lead import Lead, LeadStatus, LeadChannel
from app.tasks.sms_tasks import send_sms_task

logger = logging.getLogger(__name__)


class LeadTask(Task):
    """Base task for lead operations."""

    autoretry_for = (ConnectionError,)
    retry_kwargs = {"max_retries": 3}
    retry_backoff = True


@celery_app.task(base=LeadTask, name="process_new_lead")
def process_new_lead_task(lead_id: int) -> dict:
    """
    Process a new lead based on channel.

    This is the main orchestrator task that determines what action
    to take based on the lead's channel.

    Args:
        lead_id: Lead ID

    Returns:
        Dict with processing result
    """
    logger.info(f"Processing new lead: {lead_id}")

    # Get lead from database
    lead = asyncio.run(_get_lead(lead_id))

    if not lead:
        logger.error(f"Lead {lead_id} not found")
        return {"success": False, "error": "Lead not found"}

    # Update status to processing
    asyncio.run(_update_lead_status(lead_id, LeadStatus.PROCESSING))

    # Process based on channel
    try:
        if lead.channel == LeadChannel.SMS:
            return _process_sms_lead(lead)
        elif lead.channel == LeadChannel.EMAIL:
            return _process_email_lead(lead)
        elif lead.channel == LeadChannel.VK:
            return _process_vk_lead(lead)
        elif lead.channel == LeadChannel.TELEGRAM:
            return _process_telegram_lead(lead)
        elif lead.channel == LeadChannel.WHATSAPP:
            return _process_whatsapp_lead(lead)
        elif lead.channel == LeadChannel.WEB:
            return _process_web_lead(lead)
        else:
            logger.warning(f"Unknown channel: {lead.channel}")
            asyncio.run(_update_lead_status(lead_id, LeadStatus.NEW))
            return {"success": False, "error": "Unknown channel"}

    except Exception as e:
        logger.error(f"Error processing lead {lead_id}: {e}")
        asyncio.run(_update_lead_status(lead_id, LeadStatus.FAILED))
        return {"success": False, "error": str(e)}


def _process_sms_lead(lead: Lead) -> dict:
    """
    Process SMS channel lead.

    Sends a welcome SMS with next steps.
    """
    logger.info(f"Processing SMS lead: {lead.id}")

    # Generate message
    message = (
        f"Здравствуйте, {lead.name}!\n\n"
        f"Спасибо за интерес к нашим услугам. "
        f"Наш специалист свяжется с вами в ближайшее время.\n\n"
        f"С уважением, Fast Lead"
    )

    # Send SMS asynchronously
    send_sms_task.delay(
        phone=lead.phone,
        message=message,
        lead_id=lead.id,
    )

    # Update lead status
    asyncio.run(_update_lead_status(lead.id, LeadStatus.CONTACTED))

    return {
        "success": True,
        "action": "sms_sent",
        "message": "SMS queued for sending",
    }


def _process_email_lead(lead: Lead) -> dict:
    """
    Process Email channel lead.

    Sends a welcome email with next steps.
    """
    logger.info(f"Processing Email lead: {lead.id}")

    # Import here to avoid circular dependency
    from app.tasks.email_tasks import send_welcome_email_task

    # Send welcome email asynchronously
    send_welcome_email_task.delay(
        to_email=lead.email,
        name=lead.name,
        lead_id=lead.id,
    )

    # Update lead status
    asyncio.run(_update_lead_status(lead.id, LeadStatus.CONTACTED))

    return {
        "success": True,
        "action": "email_sent",
        "message": "Welcome email queued for sending",
    }


def _process_vk_lead(lead: Lead) -> dict:
    """
    Process VK channel lead.

    NOTE: Requires VK bot configuration and user_id.
    For now, just marks as contacted.
    Full implementation requires webhook integration.
    """
    logger.info(f"Processing VK lead: {lead.id}")

    # Update lead status
    asyncio.run(_update_lead_status(lead.id, LeadStatus.CONTACTED))

    return {
        "success": True,
        "action": "vk_ready",
        "message": "VK lead ready for manual processing",
    }


def _process_telegram_lead(lead: Lead) -> dict:
    """
    Process Telegram channel lead.

    NOTE: Requires Telegram bot configuration and chat_id.
    For now, just marks as contacted.
    Full implementation requires webhook integration.
    """
    logger.info(f"Processing Telegram lead: {lead.id}")

    # Update lead status
    asyncio.run(_update_lead_status(lead.id, LeadStatus.CONTACTED))

    return {
        "success": True,
        "action": "telegram_ready",
        "message": "Telegram lead ready for manual processing",
    }


def _process_whatsapp_lead(lead: Lead) -> dict:
    """
    Process WhatsApp channel lead.

    TODO: Implement WhatsApp Business API in Week 5
    """
    logger.info(f"Processing WhatsApp lead: {lead.id}")

    asyncio.run(_update_lead_status(lead.id, LeadStatus.CONTACTED))

    return {
        "success": True,
        "action": "whatsapp_pending",
        "message": "WhatsApp processing not yet implemented",
    }


def _process_web_lead(lead: Lead) -> dict:
    """
    Process Web channel lead.

    For web channel, we don't send automatic messages.
    The lead should be handled by the dashboard operator.
    """
    logger.info(f"Processing Web lead: {lead.id}")

    asyncio.run(_update_lead_status(lead.id, LeadStatus.NEW))

    return {
        "success": True,
        "action": "manual_review",
        "message": "Lead ready for manual review in dashboard",
    }


# Helper functions

async def _get_lead(lead_id: int) -> Optional[Lead]:
    """Get lead by ID."""
    async with async_session_maker() as session:
        result = await session.execute(
            select(Lead).where(Lead.id == lead_id)
        )
        return result.scalar_one_or_none()


async def _update_lead_status(lead_id: int, status: LeadStatus) -> None:
    """Update lead status."""
    async with async_session_maker() as session:
        try:
            stmt = update(Lead).where(Lead.id == lead_id).values(status=status)
            await session.execute(stmt)
            await session.commit()
            logger.info(f"Lead {lead_id} status updated to {status.value}")
        except Exception as e:
            logger.error(f"Failed to update lead status: {e}")
            await session.rollback()
