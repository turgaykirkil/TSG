from supabase import create_client, Client
from app.core.config import settings

# Use the centralized settings object to get Supabase credentials
# Pydantic v2 returns AnyHttpUrl, which needs to be cast to a string.
url: str = settings.supabase_url
# Use the service role key for backend operations that require admin privileges
key: str = settings.supabase_service_role_key

# Ensure that the environment variables are loaded before creating the client
if not url or not key:
    raise ValueError("Supabase URL and/or Key not found in settings. Please check your .env file and config.py.")

supabase: Client = create_client(url, key)
