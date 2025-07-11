import os
from functools import lru_cache
from pathlib import Path
from typing import List, Optional, Set

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl, Field, RedisDsn, PostgresDsn, field_validator, ValidationInfo

class Settings(BaseSettings):
    # Pydantic v2 config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix='tsg_',
        case_sensitive=False
    )
    
    # API Settings
    API_V1_STR: str = "/api/v1"
    
    # Project Paths
    PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent.parent

    # App Settings
    APP_NAME: str = "TSG Platform"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 5001
    CORS_ORIGINS: str
    
    # Database (SQLAlchemy connection)
    DATABASE_URL: PostgresDsn

    # Supabase Client
    supabase_url: str
    supabase_key: str

    # Geocoding Services
    locationiq_token: str



    TEST_DATABASE_URL: str = "sqlite:///./test_tsg_platform.db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    SECURE_COOKIE: Optional[bool] = None

    @field_validator('SECURE_COOKIE', mode='before')
    @classmethod
    def assemble_secure_cookie(cls, v: Optional[bool], info: ValidationInfo) -> bool:
        if isinstance(v, bool):
            return v
        # Set secure cookies only in production
        return info.data.get("ENVIRONMENT", "development").lower() == "production"
    
    # File Uploads
    UPLOAD_FOLDER: str = "./data/uploads"
    MAX_CONTENT_LENGTH: int = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS: str
    
    # OCR
    TESSERACT_CMD: str = "/usr/bin/tesseract"
    TESSDATA_PREFIX: str = "/usr/share/tesseract-ocr/4.00/tessdata/"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/tsg_platform.log"
    
    # Redis
    REDIS_URL: RedisDsn = "redis://localhost:6379/0"
    
    # Background Tasks
    BACKGROUND_TASKS_MAX_WORKERS: int = Field(
        default=10,
        description="Maximum number of background worker threads"
    )
    JOB_TIMEOUT_SECONDS: int = Field(
        default=3600,  # 1 hour
        description="Maximum time (in seconds) a job can run before being considered stuck"
    )
    STUCK_JOB_CHECK_INTERVAL: int = Field(
        default=300,  # 5 minutes
        description="How often to check for stuck jobs (in seconds)"
    )
    JOB_STUCK_AFTER_SECONDS: int = Field(
        default=1800,  # 30 minutes
        description="How old a job must be (in seconds) to be considered stuck"
    )
    MAX_JOB_RETRIES: int = Field(
        default=3,
        description="Maximum number of retries for failed jobs"
    )
    AUTO_RETRY_FAILED_JOBS: bool = Field(
        default=True,
        description="Whether to automatically retry failed jobs"
    )
    COMPLETED_JOB_RETENTION_DAYS: int = Field(
        default=30,
        description="Number of days to keep completed job records"
    )
    FAILED_JOB_RETENTION_DAYS: int = Field(
        default=90,
        description="Number of days to keep failed job records"
    )
    

@lru_cache()
def get_settings() -> Settings:
    return Settings()


# Settings instance
settings = get_settings()

# Task settings (import from task_config to avoid circular imports)
try:
    from .task_config import task_settings
except ImportError:
    # If task_config.py doesn't exist yet, create a dummy settings object
    from pydantic import BaseModel
    
    class DummySettings(BaseModel):
        pass
    
    task_settings = DummySettings()
