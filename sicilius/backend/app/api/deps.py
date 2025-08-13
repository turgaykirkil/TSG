"""
Dependencies for FastAPI endpoints
"""
import logging
from typing import Generator, Optional

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

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
        db.close()

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
    logging.info(f"[deps.py] Attempting to get current user with token: {token[:10]}...")
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
        logging.info(f"[deps.py] Token payload decoded successfully: {token_data}")
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

    logging.info(f"[deps.py] User {user.email} found and is active.")
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
