"""Booking schemas - Pydantic models for appointment booking."""

from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


class CreateBookingRequest(BaseModel):
    """Request schema for creating a booking."""

    lead_id: int = Field(..., description="Lead ID to create booking for")
    name: str = Field(..., min_length=1, max_length=255, description="Guest name")
    email: EmailStr = Field(..., description="Guest email")
    start_time: Optional[str] = Field(
        None,
        description="Start time in ISO 8601 format (optional)",
        example="2024-01-15T14:00:00Z"
    )
    timezone: str = Field(
        default="Europe/Moscow",
        description="Timezone",
        example="Europe/Moscow"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional metadata"
    )


class BookingResponse(BaseModel):
    """Response schema for booking information."""

    booking_id: int = Field(..., description="Cal.com booking ID")
    booking_uid: str = Field(..., description="Cal.com booking UID")
    booking_url: str = Field(..., description="Meeting URL")
    start_time: str = Field(..., description="Start time")
    end_time: str = Field(..., description="End time")
    status: str = Field(..., description="Booking status")
    lead_id: Optional[int] = Field(None, description="Associated lead ID")

    class Config:
        from_attributes = True


class CancelBookingRequest(BaseModel):
    """Request schema for cancelling a booking."""

    booking_id: int = Field(..., description="Booking ID to cancel")
    cancellation_reason: Optional[str] = Field(
        None,
        max_length=500,
        description="Reason for cancellation"
    )


class RescheduleBookingRequest(BaseModel):
    """Request schema for rescheduling a booking."""

    booking_id: int = Field(..., description="Booking ID to reschedule")
    new_start_time: str = Field(
        ...,
        description="New start time in ISO 8601 format",
        example="2024-01-20T15:00:00Z"
    )
    reschedule_reason: Optional[str] = Field(
        None,
        max_length=500,
        description="Reason for rescheduling"
    )


class AvailabilityRequest(BaseModel):
    """Request schema for checking availability."""

    date_from: Optional[str] = Field(
        None,
        description="Start date in YYYY-MM-DD format",
        example="2024-01-15"
    )
    date_to: Optional[str] = Field(
        None,
        description="End date in YYYY-MM-DD format",
        example="2024-01-20"
    )


class AvailabilitySlot(BaseModel):
    """Availability slot information."""

    time: str = Field(..., description="Time slot in ISO 8601 format")
    available: bool = Field(..., description="Whether slot is available")


class WebhookEvent(BaseModel):
    """Cal.com webhook event schema."""

    event_type: str = Field(..., description="Event type (booking.created, booking.cancelled, etc.)")
    booking_id: int = Field(..., description="Booking ID")
    booking_uid: str = Field(..., description="Booking UID")
    payload: Dict[str, Any] = Field(..., description="Event payload")
    triggered_at: datetime = Field(..., description="When event was triggered")
