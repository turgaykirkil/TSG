from fastapi import HTTPException, Depends
from supabase import create_client, Client
from app.core.config import settings

def get_supabase_client() -> Client:
    if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
        raise HTTPException(status_code=500, detail="Supabase URL or Key not configured")
    supabase_url = str(settings.SUPABASE_URL)
    supabase_key = str(settings.SUPABASE_KEY)
    return create_client(supabase_url, supabase_key)
