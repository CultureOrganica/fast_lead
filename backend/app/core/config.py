"""Application configuration."""

from typing import List
from pydantic import Field, PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = "Fast Lead"
    app_version: str = "0.1.0"
    environment: str = Field(default="development", alias="ENVIRONMENT")
    debug: bool = Field(default=True, alias="DEBUG")
    secret_key: str = Field(..., alias="SECRET_KEY")

    # API
    api_v1_prefix: str = Field(default="/api/v1", alias="API_V1_PREFIX")

    # CORS
    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:3001", "http://localhost:5173"],
        alias="CORS_ORIGINS"
    )
    cors_allow_credentials: bool = Field(default=True, alias="CORS_ALLOW_CREDENTIALS")

    # Database
    database_url: PostgresDsn = Field(..., alias="DATABASE_URL")
    database_pool_size: int = Field(default=20, alias="DATABASE_POOL_SIZE")
    database_max_overflow: int = Field(default=10, alias="DATABASE_MAX_OVERFLOW")

    # Redis
    redis_url: RedisDsn = Field(..., alias="REDIS_URL")

    # Celery
    celery_broker_url: str = Field(..., alias="CELERY_BROKER_URL")
    celery_result_backend: str = Field(..., alias="CELERY_RESULT_BACKEND")

    # SMSC.ru (SMS provider)
    smsc_login: str = Field(default="", alias="SMSC_LOGIN")
    smsc_password: str = Field(default="", alias="SMSC_PASSWORD")
    smsc_sender: str = Field(default="FastLead", alias="SMSC_SENDER")
    smsc_api_url: str = Field(default="https://smsc.ru/sys/send.php", alias="SMSC_API_URL")

    # Cal.com (Appointment booking)
    calcom_api_key: str = Field(default="", alias="CALCOM_API_KEY")
    calcom_api_url: str = Field(default="https://api.cal.com/v1", alias="CALCOM_API_URL")
    calcom_event_type_id: int = Field(default=0, alias="CALCOM_EVENT_TYPE_ID")
    calcom_webhook_secret: str = Field(default="", alias="CALCOM_WEBHOOK_SECRET")

    # JWT
    jwt_secret_key: str = Field(..., alias="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = Field(default=7, alias="REFRESH_TOKEN_EXPIRE_DAYS")

    # Feature Flags
    feature_sms_enabled: bool = Field(default=True, alias="FEATURE_SMS_ENABLED")
    feature_email_enabled: bool = Field(default=True, alias="FEATURE_EMAIL_ENABLED")
    feature_vk_enabled: bool = Field(default=True, alias="FEATURE_VK_ENABLED")
    feature_telegram_enabled: bool = Field(default=True, alias="FEATURE_TELEGRAM_ENABLED")
    feature_whatsapp_enabled: bool = Field(default=False, alias="FEATURE_WHATSAPP_ENABLED")
    feature_billing_enabled: bool = Field(default=False, alias="FEATURE_BILLING_ENABLED")
    feature_analytics_enabled: bool = Field(default=True, alias="FEATURE_ANALYTICS_ENABLED")

    # Rate Limiting
    rate_limit_enabled: bool = Field(default=True, alias="RATE_LIMIT_ENABLED")
    rate_limit_per_minute: int = Field(default=100, alias="RATE_LIMIT_PER_MINUTE")

    @property
    def database_url_str(self) -> str:
        """Get database URL as string."""
        return str(self.database_url)

    @property
    def redis_url_str(self) -> str:
        """Get Redis URL as string."""
        return str(self.redis_url)


# Global settings instance
settings = Settings()
