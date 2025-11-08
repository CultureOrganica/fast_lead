"""Booking API endpoints - Appointment booking via Cal.com."""

import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from app.core.database import get_db
from app.models.lead import Lead, LeadStatus
from app.schemas.booking import (
    CreateBookingRequest,
    BookingResponse,
    CancelBookingRequest,
    RescheduleBookingRequest,
    AvailabilityRequest,
    AvailabilitySlot,
)
from app.services.calcom_service import CalcomService, CalcomServiceError

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post("", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
async def create_booking(
    data: CreateBookingRequest,
    db: AsyncSession = Depends(get_db),
) -> BookingResponse:
    """
    Create a new appointment booking for a lead.

    This endpoint:
    1. Validates the lead exists
    2. Creates a booking in Cal.com
    3. Updates the lead with booking information
    4. Returns booking details

    **Required fields:**
    - lead_id: ID of the lead to book for
    - name: Guest name
    - email: Guest email

    **Optional fields:**
    - start_time: Specific time (if not provided, Cal.com will suggest times)
    - timezone: Timezone (default: Europe/Moscow)
    - metadata: Additional booking metadata
    """
    # Get lead
    result = await db.execute(
        select(Lead).where(Lead.id == data.lead_id)
    )
    lead = result.scalar_one_or_none()

    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lead {data.lead_id} not found"
        )

    # Check if lead already has a booking
    if lead.booking_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Lead {data.lead_id} already has a booking"
        )

    # Create booking via Cal.com
    calcom = CalcomService()

    try:
        booking_result = await calcom.create_booking(
            name=data.name,
            email=data.email,
            start_time=data.start_time,
            timezone=data.timezone,
            metadata={
                **(data.metadata or {}),
                "lead_id": lead.id,
                "tenant_id": lead.tenant_id,
            },
        )
    except CalcomServiceError as e:
        logger.error(f"Failed to create booking for lead {lead.id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create booking: {str(e)}"
        )

    # Update lead with booking information
    try:
        lead.booking_id = str(booking_result["booking_id"])
        lead.booking_url = booking_result["booking_url"]
        lead.booked_at = booking_result["start_time"]
        lead.status = LeadStatus.BOOKED

        await db.commit()
        await db.refresh(lead)

        logger.info(f"Booking created for lead {lead.id}: {booking_result['booking_id']}")

    except Exception as e:
        await db.rollback()
        logger.error(f"Failed to update lead with booking info: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Booking created but failed to update lead"
        )

    return BookingResponse(
        booking_id=booking_result["booking_id"],
        booking_uid=booking_result["booking_uid"],
        booking_url=booking_result["booking_url"],
        start_time=booking_result["start_time"],
        end_time=booking_result["end_time"],
        status=booking_result["status"],
        lead_id=lead.id,
    )


@router.delete("/{booking_id}", status_code=status.HTTP_200_OK)
async def cancel_booking(
    booking_id: int,
    data: CancelBookingRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Cancel an existing booking.

    This endpoint:
    1. Finds the lead with this booking
    2. Cancels the booking in Cal.com
    3. Updates lead status
    """
    # Find lead with this booking
    result = await db.execute(
        select(Lead).where(Lead.booking_id == str(booking_id))
    )
    lead = result.scalar_one_or_none()

    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Booking {booking_id} not found"
        )

    # Cancel booking in Cal.com
    calcom = CalcomService()

    try:
        await calcom.cancel_booking(
            booking_id=booking_id,
            cancellation_reason=data.cancellation_reason,
        )
    except CalcomServiceError as e:
        logger.error(f"Failed to cancel booking {booking_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to cancel booking: {str(e)}"
        )

    # Update lead
    try:
        lead.status = LeadStatus.QUALIFIED  # Move back to qualified
        # Keep booking_id and booking_url for history

        await db.commit()

        logger.info(f"Booking {booking_id} cancelled for lead {lead.id}")

        return {
            "success": True,
            "booking_id": booking_id,
            "lead_id": lead.id,
            "message": "Booking cancelled successfully",
        }

    except Exception as e:
        await db.rollback()
        logger.error(f"Failed to update lead after cancellation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Booking cancelled but failed to update lead"
        )


@router.patch("/{booking_id}", response_model=BookingResponse)
async def reschedule_booking(
    booking_id: int,
    data: RescheduleBookingRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Reschedule an existing booking.

    This endpoint:
    1. Finds the lead with this booking
    2. Reschedules the booking in Cal.com
    3. Updates lead with new time
    """
    # Find lead with this booking
    result = await db.execute(
        select(Lead).where(Lead.booking_id == str(booking_id))
    )
    lead = result.scalar_one_or_none()

    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Booking {booking_id} not found"
        )

    # Reschedule booking in Cal.com
    calcom = CalcomService()

    try:
        reschedule_result = await calcom.reschedule_booking(
            booking_id=booking_id,
            new_start_time=data.new_start_time,
            cancellation_reason=data.reschedule_reason,
        )
    except CalcomServiceError as e:
        logger.error(f"Failed to reschedule booking {booking_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to reschedule booking: {str(e)}"
        )

    # Update lead with new time
    try:
        lead.booked_at = reschedule_result["new_start_time"]

        await db.commit()
        await db.refresh(lead)

        logger.info(f"Booking {booking_id} rescheduled for lead {lead.id}")

        # Get full booking details
        booking_details = await calcom.get_booking(booking_id)

        return BookingResponse(
            booking_id=booking_id,
            booking_uid=booking_details.get("uid", ""),
            booking_url=lead.booking_url or "",
            start_time=reschedule_result["new_start_time"],
            end_time=reschedule_result["new_end_time"],
            status="rescheduled",
            lead_id=lead.id,
        )

    except Exception as e:
        await db.rollback()
        logger.error(f"Failed to update lead after rescheduling: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Booking rescheduled but failed to update lead"
        )


@router.get("/availability", response_model=List[AvailabilitySlot])
async def get_availability(
    date_from: str = None,
    date_to: str = None,
):
    """
    Get available time slots from Cal.com.

    **Query parameters:**
    - date_from: Start date in YYYY-MM-DD format (optional)
    - date_to: End date in YYYY-MM-DD format (optional)

    Returns a list of available time slots.
    """
    calcom = CalcomService()

    try:
        slots = await calcom.get_availability(
            date_from=date_from,
            date_to=date_to,
        )

        # Convert to response format
        return [
            AvailabilitySlot(
                time=slot.get("time"),
                available=slot.get("available", True),
            )
            for slot in slots
        ]

    except CalcomServiceError as e:
        logger.error(f"Failed to get availability: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get availability: {str(e)}"
        )
