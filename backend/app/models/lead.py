"""Lead model - represents leads captured through the widget."""

import enum
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey, Enum, JSON, Text
from sqlalchemy.orm import relationship
from app.core.database import Base


class LeadStatus(str, enum.Enum):
    """Lead status enum."""

    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    BOOKED = "booked"
    COMPLETED = "completed"
    LOST = "lost"


class LeadChannel(str, enum.Enum):
    """Lead channel enum."""

    WEB = "web"
    SMS = "sms"
    EMAIL = "email"
    VK = "vk"
    TELEGRAM = "telegram"
    WHATSAPP = "whatsapp"
    INSTAGRAM = "instagram"
    MAX = "max"


class Lead(Base):
    """
    Lead model.

    Represents a lead captured through the widget on a client's website.
    Contains contact information, channel preference, and status tracking.
    """

    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)

    # Contact information
    name = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=True, index=True)
    email = Column(String(255), nullable=True, index=True)
    vk_id = Column(String(100), nullable=True, index=True)

    # Channel and status
    channel = Column(Enum(LeadChannel), nullable=False, index=True)
    status = Column(Enum(LeadStatus), default=LeadStatus.NEW, nullable=False, index=True)

    # Source tracking
    source = Column(String(255), nullable=True)  # website URL
    utm_source = Column(String(255), nullable=True)
    utm_medium = Column(String(255), nullable=True)
    utm_campaign = Column(String(255), nullable=True)
    utm_content = Column(String(255), nullable=True)
    utm_term = Column(String(255), nullable=True)

    # Consent
    consent_gdpr = Column(Boolean, default=False, nullable=False)
    consent_marketing = Column(Boolean, default=False, nullable=False)

    # Booking information
    booking_id = Column(String(255), nullable=True)
    booking_url = Column(String(500), nullable=True)
    booked_at = Column(DateTime, nullable=True)

    # Additional data
    payload = Column(JSON, nullable=True)  # Extra data from widget
    notes = Column(Text, nullable=True)

    # Tenant relationship
    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    tenant = relationship("Tenant", back_populates="leads")

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    contacted_at = Column(DateTime, nullable=True)

    def __repr__(self) -> str:
        return f"<Lead(id={self.id}, name='{self.name}', channel='{self.channel}', status='{self.status}')>"
