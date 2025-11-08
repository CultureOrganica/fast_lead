"""Lead service - business logic for lead management."""

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.lead import Lead, LeadStatus
from app.schemas.lead import CreateLeadRequest


class LeadService:
    """Service for managing leads."""

    def __init__(self, db: AsyncSession):
        """Initialize service with database session."""
        self.db = db

    async def create_lead(
        self,
        data: CreateLeadRequest,
        tenant_id: int
    ) -> Lead:
        """
        Create a new lead.

        Args:
            data: Lead creation request data
            tenant_id: ID of the tenant creating the lead

        Returns:
            Created Lead instance
        """
        # Create lead instance
        lead = Lead(
            name=data.name,
            phone=data.phone,
            email=data.email,
            vk_id=data.vk_id,
            channel=data.channel,
            status=LeadStatus.NEW,
            source=data.source,
            consent_gdpr=data.consent.gdpr,
            consent_marketing=data.consent.marketing,
            payload=data.payload,
            tenant_id=tenant_id,
        )

        # Add UTM parameters if provided
        if data.utm:
            lead.utm_source = data.utm.source
            lead.utm_medium = data.utm.medium
            lead.utm_campaign = data.utm.campaign
            lead.utm_content = data.utm.content
            lead.utm_term = data.utm.term

        # Save to database
        self.db.add(lead)
        await self.db.commit()
        await self.db.refresh(lead)

        return lead

    async def get_lead(self, lead_id: int, tenant_id: int) -> Optional[Lead]:
        """
        Get lead by ID.

        Args:
            lead_id: Lead ID
            tenant_id: Tenant ID (for security check)

        Returns:
            Lead instance or None if not found
        """
        result = await self.db.execute(
            select(Lead).where(
                Lead.id == lead_id,
                Lead.tenant_id == tenant_id
            )
        )
        return result.scalar_one_or_none()

    async def get_next_action(self, lead: Lead) -> str:
        """
        Determine next action for the lead based on channel.

        Args:
            lead: Lead instance

        Returns:
            Next action recommendation (e.g., 'send_sms', 'send_email')
        """
        channel_to_action = {
            "web": "open_chat",
            "sms": "send_sms",
            "email": "send_email",
            "vk": "send_vk_message",
            "telegram": "send_telegram_message",
            "whatsapp": "send_whatsapp_message",
            "instagram": "send_instagram_message",
            "max": "send_max_message",
        }
        return channel_to_action.get(lead.channel.value, "manual_review")
