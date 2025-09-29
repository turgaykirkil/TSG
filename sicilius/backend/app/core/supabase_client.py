from typing import Optional
from supabase import create_client, Client
from app.core.config import settings

# Use the centralized settings object to get Supabase credentials
# Pydantic v2 returns AnyHttpUrl, which needs to be cast to a string.
url: str = settings.supabase_url
# Use the service role key for backend operations that require admin privileges
key: str = settings.supabase_service_role_key

# Create client lazily/safely at import time. If anything fails, set to None.
supabase: Optional[Client]
try:
    if not url or not key:
        raise ValueError("Supabase URL and/or Key not found in settings. Please check your .env file and config.py.")
    supabase = create_client(url, key)
except Exception:
    # Do not crash app import; endpoints that actually need Supabase will use dependency-based creation.
    supabase = None
