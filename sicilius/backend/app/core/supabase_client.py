from supabase import create_client, Client, ClientOptions
from app.core.config import settings

# Use the centralized settings object to get Supabase credentials
# Pydantic v2 returns AnyHttpUrl, which needs to be cast to a string.
url: str = settings.supabase_url
# Use the service role key for backend operations that require admin privileges
key: str = settings.supabase_service_role_key

# Ensure that the environment variables are loaded before creating the client
if not url or not key:
    raise ValueError("Supabase URL and/or Key not found in settings. Please check your .env file and config.py.")

# Set a longer timeout for storage operations to prevent ConnectTimeout errors.
# The library expects a simple float for the timeout in seconds.
opts: ClientOptions = ClientOptions(
    storage_client_timeout=60.0
)

supabase: Client = create_client(url, key, options=opts)
