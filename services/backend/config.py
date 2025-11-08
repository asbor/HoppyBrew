"""
Simple Environment Configuration for HoppyBrew
Handles loading and validation of environment variables
"""

import os
from typing import Optional, List
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()


class Settings:
    """Application settings from environment variables"""

    def __init__(self):
        # Security
        self.SECRET_KEY: str = os.getenv(
            "SECRET_KEY", "dev-secret-key-change-in-production-must-be-32-chars-minimum"
        )
        self.ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
        self.ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
            os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
        )

        # Database Configuration
        self.DATABASE_USER: str = os.getenv("DATABASE_USER", "postgres")
        self.DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "postgres")
        self.DATABASE_HOST: str = os.getenv("DATABASE_HOST", "localhost")
        self.DATABASE_PORT: int = int(os.getenv("DATABASE_PORT", "5432"))
        self.DATABASE_NAME: str = os.getenv("DATABASE_NAME", "hoppybrew_db")

        # Test Database
        self.TEST_DATABASE_URL: str = os.getenv(
            "TEST_DATABASE_URL", "sqlite:///:memory:"
        )

        # API Configuration
        self.API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
        self.API_PORT: int = int(os.getenv("API_PORT", "8000"))
        self.API_RELOAD: bool = os.getenv("API_RELOAD", "true").lower() == "true"
        self.API_LOG_LEVEL: str = os.getenv("API_LOG_LEVEL", "info")

        # CORS Configuration
        cors_origins_str = os.getenv(
            "CORS_ORIGINS", "http://localhost:3000,http://localhost:5173"
        )
        self.CORS_ORIGINS: List[str] = [
            origin.strip() for origin in cors_origins_str.split(",")
        ]
        self.CORS_ALLOW_CREDENTIALS: bool = (
            os.getenv("CORS_ALLOW_CREDENTIALS", "true").lower() == "true"
        )
        self.CORS_ALLOW_METHODS: List[str] = ["*"]
        self.CORS_ALLOW_HEADERS: List[str] = ["*"]

        # File Upload Configuration
        self.MAX_UPLOAD_SIZE: int = int(
            os.getenv("MAX_UPLOAD_SIZE", "10485760")
        )  # 10MB
        self.UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./uploads")

        # External APIs
        self.HOMEBREWING_API_KEY: Optional[str] = os.getenv("HOMEBREWING_API_KEY")
        self.WEATHER_API_KEY: Optional[str] = os.getenv("WEATHER_API_KEY")

        # Logging
        self.LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
        self.LOG_FILE: str = os.getenv("LOG_FILE", "./logs/hoppybrew.log")

        # Production Security
        self.PRODUCTION: bool = os.getenv("PRODUCTION", "false").lower() == "true"
        self.SSL_REDIRECT: bool = os.getenv("SSL_REDIRECT", "false").lower() == "true"

        # Email Configuration
        self.SMTP_SERVER: Optional[str] = os.getenv("SMTP_SERVER")
        self.SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
        self.SMTP_USERNAME: Optional[str] = os.getenv("SMTP_USERNAME")
        self.SMTP_PASSWORD: Optional[str] = os.getenv("SMTP_PASSWORD")

        # Redis Configuration
        self.REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

        # Backup Configuration
        self.BACKUP_ENABLED: bool = (
            os.getenv("BACKUP_ENABLED", "false").lower() == "true"
        )
        self.BACKUP_SCHEDULE: str = os.getenv("BACKUP_SCHEDULE", "0 2 * * *")
        self.BACKUP_RETENTION_DAYS: int = int(os.getenv("BACKUP_RETENTION_DAYS", "30"))

        # Validate configuration
        self._validate_settings()

        # Ensure required directories exist
        self.ensure_directories()

    def _validate_settings(self):
        """Validate critical settings"""
        if (
            self.PRODUCTION
            and self.SECRET_KEY
            == "dev-secret-key-change-in-production-must-be-32-chars-minimum"
        ):
            raise ValueError("SECRET_KEY must be changed in production")
        if len(self.SECRET_KEY) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long")

    @property
    def DATABASE_URL(self) -> str:
        """Construct database URL from individual components"""
        if os.getenv("TESTING") == "1":
            return self.TEST_DATABASE_URL
        return f"postgresql+psycopg://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"

    @property
    def is_production(self) -> bool:
        """Check if running in production mode"""
        return self.PRODUCTION

    @property
    def cors_origins_list(self) -> List[str]:
        """Get CORS origins as a list"""
        return self.CORS_ORIGINS

    def ensure_directories(self):
        """Create necessary directories if they don't exist"""
        try:
            Path(self.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
            Path(self.LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"Warning: Could not create directories: {e}")


# Global settings instance
settings = Settings()

# Security warning for development
if (
    not settings.is_production
    and settings.SECRET_KEY
    == "dev-secret-key-change-in-production-must-be-32-chars-minimum"
):
    import warnings

    warnings.warn(
        "Using default SECRET_KEY in development mode. "
        "Change this in .env file for production!",
        UserWarning,
    )
