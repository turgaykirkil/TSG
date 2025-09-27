"""
Dependencies for FastAPI endpoints
"""
import logging
from typing import Generator, Optional

from fastapi import Depends, HTTPException, status, Request
from datetime import datetime
import os
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError, DBAPIError

from app import crud, models, schemas
from app.core import security
from app.core.config import settings
from app.db.session import SessionLocal
from supabase import Client, create_client, ClientOptions

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login", auto_error=False
)

async def cookie_or_header_scheme(request: Request, token: Optional[str] = Depends(reusable_oauth2)) -> Optional[str]:
    if token:
        return token
    return request.cookies.get("auth_token")

def get_db() -> Generator:
    """
    Get a database session.
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        try:
            db.close()
        except (OperationalError, DBAPIError):
            # Connection might already be closed by the server (e.g., Supabase idle timeout)
            # Suppress to avoid noisy shutdown tracebacks
            pass

def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(cookie_or_header_scheme)
) -> models.User:
    """
    Get the current user from the token.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Avoid noisy logs and leaking token content; keep as DEBUG with minimal info
    logging.debug("[deps.py] Resolving current user from token (masked)")
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
        logging.debug("[deps.py] Token payload decoded successfully")
    except (jwt.JWTError, ValidationError) as e:
        logging.error(f"[deps.py] Token validation failed. Error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    user = crud.user.get(db, id=token_data.sub)
    if not user:
        logging.warning(f"[deps.py] User with ID {token_data.sub} not found in database.")
        raise HTTPException(status_code=404, detail="User not found")

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    logging.debug(f"[deps.py] User {user.email} found and is active.")
    return user

def get_current_active_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    """
    Get the current user and check if they are a superuser.
    """
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user

def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    """
    Get the current user and check if they are active.
    """
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_supabase_client() -> Generator[Client, None, None]:
    """
    Get a Supabase client.
    """
    try:
        if not settings.supabase_url or not settings.supabase_service_role_key:
            raise ValueError("Supabase URL or Service Role Key not configured")

        opts: ClientOptions = ClientOptions(
            postgrest_client_timeout=60.0,
        )
        supabase_client = create_client(settings.supabase_url, settings.supabase_service_role_key, options=opts)
        yield supabase_client
    except Exception as e:
        logging.error(f"Failed to create Supabase client: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not connect to Supabase service."
        )


def enforce_daily_limit(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
) -> None:
    """Kullanıcı başına günlük sorgu limitini uygular ve sayacı arttırır.

    Varsayılan limit 20'dir. ENV ile değiştirilebilir: TSG_DAILY_QUERY_LIMIT
    Aşıldığında 429 döner.
    """
    # Öncelik: ENV > settings
    limit_env = os.getenv("TSG_DAILY_QUERY_LIMIT")
    if limit_env is not None:
        try:
            limit = int(limit_env)
        except Exception:
            limit = settings.daily_query_limit
    else:
        limit = settings.daily_query_limit

    today = datetime.utcnow().date()
    # Günlük kayıt mevcut mu kontrol et
    usage = (
        db.query(models.DailyUsage)
        .filter(models.DailyUsage.user_id == current_user.id, models.DailyUsage.day == today)
        .first()
    )
    if usage is None:
        usage = models.DailyUsage(user_id=current_user.id, day=today, count=0)
        db.add(usage)
        db.commit()
        db.refresh(usage)

    # Süper kullanıcılar için limit uygulanmaz (sınırsız), fakat sayaç artmaya devam eder
    is_admin = crud.user.is_superuser(current_user)

    if usage.count >= limit and not is_admin:
        raise HTTPException(
            status_code=429,
            detail=f"Günlük sorgu limitine ulaştınız ({limit}). Lütfen yarın tekrar deneyin.",
            headers={"Retry-After": "86400"},
        )

    usage.count += 1
    db.add(usage)
    db.commit()
