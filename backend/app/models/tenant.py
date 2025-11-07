"""Tenant model - represents a client/organization using Fast Lead."""

from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Integer, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


class Tenant(Base):
    """
    Tenant model.

    Represents an organization/client using Fast Lead platform.
    Each tenant can have multiple users, leads, and widget configurations.
    """

    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    domain = Column(String(255), nullable=True)

    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    is_trial = Column(Boolean, default=True, nullable=False)
    trial_ends_at = Column(DateTime, nullable=True)

    # Subscription
    subscription_plan = Column(String(50), nullable=True)  # trial, start, pro, business
    subscription_status = Column(String(50), nullable=True)  # active, cancelled, expired

    # Widget configuration
    widget_config = Column(JSON, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    users = relationship("User", back_populates="tenant", cascade="all, delete-orphan")
    leads = relationship("Lead", back_populates="tenant", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Tenant(id={self.id}, name='{self.name}', slug='{self.slug}')>"
