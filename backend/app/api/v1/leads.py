"""Leads API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.lead import CreateLeadRequest, CreateLeadResponse, LeadResponse
from app.services.lead_service import LeadService

router = APIRouter(prefix="/leads", tags=["leads"])


async def get_tenant_id_from_header(
    x_tenant_id: int = Header(..., description="Tenant ID from widget configuration")
) -> int:
    """
    Extract tenant ID from request header.

    In production, this would validate the tenant ID against a token or API key.
    For MVP, we accept the tenant ID directly from the header.

    Args:
        x_tenant_id: Tenant ID from X-Tenant-Id header

    Returns:
        Validated tenant ID

    Raises:
        HTTPException: If tenant ID is invalid
    """
    if x_tenant_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid tenant ID"
        )
    return x_tenant_id


@router.post(
    "",
    response_model=CreateLeadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new lead",
    description="""
    Create a new lead from widget submission.

    This endpoint is called by the widget when a user submits their contact information.
    The lead is created with status 'new' and can be processed by the orchestrator.

    **Headers:**
    - `X-Tenant-Id`: Tenant ID from widget configuration (required)

    **Request Body:**
    - `name`: Contact name (required)
    - `phone`, `email`, or `vk_id`: At least one contact method (required)
    - `channel`: Communication channel preference (required)
    - `source`: Source website URL (optional)
    - `utm`: UTM tracking parameters (optional)
    - `consent`: User consent for GDPR and marketing (optional)
    - `payload`: Additional data from widget (optional)

    **Response:**
    - `lead`: Created lead object
    - `next_action`: Recommended next action for the orchestrator

    **Example:**
    ```bash
    curl -X POST "http://localhost:8000/api/v1/leads" \\
      -H "Content-Type: application/json" \\
      -H "X-Tenant-Id: 1" \\
      -d '{
        "name": "Иван Петров",
        "phone": "+79991234567",
        "channel": "sms",
        "consent": {"gdpr": true, "marketing": false}
      }'
    ```
    """,
)
async def create_lead(
    data: CreateLeadRequest,
    db: AsyncSession = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id_from_header),
):
    """Create a new lead from widget submission."""
    # Validate that at least one contact method is provided
    if not any([data.phone, data.email, data.vk_id]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one contact method (phone, email, or vk_id) is required"
        )

    # Channel-specific validation
    if data.channel == "sms" and not data.phone:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number is required for SMS channel"
        )

    if data.channel == "email" and not data.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is required for Email channel"
        )

    if data.channel == "vk" and not data.vk_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="VK ID is required for VK channel"
        )

    if data.channel == "whatsapp" and not data.consent.marketing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Marketing consent is required for WhatsApp channel"
        )

    # Create lead
    service = LeadService(db)
    lead = await service.create_lead(data, tenant_id)

    # Get next action
    next_action = await service.get_next_action(lead)

    # Trigger orchestrator task to process the lead asynchronously
    from app.tasks.lead_tasks import process_new_lead_task
    process_new_lead_task.delay(lead.id)

    return CreateLeadResponse(
        lead=LeadResponse.model_validate(lead),
        next_action=next_action
    )


@router.get(
    "/{lead_id}",
    response_model=LeadResponse,
    summary="Get lead by ID",
    description="Retrieve a specific lead by its ID. Requires tenant ID for security."
)
async def get_lead(
    lead_id: int,
    db: AsyncSession = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id_from_header),
):
    """Get lead by ID."""
    service = LeadService(db)
    lead = await service.get_lead(lead_id, tenant_id)

    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lead with id {lead_id} not found"
        )

    return LeadResponse.model_validate(lead)
