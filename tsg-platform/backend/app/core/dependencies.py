from fastapi import HTTPException, Depends
from supabase import create_client, Client
from app.core.config import settings

def get_supabase_client() -> Client:
    if not settings.supabase_url or not settings.supabase_key:
        raise HTTPException(status_code=500, detail="Supabase URL or Key not configured")
    return create_client(settings.supabase_url, settings.supabase_key)
