"""SMS service - SMSC.ru integration."""

import hashlib
import logging
from typing import Optional, Dict, Any
from urllib.parse import urlencode

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


class SMSServiceError(Exception):
    """Base exception for SMS service errors."""
    pass


class SMSService:
    """
    Service for sending SMS via SMSC.ru.

    API Documentation: https://smsc.ru/api/http/
    """

    def __init__(self):
        """Initialize SMS service."""
        self.api_url = settings.smsc_api_url
        self.login = settings.smsc_login
        self.password = settings.smsc_password
        self.sender = settings.smsc_sender

        # Validate configuration
        if not self.login or not self.password:
            logger.warning("SMSC credentials not configured. SMS sending will fail.")

    async def send_sms(
        self,
        phone: str,
        message: str,
        sender: Optional[str] = None,
        translit: bool = False,
    ) -> Dict[str, Any]:
        """
        Send SMS message.

        Args:
            phone: Phone number in international format (e.g., 79991234567)
            message: Message text (up to 1000 characters)
            sender: Sender name (optional, defaults to configured sender)
            translit: Transliterate message to Latin (optional)

        Returns:
            Response from SMSC.ru API with message ID and status

        Raises:
            SMSServiceError: If SMS sending fails
        """
        # Clean phone number (remove +, spaces, etc.)
        phone = self._clean_phone(phone)

        # Validate phone number
        if not self._validate_phone(phone):
            raise SMSServiceError(f"Invalid phone number: {phone}")

        # Validate message
        if not message or len(message) == 0:
            raise SMSServiceError("Message cannot be empty")

        if len(message) > 1000:
            raise SMSServiceError("Message too long (max 1000 characters)")

        # Prepare request parameters
        params = {
            "login": self.login,
            "psw": self.password,
            "phones": phone,
            "mes": message,
            "sender": sender or self.sender,
            "charset": "utf-8",
            "fmt": 3,  # JSON response format
        }

        # Add optional parameters
        if translit:
            params["translit"] = 1

        # Send request
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.api_url,
                    data=params,
                    timeout=30.0,
                )

                # Check HTTP status
                if response.status_code != 200:
                    raise SMSServiceError(
                        f"SMSC API returned status {response.status_code}: {response.text}"
                    )

                # Parse JSON response
                result = response.json()

                # Check for errors
                if "error" in result or "error_code" in result:
                    error_code = result.get("error_code", result.get("error"))
                    error_text = result.get("error_text", "Unknown error")
                    raise SMSServiceError(
                        f"SMSC API error {error_code}: {error_text}"
                    )

                logger.info(
                    f"SMS sent successfully to {phone}. Message ID: {result.get('id')}"
                )

                return {
                    "success": True,
                    "message_id": result.get("id"),
                    "count": result.get("cnt", 1),
                    "cost": result.get("cost", 0),
                    "balance": result.get("balance"),
                }

        except httpx.HTTPError as e:
            logger.error(f"HTTP error while sending SMS: {e}")
            raise SMSServiceError(f"Failed to send SMS: {e}") from e
        except Exception as e:
            logger.error(f"Unexpected error while sending SMS: {e}")
            raise SMSServiceError(f"Failed to send SMS: {e}") from e

    async def get_balance(self) -> float:
        """
        Get account balance.

        Returns:
            Balance in rubles

        Raises:
            SMSServiceError: If balance check fails
        """
        params = {
            "login": self.login,
            "psw": self.password,
            "fmt": 3,  # JSON response
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://smsc.ru/sys/balance.php",
                    data=params,
                    timeout=10.0,
                )

                result = response.json()

                if "balance" in result:
                    return float(result["balance"])
                else:
                    raise SMSServiceError("Failed to get balance")

        except Exception as e:
            logger.error(f"Error checking balance: {e}")
            raise SMSServiceError(f"Failed to check balance: {e}") from e

    async def get_status(self, message_id: int, phone: str) -> Dict[str, Any]:
        """
        Check message delivery status.

        Args:
            message_id: Message ID from send_sms response
            phone: Phone number

        Returns:
            Status information

        Raises:
            SMSServiceError: If status check fails
        """
        phone = self._clean_phone(phone)

        params = {
            "login": self.login,
            "psw": self.password,
            "phone": phone,
            "id": message_id,
            "fmt": 3,
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://smsc.ru/sys/status.php",
                    data=params,
                    timeout=10.0,
                )

                result = response.json()

                return {
                    "status": result.get("status"),
                    "status_name": result.get("status_name"),
                    "last_date": result.get("last_date"),
                    "last_timestamp": result.get("last_timestamp"),
                    "err": result.get("err"),
                }

        except Exception as e:
            logger.error(f"Error checking status: {e}")
            raise SMSServiceError(f"Failed to check status: {e}") from e

    def _clean_phone(self, phone: str) -> str:
        """
        Clean phone number (remove +, spaces, dashes, etc.).

        Args:
            phone: Phone number

        Returns:
            Cleaned phone number (digits only)
        """
        return "".join(c for c in phone if c.isdigit())

    def _validate_phone(self, phone: str) -> bool:
        """
        Validate phone number format.

        Args:
            phone: Phone number (digits only)

        Returns:
            True if valid, False otherwise
        """
        # Russian phone number: 11 digits starting with 7
        if len(phone) == 11 and phone.startswith("7"):
            return True

        # International format: 10-15 digits
        if 10 <= len(phone) <= 15:
            return True

        return False
