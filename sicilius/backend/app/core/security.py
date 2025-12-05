from datetime import datetime, timedelta
from typing import Optional, Any, Union

import logging
from jose import jwt
import bcrypt

logger = logging.getLogger(__name__)
from pydantic import ValidationError

from app.core.config import settings

def create_access_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """JWT access token oluşturur.
    
    Args:
        subject: Token'da saklanacak veri (genellikle kullanıcı ID'si)
        expires_delta: Token süresini belirler, None ise ayarlardan alınır
        
    Returns:
        str: JWT token
    """
    now = datetime.utcnow()
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {"exp": expire, "sub": str(subject), "iat": int(now.timestamp())}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt

def _to_bytes(value: Union[str, bytes]) -> bytes:
    if isinstance(value, bytes):
        return value
    return value.encode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Şifre doğrulama."""
    if not hashed_password:
        return False
    try:
        return bool(bcrypt.checkpw(_to_bytes(plain_password), _to_bytes(hashed_password)))
    except ValueError as exc:
        logger.error(
            "bcrypt hash doğrulanamadı. Hash formatı bozuk olabilir: %s", exc
        )
        return False
    except Exception as exc:
        logger.error("Parola doğrulanırken beklenmedik bir hata oluştu: %s", exc)
        return False

def get_password_hash(password: str) -> str:
    """Şifre hash'leme."""
    try:
        return bcrypt.hashpw(_to_bytes(password), bcrypt.gensalt()).decode()
    except Exception as exc:
        logger.error("Parola hash'lenirken beklenmedik bir hata oluştu: %s", exc)
        raise

def verify_token(token: str) -> Optional[dict]:
    """JWT token doğrulama.
    
    Args:
        token: Doğrulanacak JWT token
        
    Returns:
        Optional[dict]: Token geçerliyse içeriği, değilse None
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except (jwt.JWTError, ValidationError):
        return None

def create_password_reset_token(email: str) -> str:
    """Şifre sıfırlama token'ı oluşturur.
    
    Args:
        email: Kullanıcı e-posta adresi
        
    Returns:
        str: JWT token
    """
    expires = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    return create_access_token(subject=email, expires_delta=expires)

def verify_password_reset_token(token: str) -> Optional[str]:
    """Şifre sıfırlama token'ını doğrular.
    
    Args:
        token: Doğrulanacak JWT token
        
    Returns:
        Optional[str]: Token geçerliyse e-posta adresi, değilse None
    """
    try:
        decoded_token = verify_token(token)
        if not decoded_token:
            return None
        return decoded_token.get("sub")
    except Exception:
        return None
