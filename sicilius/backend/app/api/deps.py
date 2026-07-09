"""
Dependencies for FastAPI endpoints
"""
import logging
import secrets
import uuid
from typing import Generator, Optional, TYPE_CHECKING

from fastapi import Depends, HTTPException, status, Request
import logging
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
    Resolve current user via local JWT.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

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


def enforce_daily_limit(
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
) -> None:
    """Kullanıcı başına günlük sorgu limitini uygular ve sayacı arttırır.

    Varsayılan limit 20'dir. ENV ile değiştirilebilir: TSG_DAILY_QUERY_LIMIT
    Aşıldığında 429 döner.
    """
    # Sayfalama aramalarında limiti düşürme (cursor > 0)
    cursor = request.query_params.get("cursor", "0")
    if cursor != "0":
        return

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
        try:
            db.commit()
            db.refresh(usage)
        except:
            # Race condition: another request created the record
            db.rollback()
            usage = (
                db.query(models.DailyUsage)
                .filter(models.DailyUsage.user_id == current_user.id, models.DailyUsage.day == today)
                .first()
            )

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
    try:
        db.commit()
    except Exception as e:
        # DB failure during limit update shouldn't block the request, 
        # but we should log it.
        logging.error(f"Failed to update daily usage: {e}")
        db.rollback()
