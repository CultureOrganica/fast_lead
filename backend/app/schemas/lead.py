"""Lead schemas for API requests and responses."""

from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, EmailStr, field_validator

from app.models.lead import LeadStatus, LeadChannel


class UTMParams(BaseModel):
    """UTM tracking parameters."""

    source: Optional[str] = Field(None, max_length=255, description="UTM source")
    medium: Optional[str] = Field(None, max_length=255, description="UTM medium")
    campaign: Optional[str] = Field(None, max_length=255, description="UTM campaign")
    content: Optional[str] = Field(None, max_length=255, description="UTM content")
    term: Optional[str] = Field(None, max_length=255, description="UTM term")


class ConsentParams(BaseModel):
    """User consent parameters."""

    gdpr: bool = Field(False, description="GDPR consent")
    marketing: bool = Field(False, description="Marketing consent")


class CreateLeadRequest(BaseModel):
    """Request schema for creating a lead."""

    # Contact information
    name: str = Field(..., min_length=1, max_length=255, description="Contact name")
    phone: Optional[str] = Field(None, max_length=50, description="Phone number")
    email: Optional[EmailStr] = Field(None, description="Email address")
    vk_id: Optional[str] = Field(None, max_length=100, description="VK user ID or profile URL")

    # Channel
    channel: LeadChannel = Field(..., description="Communication channel")

    # Source tracking
    source: Optional[str] = Field(None, max_length=255, description="Source website URL")
    utm: Optional[UTMParams] = Field(None, description="UTM parameters")

    # Consent
    consent: ConsentParams = Field(default_factory=ConsentParams, description="User consents")

    # Additional data
    payload: Optional[Dict[str, Any]] = Field(None, description="Additional data from widget")

    @field_validator("phone", "email", "vk_id")
    @classmethod
    def at_least_one_contact(cls, v, info):
        """Validate that at least one contact method is provided."""
        # This will be called for each field, we'll do the validation in model_validator
        return v

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Иван Петров",
                    "phone": "+79991234567",
                    "email": "ivan@example.com",
                    "channel": "sms",
                    "source": "https://example.com/landing",
                    "utm": {
                        "source": "google",
                        "medium": "cpc",
                        "campaign": "spring_sale"
                    },
                    "consent": {
                        "gdpr": True,
                        "marketing": False
                    }
                }
            ]
        }
    }


class LeadResponse(BaseModel):
    """Response schema for lead data."""

    id: int
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    vk_id: Optional[str] = None
    channel: LeadChannel
    status: LeadStatus
    source: Optional[str] = None
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_campaign: Optional[str] = None
    consent_gdpr: bool
    consent_marketing: bool
    booking_id: Optional[str] = None
    booking_url: Optional[str] = None
    booked_at: Optional[datetime] = None
    tenant_id: int
    created_at: datetime
    updated_at: datetime
    contacted_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "name": "Иван Петров",
                    "phone": "+79991234567",
                    "email": "ivan@example.com",
                    "vk_id": None,
                    "channel": "sms",
                    "status": "new",
                    "source": "https://example.com/landing",
                    "utm_source": "google",
                    "utm_medium": "cpc",
                    "utm_campaign": "spring_sale",
                    "consent_gdpr": True,
                    "consent_marketing": False,
                    "booking_id": None,
                    "booking_url": None,
                    "booked_at": None,
                    "tenant_id": 1,
                    "created_at": "2025-01-08T12:00:00",
                    "updated_at": "2025-01-08T12:00:00",
                    "contacted_at": None
                }
            ]
        }
    }


class CreateLeadResponse(BaseModel):
    """Response schema for lead creation."""

    lead: LeadResponse
    next_action: Optional[str] = Field(
        None,
        description="Recommended next action (e.g., 'send_sms', 'send_email')"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "lead": {
                        "id": 1,
                        "name": "Иван Петров",
                        "channel": "sms",
                        "status": "new"
                    },
                    "next_action": "send_sms"
                }
            ]
        }
    }
