import os
from functools import lru_cache
from pathlib import Path
from typing import List, Optional, Set

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl, Field, PostgresDsn, RedisDsn, ValidationInfo, field_validator

class Settings(BaseSettings):
    # Pydantic v2 config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix='tsg_',
        case_sensitive=False,
        extra='ignore',
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
    # Auth mode: 'local' (legacy DB users) or 'supabase' (Supabase Auth JWT)
    auth_mode: str = "local"
    # API-only mode (disable heavy OCR endpoints in prod containers)
    API_ONLY: bool = False
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 5001
    CORS_ORIGINS: List[AnyHttpUrl] = []
    
    # Database (SQLAlchemy connection)
    DATABASE_URL: PostgresDsn

    # Supabase Client (optional in local auth mode)
    supabase_url: Optional[str] = None
    supabase_key: Optional[str] = None  # Public anon key
    supabase_service_role_key: Optional[str] = None  # Service role key for admin operations
    # Supabase JWT secret for verifying access tokens locally (HS256). Optional fallback to auth.get_user if absent.
    supabase_jwt_secret: Optional[str] = None

    # MinIO / S3-compatible object storage
    MINIO_ENDPOINT: str = "minio:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "ChangeMe_12345"
    MINIO_SECURE: bool = False
    minio_region: Optional[str] = None
    minio_bucket_gazette_pdfs: str = "gazette-pdfs"
    minio_bucket_company_gazettes: str = "company-gazettes"

    # Firebase (optional)
    # Service account JSON dosya yolu (mutlaka local path, repo'ya girmemeli)
    firebase_service_account_path: Optional[str] = None
    # Firebase Project ID (örn. tsg-platform-13d58)
    firebase_project_id: Optional[str] = None
    # Storage bucket adı (örn. tsg-platform-13d58.appspot.com). İlk fazda opsiyonel/kapalı.
    firebase_storage_bucket: Optional[str] = None
    # Firebase Hosting site ID (örn. tsg-platform)
    firebase_hosting_site: Optional[str] = None
    # Storage kullanım bayrağı (ilk fazda False)
    firebase_enable_storage: bool = False

    # Geocoding Services
    locationiq_token: Optional[str] = None
    
    # Cloudflare Email Routing Webhook
    CLOUDFLARE_WEBHOOK_SECRET: Optional[str] = None  # Optional HMAC secret for webhook validation
    
    # Contact Form
    CONTACT_EMAIL: str = "info@sicilius.com.tr"  # Email to receive contact form submissions



    TEST_DATABASE_URL: str = "sqlite:///./test_tsg_platform.db"
    
    # Security
    SECRET_KEY: str  # REQUIRED - Must be set via TSG_SECRET_KEY environment variable
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10  # 10 minutes for regular users
    ADMIN_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours for admin users
    SECURE_COOKIE: Optional[bool] = None
    # Optional cookie domain to share auth cookie across subdomains (e.g. .sicilius.com.tr)
    COOKIE_DOMAIN: Optional[str] = None

    @field_validator('COOKIE_DOMAIN', mode='before')
    @classmethod
    def assemble_cookie_domain(cls, v: Optional[str], info: ValidationInfo) -> Optional[str]:
        if isinstance(v, str):
            return v
        # In production, share cookie across subdomains
        if info.data.get("ENVIRONMENT", "development").lower() == "production":
            return ".sicilius.com.tr"
        return None

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
    ALLOWED_EXTENSIONS: str = "pdf,png,jpg,jpeg,gif"
    
    # OCR
    TESSERACT_CMD: str = "/usr/bin/tesseract"
    TESSDATA_PREFIX: str = "/usr/share/tesseract-ocr/4.00/tessdata/"

    # Scraping
    HEADLESS: bool = False

    # Sicil login credentials (provide via environment)
    SICIL_EMAIL: str = ""
    SICIL_PASSWORD: str = ""
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/tsg_platform.log"

    # Sentry (optional)
    sentry_dsn: Optional[str] = None
    sentry_traces_sample_rate: float = 0.0
    sentry_env: Optional[str] = None
    sentry_release: Optional[str] = None

    # Redis (Port 6380 via SSH Tunnel to Remote Server)
    REDIS_URL: RedisDsn = "redis://localhost:6380/0"

    # Search (backend performance & security)
    # Not: .env içinde anahtarlar 'tsg_search_max_companies' gibi prefix'li ya da prefix'siz olabilir.
    # extra='ignore' sayesinde fazladan anahtarlar sorun yaratmaz.
    search_max_companies: int = 20
    search_cache_ttl_seconds: int = 30
    search_rate_limit_rpm: int = 0
    # Query limits
    daily_query_limit: int = 20
    
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
