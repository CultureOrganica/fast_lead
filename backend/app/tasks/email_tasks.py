"""Celery tasks for Email operations."""

import logging
from typing import Optional

from celery import Task

from app.core.celery_app import celery_app
from app.services.email_service import EmailService, EmailServiceError

logger = logging.getLogger(__name__)


class EmailTask(Task):
    """Base task for Email operations with retry logic."""

    autoretry_for = (EmailServiceError, ConnectionError)
    retry_kwargs = {"max_retries": 3}
    retry_backoff = True
    retry_backoff_max = 600  # 10 minutes
    retry_jitter = True


@celery_app.task(base=EmailTask, name="send_email")
def send_email_task(
    to_email: str,
    subject: str,
    body_html: Optional[str] = None,
    body_text: Optional[str] = None,
    lead_id: Optional[int] = None,
) -> dict:
    """
    Send email via SMTP.

    Args:
        to_email: Recipient email address
        subject: Email subject
        body_html: HTML body (optional)
        body_text: Plain text body (optional)
        lead_id: Lead ID (optional, for tracking)

    Returns:
        Dict with success status and metadata
    """
    logger.info(f"Sending email to {to_email} (Lead ID: {lead_id})")

    # Create email service
    email_service = EmailService()

    # Send email
    try:
        result = email_service.send_email(
            to_email=to_email,
            subject=subject,
            body_html=body_html,
            body_text=body_text,
        )

        logger.info(f"Email sent successfully to {to_email}")
        return result

    except EmailServiceError as e:
        logger.error(f"Failed to send email: {e}")
        raise


@celery_app.task(base=EmailTask, name="send_welcome_email")
def send_welcome_email_task(
    to_email: str,
    name: str,
    lead_id: Optional[int] = None,
) -> dict:
    """
    Send welcome email to new lead.

    Args:
        to_email: Recipient email
        name: Lead name
        lead_id: Lead ID (optional)

    Returns:
        Dict with success status
    """
    logger.info(f"Sending welcome email to {to_email} (Lead ID: {lead_id})")

    email_service = EmailService()

    try:
        result = email_service.send_welcome_email(
            to_email=to_email,
            name=name,
        )

        logger.info(f"Welcome email sent to {to_email}")
        return result

    except EmailServiceError as e:
        logger.error(f"Failed to send welcome email: {e}")
        raise


@celery_app.task(base=EmailTask, name="send_booking_confirmation_email")
def send_booking_confirmation_email_task(
    to_email: str,
    name: str,
    booking_url: str,
    booking_time: str,
    lead_id: Optional[int] = None,
) -> dict:
    """
    Send booking confirmation email.

    Args:
        to_email: Recipient email
        name: Lead name
        booking_url: Cal.com booking URL
        booking_time: Booking time (human-readable)
        lead_id: Lead ID (optional)

    Returns:
        Dict with success status
    """
    logger.info(f"Sending booking confirmation to {to_email} (Lead ID: {lead_id})")

    email_service = EmailService()

    try:
        result = email_service.send_booking_confirmation(
            to_email=to_email,
            name=name,
            booking_url=booking_url,
            booking_time=booking_time,
        )

        logger.info(f"Booking confirmation sent to {to_email}")
        return result

    except EmailServiceError as e:
        logger.error(f"Failed to send booking confirmation: {e}")
        raise
