"""Email service - SMTP email sending."""

import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, List, Dict, Any

from app.core.config import settings

logger = logging.getLogger(__name__)


class EmailServiceError(Exception):
    """Base exception for email service errors."""
    pass


class EmailService:
    """
    Service for sending emails via SMTP.

    Supports HTML and plain text emails with attachments.
    """

    def __init__(self):
        """Initialize email service."""
        self.smtp_host = settings.smtp_host
        self.smtp_port = settings.smtp_port
        self.smtp_user = settings.smtp_user
        self.smtp_password = settings.smtp_password
        self.from_email = settings.smtp_from_email
        self.from_name = settings.smtp_from_name
        self.use_tls = settings.smtp_use_tls

        # Validate configuration
        if not self.smtp_host or not self.smtp_user:
            logger.warning("SMTP credentials not configured. Email sending will fail.")

    def send_email(
        self,
        to_email: str,
        subject: str,
        body_html: Optional[str] = None,
        body_text: Optional[str] = None,
        reply_to: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Send email.

        Args:
            to_email: Recipient email address
            subject: Email subject
            body_html: HTML body (optional)
            body_text: Plain text body (optional, falls back to HTML if not provided)
            reply_to: Reply-To email (optional)

        Returns:
            Dict with success status and message ID

        Raises:
            EmailServiceError: If email sending fails
        """
        # Validate
        if not to_email:
            raise EmailServiceError("Recipient email is required")

        if not subject:
            raise EmailServiceError("Subject is required")

        if not body_html and not body_text:
            raise EmailServiceError("Email body is required (HTML or text)")

        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = f"{self.from_name} <{self.from_email}>"
        msg['To'] = to_email

        if reply_to:
            msg['Reply-To'] = reply_to

        # Add text part
        if body_text:
            text_part = MIMEText(body_text, 'plain', 'utf-8')
            msg.attach(text_part)

        # Add HTML part
        if body_html:
            html_part = MIMEText(body_html, 'html', 'utf-8')
            msg.attach(html_part)

        # Send email
        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=30) as server:
                if self.use_tls:
                    server.starttls()

                if self.smtp_user and self.smtp_password:
                    server.login(self.smtp_user, self.smtp_password)

                server.send_message(msg)

            logger.info(f"Email sent successfully to {to_email}")

            return {
                "success": True,
                "to_email": to_email,
                "subject": subject,
            }

        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"SMTP authentication failed: {e}")
            raise EmailServiceError(f"Authentication failed: {e}") from e

        except smtplib.SMTPException as e:
            logger.error(f"SMTP error while sending email: {e}")
            raise EmailServiceError(f"Failed to send email: {e}") from e

        except Exception as e:
            logger.error(f"Unexpected error while sending email: {e}")
            raise EmailServiceError(f"Failed to send email: {e}") from e

    def send_welcome_email(
        self,
        to_email: str,
        name: str,
        company_name: str = "Fast Lead",
    ) -> Dict[str, Any]:
        """
        Send welcome email to new lead.

        Args:
            to_email: Recipient email
            name: Lead name
            company_name: Company name

        Returns:
            Send result
        """
        subject = f"Спасибо за интерес к {company_name}"

        body_html = f"""
        <html>
          <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
              <h2 style="color: #2563eb;">Здравствуйте, {name}!</h2>

              <p>Спасибо за интерес к нашим услугам.</p>

              <p>Наш специалист свяжется с вами в ближайшее время для обсуждения деталей.</p>

              <p>Если у вас есть срочные вопросы, вы можете ответить на это письмо.</p>

              <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
                <p style="color: #666; font-size: 14px;">
                  С уважением,<br>
                  Команда {company_name}
                </p>
              </div>
            </div>
          </body>
        </html>
        """

        body_text = f"""
Здравствуйте, {name}!

Спасибо за интерес к нашим услугам.

Наш специалист свяжется с вами в ближайшее время для обсуждения деталей.

Если у вас есть срочные вопросы, вы можете ответить на это письмо.

С уважением,
Команда {company_name}
        """

        return self.send_email(
            to_email=to_email,
            subject=subject,
            body_html=body_html,
            body_text=body_text,
        )

    def send_booking_confirmation(
        self,
        to_email: str,
        name: str,
        booking_url: str,
        booking_time: str,
    ) -> Dict[str, Any]:
        """
        Send booking confirmation email.

        Args:
            to_email: Recipient email
            name: Lead name
            booking_url: Cal.com booking URL
            booking_time: Booking time (human-readable)

        Returns:
            Send result
        """
        subject = "Подтверждение встречи"

        body_html = f"""
        <html>
          <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
              <h2 style="color: #2563eb;">Встреча подтверждена!</h2>

              <p>Здравствуйте, {name}!</p>

              <p>Ваша встреча успешно забронирована на <strong>{booking_time}</strong>.</p>

              <div style="margin: 30px 0; padding: 20px; background-color: #f3f4f6; border-radius: 8px;">
                <p style="margin: 0;">
                  <a href="{booking_url}"
                     style="display: inline-block; padding: 12px 24px; background-color: #2563eb; color: white; text-decoration: none; border-radius: 6px;">
                    Открыть встречу
                  </a>
                </p>
              </div>

              <p>По этой ссылке вы сможете:</p>
              <ul>
                <li>Добавить встречу в календарь</li>
                <li>Перенести встречу</li>
                <li>Отменить встречу</li>
              </ul>

              <p>До встречи!</p>

              <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
                <p style="color: #666; font-size: 14px;">
                  С уважением,<br>
                  Команда Fast Lead
                </p>
              </div>
            </div>
          </body>
        </html>
        """

        body_text = f"""
Встреча подтверждена!

Здравствуйте, {name}!

Ваша встреча успешно забронирована на {booking_time}.

Ссылка на встречу: {booking_url}

По этой ссылке вы сможете:
- Добавить встречу в календарь
- Перенести встречу
- Отменить встречу

До встречи!

С уважением,
Команда Fast Lead
        """

        return self.send_email(
            to_email=to_email,
            subject=subject,
            body_html=body_html,
            body_text=body_text,
        )
