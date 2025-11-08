"""Pydantic schemas for API requests and responses."""

from app.schemas.lead import (
    CreateLeadRequest,
    LeadResponse,
    CreateLeadResponse,
    UTMParams,
    ConsentParams,
)
from app.schemas.booking import (
    CreateBookingRequest,
    BookingResponse,
    CancelBookingRequest,
    RescheduleBookingRequest,
    AvailabilityRequest,
    AvailabilitySlot,
    WebhookEvent,
)

__all__ = [
    "CreateLeadRequest",
    "LeadResponse",
    "CreateLeadResponse",
    "UTMParams",
    "ConsentParams",
    "CreateBookingRequest",
    "BookingResponse",
    "CancelBookingRequest",
    "RescheduleBookingRequest",
    "AvailabilityRequest",
    "AvailabilitySlot",
    "WebhookEvent",
]
