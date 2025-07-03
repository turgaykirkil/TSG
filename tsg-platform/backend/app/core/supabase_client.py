from supabase import create_client, Client
from app.core.config import settings

# Use the centralized settings object to get Supabase credentials
# Pydantic v2 returns AnyHttpUrl, which needs to be cast to a string.
url: str = str(settings.SUPABASE_URL) if settings.SUPABASE_URL else None
key: str = settings.SUPABASE_KEY

# Ensure that the environment variables are loaded before creating the client
if not url or not key:
    raise ValueError("Supabase URL and/or Key not found in settings. Please check your .env file and config.py.")

supabase: Client = create_client(url, key)
