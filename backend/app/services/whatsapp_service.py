"""WhatsApp service - WhatsApp Business API integration."""

import logging
from typing import Optional, Dict, Any

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


class WhatsAppServiceError(Exception):
    """Base exception for WhatsApp service errors."""
    pass


class WhatsAppService:
    """
    Service for sending messages via WhatsApp Business Cloud API.

    API Documentation: https://developers.facebook.com/docs/whatsapp/cloud-api
    """

    def __init__(self):
        """Initialize WhatsApp service."""
        self.access_token = settings.whatsapp_access_token
        self.phone_number_id = settings.whatsapp_phone_number_id
        self.api_version = settings.whatsapp_api_version
        self.api_url = f"https://graph.facebook.com/{self.api_version}/{self.phone_number_id}/messages"

        # Validate configuration
        if not self.access_token:
            logger.warning("WhatsApp access token not configured. Messaging will fail.")
        if not self.phone_number_id:
            logger.warning("WhatsApp phone number ID not configured. Messaging will fail.")

    async def send_message(
        self,
        to: str,
        message: str,
        preview_url: bool = False,
    ) -> Dict[str, Any]:
        """
        Send text message via WhatsApp Business API.

        Args:
            to: Recipient phone number in international format (e.g., "79991234567")
            message: Message text
            preview_url: Enable URL preview (default: False)

        Returns:
            Dict with message ID and status

        Raises:
            WhatsAppServiceError: If sending fails
        """
        # Validate
        if not to:
            raise WhatsAppServiceError("Recipient phone number is required")

        if not message or len(message) == 0:
            raise WhatsAppServiceError("Message cannot be empty")

        if len(message) > 4096:
            raise WhatsAppServiceError("Message too long (max 4096 characters)")

        # Prepare request
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "text",
            "text": {
                "preview_url": preview_url,
                "body": message,
            },
        }

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        # Send request
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.api_url,
                    json=payload,
                    headers=headers,
                    timeout=30.0,
                )

                # Check HTTP status
                if response.status_code != 200:
                    raise WhatsAppServiceError(
                        f"WhatsApp API returned status {response.status_code}: {response.text}"
                    )

                # Parse response
                result = response.json()

                # Check for errors
                if "error" in result:
                    error = result["error"]
                    error_msg = error.get("message", "Unknown error")
                    error_code = error.get("code", 0)
                    raise WhatsAppServiceError(
                        f"WhatsApp API error {error_code}: {error_msg}"
                    )

                # Extract message ID
                messages = result.get("messages", [])
                message_id = messages[0].get("id") if messages else None

                logger.info(f"WhatsApp message sent successfully. Message ID: {message_id}")

                return {
                    "success": True,
                    "message_id": message_id,
                    "to": to,
                }

        except httpx.HTTPError as e:
            logger.error(f"HTTP error while sending WhatsApp message: {e}")
            raise WhatsAppServiceError(f"Failed to send message: {e}") from e
        except Exception as e:
            logger.error(f"Unexpected error while sending WhatsApp message: {e}")
            raise WhatsAppServiceError(f"Failed to send message: {e}") from e

    async def send_template_message(
        self,
        to: str,
        template_name: str,
        language_code: str = "ru",
        components: Optional[list] = None,
    ) -> Dict[str, Any]:
        """
        Send template message via WhatsApp Business API.

        Args:
            to: Recipient phone number
            template_name: Template name (must be approved in Meta Business Manager)
            language_code: Template language (default: "ru")
            components: Template components (parameters, buttons, etc.)

        Returns:
            Dict with message ID and status

        Raises:
            WhatsAppServiceError: If sending fails
        """
        # Validate
        if not to:
            raise WhatsAppServiceError("Recipient phone number is required")

        if not template_name:
            raise WhatsAppServiceError("Template name is required")

        # Prepare request
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {
                    "code": language_code,
                },
            },
        }

        if components:
            payload["template"]["components"] = components

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        # Send request
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.api_url,
                    json=payload,
                    headers=headers,
                    timeout=30.0,
                )

                # Check HTTP status
                if response.status_code != 200:
                    raise WhatsAppServiceError(
                        f"WhatsApp API returned status {response.status_code}: {response.text}"
                    )

                # Parse response
                result = response.json()

                # Check for errors
                if "error" in result:
                    error = result["error"]
                    error_msg = error.get("message", "Unknown error")
                    error_code = error.get("code", 0)
                    raise WhatsAppServiceError(
                        f"WhatsApp API error {error_code}: {error_msg}"
                    )

                # Extract message ID
                messages = result.get("messages", [])
                message_id = messages[0].get("id") if messages else None

                logger.info(f"WhatsApp template message sent. Message ID: {message_id}")

                return {
                    "success": True,
                    "message_id": message_id,
                    "to": to,
                    "template": template_name,
                }

        except httpx.HTTPError as e:
            logger.error(f"HTTP error while sending WhatsApp template: {e}")
            raise WhatsAppServiceError(f"Failed to send template: {e}") from e
        except Exception as e:
            logger.error(f"Unexpected error while sending WhatsApp template: {e}")
            raise WhatsAppServiceError(f"Failed to send template: {e}") from e
