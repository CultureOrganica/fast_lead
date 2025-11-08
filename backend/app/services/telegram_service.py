"""Telegram service - Telegram Bot API integration."""

import logging
from typing import Optional, Dict, Any

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


class TelegramServiceError(Exception):
    """Base exception for Telegram service errors."""
    pass


class TelegramService:
    """
    Service for sending messages via Telegram Bot API.

    API Documentation: https://core.telegram.org/bots/api
    """

    def __init__(self):
        """Initialize Telegram service."""
        self.bot_token = settings.telegram_bot_token
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}"

        # Validate configuration
        if not self.bot_token:
            logger.warning("Telegram bot token not configured. Messaging will fail.")

    async def send_message(
        self,
        chat_id: int,
        text: str,
        parse_mode: Optional[str] = None,
        reply_markup: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Send message to Telegram chat.

        Args:
            chat_id: Chat ID or user ID
            text: Message text
            parse_mode: Parse mode (Markdown, HTML, or None)
            reply_markup: Inline keyboard (optional)

        Returns:
            Dict with message ID and status

        Raises:
            TelegramServiceError: If sending fails
        """
        # Validate
        if not chat_id:
            raise TelegramServiceError("Chat ID is required")

        if not text or len(text) == 0:
            raise TelegramServiceError("Message cannot be empty")

        if len(text) > 4096:
            raise TelegramServiceError("Message too long (max 4096 characters)")

        # Prepare request
        payload = {
            "chat_id": chat_id,
            "text": text,
        }

        if parse_mode:
            payload["parse_mode"] = parse_mode

        if reply_markup:
            payload["reply_markup"] = reply_markup

        # Send request
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/sendMessage",
                    json=payload,
                    timeout=30.0,
                )

                # Check HTTP status
                if response.status_code != 200:
                    raise TelegramServiceError(
                        f"Telegram API returned status {response.status_code}: {response.text}"
                    )

                # Parse response
                result = response.json()

                # Check for errors
                if not result.get("ok"):
                    error_code = result.get("error_code", 0)
                    description = result.get("description", "Unknown error")
                    raise TelegramServiceError(
                        f"Telegram API error {error_code}: {description}"
                    )

                message_data = result.get("result", {})
                message_id = message_data.get("message_id")

                logger.info(f"Telegram message sent successfully. Message ID: {message_id}")

                return {
                    "success": True,
                    "message_id": message_id,
                    "chat_id": chat_id,
                }

        except httpx.HTTPError as e:
            logger.error(f"HTTP error while sending Telegram message: {e}")
            raise TelegramServiceError(f"Failed to send message: {e}") from e
        except Exception as e:
            logger.error(f"Unexpected error while sending Telegram message: {e}")
            raise TelegramServiceError(f"Failed to send message: {e}") from e
