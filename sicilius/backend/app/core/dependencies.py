from fastapi import HTTPException

from app.db.session import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_supabase_client():
    """Supabase entegrasyonu devre dışı bırakılmıştır."""
    raise HTTPException(status_code=503, detail="Supabase integration disabled")
