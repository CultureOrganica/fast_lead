"""VK service - VK Bots API integration."""

import logging
from typing import Optional, Dict, Any

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


class VKServiceError(Exception):
    """Base exception for VK service errors."""
    pass


class VKService:
    """
    Service for sending messages via VK Bots API.

    API Documentation: https://dev.vk.com/method/messages
    """

    def __init__(self):
        """Initialize VK service."""
        self.access_token = settings.vk_access_token
        self.api_version = settings.vk_api_version
        self.group_id = settings.vk_group_id
        self.api_url = "https://api.vk.com/method"

        # Validate configuration
        if not self.access_token:
            logger.warning("VK access token not configured. VK messaging will fail.")

    async def send_message(
        self,
        user_id: int,
        message: str,
        keyboard: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Send message to VK user.

        Args:
            user_id: VK user ID
            message: Message text
            keyboard: Keyboard JSON (optional)

        Returns:
            Dict with message ID and status

        Raises:
            VKServiceError: If sending fails
        """
        # Validate
        if not user_id:
            raise VKServiceError("User ID is required")

        if not message or len(message) == 0:
            raise VKServiceError("Message cannot be empty")

        if len(message) > 4096:
            raise VKServiceError("Message too long (max 4096 characters)")

        # Prepare request
        import random
        params = {
            "user_id": user_id,
            "message": message,
            "random_id": random.randint(0, 2**31),
            "access_token": self.access_token,
            "v": self.api_version,
        }

        if keyboard:
            import json
            params["keyboard"] = json.dumps(keyboard)

        # Send request
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/messages.send",
                    data=params,
                    timeout=30.0,
                )

                # Check HTTP status
                if response.status_code != 200:
                    raise VKServiceError(
                        f"VK API returned status {response.status_code}: {response.text}"
                    )

                # Parse response
                result = response.json()

                # Check for errors
                if "error" in result:
                    error = result["error"]
                    error_msg = error.get("error_msg", "Unknown error")
                    error_code = error.get("error_code", 0)
                    raise VKServiceError(
                        f"VK API error {error_code}: {error_msg}"
                    )

                message_id = result.get("response")

                logger.info(f"VK message sent successfully. Message ID: {message_id}")

                return {
                    "success": True,
                    "message_id": message_id,
                    "user_id": user_id,
                }

        except httpx.HTTPError as e:
            logger.error(f"HTTP error while sending VK message: {e}")
            raise VKServiceError(f"Failed to send message: {e}") from e
        except Exception as e:
            logger.error(f"Unexpected error while sending VK message: {e}")
            raise VKServiceError(f"Failed to send message: {e}") from e
