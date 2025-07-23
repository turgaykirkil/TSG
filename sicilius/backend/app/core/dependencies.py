from fastapi import HTTPException, Depends
from supabase import create_client, Client, ClientOptions
from app.core.config import settings
from app.db.session import SessionLocal

def get_supabase_client() -> Client:
    if not settings.supabase_url or not settings.supabase_key:
        raise HTTPException(status_code=500, detail="Supabase URL or Key not configured")
    
    # Increase the timeout to 60 seconds to handle large file uploads
    opts: ClientOptions = ClientOptions(
        postgrest_client_timeout=60.0,
    )

    return create_client(settings.supabase_url, settings.supabase_key, options=opts)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
