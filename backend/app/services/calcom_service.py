"""Cal.com service - Appointment booking integration."""

import logging
from typing import Optional, Dict, Any, List
from datetime import datetime

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


class CalcomServiceError(Exception):
    """Base exception for Cal.com service errors."""
    pass


class CalcomService:
    """
    Service for managing appointments via Cal.com.

    API Documentation: https://cal.com/docs/api-reference
    """

    def __init__(self):
        """Initialize Cal.com service."""
        self.api_url = settings.calcom_api_url
        self.api_key = settings.calcom_api_key
        self.event_type_id = settings.calcom_event_type_id

        # Validate configuration
        if not self.api_key:
            logger.warning("Cal.com API key not configured. Booking will fail.")

    async def create_booking(
        self,
        name: str,
        email: str,
        event_type_id: Optional[int] = None,
        start_time: Optional[str] = None,
        timezone: str = "Europe/Moscow",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Create a new booking.

        Args:
            name: Guest name
            email: Guest email
            event_type_id: Event type ID (optional, uses default if not provided)
            start_time: Start time in ISO 8601 format (optional, for specific time)
            timezone: Timezone (default: Europe/Moscow)
            metadata: Additional metadata to attach to booking

        Returns:
            Booking information with booking ID and meeting URL

        Raises:
            CalcomServiceError: If booking creation fails
        """
        # Use default event type if not provided
        event_type_id = event_type_id or self.event_type_id

        if not event_type_id:
            raise CalcomServiceError("Event type ID not configured")

        # Prepare request data
        data = {
            "eventTypeId": event_type_id,
            "name": name,
            "email": email,
            "timezone": timezone,
        }

        # Add start time if provided
        if start_time:
            data["start"] = start_time

        # Add metadata if provided
        if metadata:
            data["metadata"] = metadata

        # Send request
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/bookings",
                    json=data,
                    headers=headers,
                    timeout=30.0,
                )

                # Check HTTP status
                if response.status_code != 201:
                    error_detail = response.text
                    try:
                        error_json = response.json()
                        error_detail = error_json.get("message", error_detail)
                    except:
                        pass

                    raise CalcomServiceError(
                        f"Cal.com API returned status {response.status_code}: {error_detail}"
                    )

                # Parse response
                result = response.json()

                logger.info(f"Booking created successfully. Booking ID: {result.get('id')}")

                return {
                    "success": True,
                    "booking_id": result.get("id"),
                    "booking_uid": result.get("uid"),
                    "booking_url": result.get("url"),
                    "start_time": result.get("startTime"),
                    "end_time": result.get("endTime"),
                    "status": result.get("status", "accepted"),
                }

        except httpx.HTTPError as e:
            logger.error(f"HTTP error while creating booking: {e}")
            raise CalcomServiceError(f"Failed to create booking: {e}") from e
        except Exception as e:
            logger.error(f"Unexpected error while creating booking: {e}")
            raise CalcomServiceError(f"Failed to create booking: {e}") from e

    async def get_booking(self, booking_id: int) -> Dict[str, Any]:
        """
        Get booking details.

        Args:
            booking_id: Booking ID

        Returns:
            Booking details

        Raises:
            CalcomServiceError: If retrieval fails
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
            }

            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.api_url}/bookings/{booking_id}",
                    headers=headers,
                    timeout=10.0,
                )

                if response.status_code != 200:
                    raise CalcomServiceError(
                        f"Failed to get booking: HTTP {response.status_code}"
                    )

                return response.json()

        except Exception as e:
            logger.error(f"Error getting booking: {e}")
            raise CalcomServiceError(f"Failed to get booking: {e}") from e

    async def cancel_booking(
        self,
        booking_id: int,
        cancellation_reason: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Cancel a booking.

        Args:
            booking_id: Booking ID
            cancellation_reason: Reason for cancellation (optional)

        Returns:
            Cancellation result

        Raises:
            CalcomServiceError: If cancellation fails
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

            data = {}
            if cancellation_reason:
                data["cancellationReason"] = cancellation_reason

            async with httpx.AsyncClient() as client:
                response = await client.delete(
                    f"{self.api_url}/bookings/{booking_id}",
                    headers=headers,
                    json=data if data else None,
                    timeout=10.0,
                )

                if response.status_code not in [200, 204]:
                    raise CalcomServiceError(
                        f"Failed to cancel booking: HTTP {response.status_code}"
                    )

                logger.info(f"Booking {booking_id} cancelled successfully")

                return {
                    "success": True,
                    "booking_id": booking_id,
                    "cancelled_at": datetime.utcnow().isoformat(),
                }

        except Exception as e:
            logger.error(f"Error cancelling booking: {e}")
            raise CalcomServiceError(f"Failed to cancel booking: {e}") from e

    async def reschedule_booking(
        self,
        booking_id: int,
        new_start_time: str,
        cancellation_reason: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Reschedule a booking.

        Args:
            booking_id: Booking ID
            new_start_time: New start time in ISO 8601 format
            cancellation_reason: Reason for rescheduling (optional)

        Returns:
            Rescheduled booking information

        Raises:
            CalcomServiceError: If rescheduling fails
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

            data = {
                "start": new_start_time,
            }

            if cancellation_reason:
                data["rescheduleReason"] = cancellation_reason

            async with httpx.AsyncClient() as client:
                response = await client.patch(
                    f"{self.api_url}/bookings/{booking_id}",
                    headers=headers,
                    json=data,
                    timeout=10.0,
                )

                if response.status_code != 200:
                    raise CalcomServiceError(
                        f"Failed to reschedule booking: HTTP {response.status_code}"
                    )

                result = response.json()

                logger.info(f"Booking {booking_id} rescheduled successfully")

                return {
                    "success": True,
                    "booking_id": result.get("id"),
                    "new_start_time": result.get("startTime"),
                    "new_end_time": result.get("endTime"),
                }

        except Exception as e:
            logger.error(f"Error rescheduling booking: {e}")
            raise CalcomServiceError(f"Failed to reschedule booking: {e}") from e

    async def get_availability(
        self,
        event_type_id: Optional[int] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get available time slots.

        Args:
            event_type_id: Event type ID (optional)
            date_from: Start date in YYYY-MM-DD format (optional)
            date_to: End date in YYYY-MM-DD format (optional)

        Returns:
            List of available time slots

        Raises:
            CalcomServiceError: If retrieval fails
        """
        event_type_id = event_type_id or self.event_type_id

        if not event_type_id:
            raise CalcomServiceError("Event type ID not configured")

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
            }

            params = {
                "eventTypeId": event_type_id,
            }

            if date_from:
                params["dateFrom"] = date_from
            if date_to:
                params["dateTo"] = date_to

            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.api_url}/availability",
                    headers=headers,
                    params=params,
                    timeout=10.0,
                )

                if response.status_code != 200:
                    raise CalcomServiceError(
                        f"Failed to get availability: HTTP {response.status_code}"
                    )

                result = response.json()
                return result.get("slots", [])

        except Exception as e:
            logger.error(f"Error getting availability: {e}")
            raise CalcomServiceError(f"Failed to get availability: {e}") from e
