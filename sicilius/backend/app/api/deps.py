"""
Dependencies for FastAPI endpoints
"""
import logging
import secrets
import uuid
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
from supabase import Client, create_client

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

def _ensure_local_user(db: Session, *, user_id_str: str, email: Optional[str]) -> models.User:
    """Ensure a shadow local user row exists for Supabase-authenticated users.
    Creates the row with a random password hash if missing.
    """
    try:
        user_uuid = uuid.UUID(user_id_str)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Supabase user id")

    user = crud.user.get(db, id=user_uuid)
    if user:
        return user

    # Try by email as well to link existing row
    if email:
        by_email = crud.user.get_by_email(db, email=email)
        if by_email:
            # If an existing row has different id, keep existing to avoid PK conflict
            return by_email

    # Create a minimal user row with random password (unused under Supabase auth)
    from app.models.user import User, UserRole
    random_hash = security.get_password_hash(secrets.token_urlsafe(16))
    new_user = User(
        id=user_uuid,
        email=(email or f"user-{user_id_str}@example.com"),
        hashed_password=random_hash,
        full_name=email or None,
        is_active=True,
        role=UserRole.USER,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(cookie_or_header_scheme)
) -> models.User:
    """
    Resolve current user depending on auth mode.
    - local: validate our own JWT and fetch user from DB
    - supabase: validate Supabase JWT (HS256) or fallback to auth.get_user(token),
      then ensure a shadow local user exists and return it
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if getattr(settings, "auth_mode", "local").lower() != "supabase":
        # Legacy local JWT mode
        logging.debug("[deps.py] Resolving current user via local JWT")
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            token_data = schemas.TokenPayload(**payload)
        except (jwt.JWTError, ValidationError) as e:
            logging.error(f"[deps.py] Token validation failed. Error: {e}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
            )

        user = crud.user.get(db, id=token_data.sub)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        return user

    # Supabase Auth mode
    logging.debug("[deps.py] Resolving current user via Supabase JWT")
    supabase_user_id: Optional[str] = None
    supabase_email: Optional[str] = None

    # Prefer local HS256 verify if jwt secret provided (faster, no network)
    if settings.supabase_jwt_secret:
        try:
            payload = jwt.decode(
                token,
                settings.supabase_jwt_secret,
                algorithms=["HS256"],
                options={"verify_aud": False},
            )
            supabase_user_id = payload.get("sub")
            supabase_email = payload.get("email") or (
                (payload.get("user_metadata") or {}).get("email") if isinstance(payload.get("user_metadata"), dict) else None
            )
        except Exception as e:
            logging.warning(f"[deps.py] Local Supabase JWT verify failed, falling back to get_user: {e}")

    if not supabase_user_id:
        try:
            supabase_client = create_client(settings.supabase_url, settings.supabase_key)
            resp = supabase_client.auth.get_user(token)
            if not resp or not getattr(resp, "user", None):
                raise HTTPException(status_code=403, detail="Could not validate Supabase token")
            supabase_user_id = str(resp.user.id)
            supabase_email = getattr(resp.user, "email", None)
        except Exception as e:
            logging.error(f"[deps.py] Supabase auth.get_user failed: {e}", exc_info=True)
            raise HTTPException(status_code=403, detail="Could not validate credentials")

    user = _ensure_local_user(db, user_id_str=supabase_user_id, email=supabase_email)
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
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

        supabase_client = create_client(settings.supabase_url, settings.supabase_service_role_key)
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
