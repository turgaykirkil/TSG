from pydantic import BaseModel, Field, EmailStr, AnyUrl
from typing import Literal, Optional, List

SecureType = Literal["starttls", "ssl"]

class EmailSettings(BaseModel):
    host: str = Field(..., min_length=1)
    port: int = Field(..., ge=1, le=65535)
    secure: SecureType = Field(default="starttls")
    username: str = Field(..., min_length=1)
    password: Optional[str] = Field(default=None, description="Leave empty to keep current password")
    from_name: str = Field(default="Sicilius")
    from_email: EmailStr
    reset_url_base: str = Field(..., min_length=1)
    invite_url_base: Optional[str] = Field(default=None, description="Base URL for invite completion link")

class EmailSettingsOut(BaseModel):
    host: str
    port: int
    secure: SecureType
    username: str
    from_name: str
    from_email: EmailStr
    reset_url_base: str
    invite_url_base: Optional[str] = None
    # do not expose password

RegistrationMode = Literal["open", "invite_only"]
UserRole = Literal["admin", "manager", "user"]

class UserSettings(BaseModel):
    registration_mode: RegistrationMode = Field(default="invite_only")
    allowed_email_domains: List[str] = Field(default_factory=list)
    blocked_email_domains: List[str] = Field(default_factory=list)
    default_user_role: UserRole = Field(default="user")
    invite_enabled: bool = True
    invite_token_ttl_hours: int = Field(default=72, ge=1, le=24*30)
    monthly_invite_limit_per_user: int = Field(default=1, ge=0, le=100, description="Monthly invite limit for regular users")
    monthly_invite_limit_per_admin: int = Field(default=999999, ge=0, le=999999, description="Monthly invite limit for admins (effectively unlimited)")
    daily_query_limit: int = Field(default=20, ge=0, le=10000)

class UserSettingsOut(UserSettings):
    pass

class SecuritySettings(BaseModel):
    session_expire_minutes: int = Field(default=1440, ge=5, le=60*24*30)
    remember_me_days: int = Field(default=7, ge=0, le=365)
    login_rate_limit_per_minute: int = Field(default=20, ge=0, le=1000)
    lockout_threshold: int = Field(default=10, ge=0, le=100)
    lockout_window_minutes: int = Field(default=15, ge=1, le=24*60)
    password_min_length: int = Field(default=8, ge=4, le=128)
    password_require_upper: bool = True
    password_require_number: bool = True
    password_require_symbol: bool = True
    password_history_disallow: int = Field(default=0, ge=0, le=24)
    password_validity_days: int = Field(default=0, ge=0, le=365)
    mfa_required_for_admins: bool = True
    mfa_enabled: bool = False

class SecuritySettingsOut(SecuritySettings):
    pass


SSOProvider = Literal["saml", "oidc"]

class SSOSettings(BaseModel):
    enabled: bool = False
    provider: Optional[SSOProvider] = None
    issuer: Optional[str] = None
    discovery_url: Optional[AnyUrl] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = Field(default=None, description="Leave empty to keep current secret")
    callback_url: Optional[AnyUrl] = None
    jit_provisioning: bool = True

class SSOSettingsOut(BaseModel):
    enabled: bool = False
    provider: Optional[SSOProvider] = None
    issuer: Optional[str] = None
    discovery_url: Optional[AnyUrl] = None
    client_id: Optional[str] = None
    callback_url: Optional[AnyUrl] = None
    jit_provisioning: bool = True


class NotificationSettings(BaseModel):
    email_on_password_change: bool = True
    email_on_new_login: bool = True

class NotificationSettingsOut(NotificationSettings):
    pass


class PrivacySettings(BaseModel):
    account_delete_grace_days: int = Field(default=7, ge=0, le=365)
    data_export_enabled: bool = True
    audit_log_retention_days: int = Field(default=90, ge=1, le=3650)

class PrivacySettingsOut(PrivacySettings):
    pass


class IntegrationSettings(BaseModel):
    sentry_dsn: Optional[str] = None
    locationiq_token: Optional[str] = None
    webhook_url: Optional[AnyUrl] = None

class IntegrationSettingsOut(IntegrationSettings):
    pass
