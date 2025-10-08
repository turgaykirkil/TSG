from datetime import datetime, timedelta
from typing import Optional, Any, Union

import logging
from jose import jwt
from passlib.context import CryptContext
from passlib.exc import UnknownHashError

logger = logging.getLogger(__name__)
from pydantic import ValidationError

from app.core.config import settings

# Password hashing
# Note: bcrypt has a 72-byte password limit. To avoid runtime errors during
# verification, configure passlib to silently truncate inputs beyond 72 bytes.
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__truncate_error=False,
)

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

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Şifre doğrulama.
    
    Args:
        plain_password: Düz metin şifre
        hashed_password: Hash'lenmiş şifre
        
    Returns:
        bool: Şifre doğru ise True, değilse False
    """
    logger.info(f"Parola doğrulanıyor. DB'den gelen hash'in başlangıcı: {hashed_password[:10] if hashed_password else 'Yok'}")
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except UnknownHashError:
        logger.error(
            f"!!! HASH FORMATI TANINAMADI !!! Veritabanındaki parola (hashed_password) "
            f"beklenen 'bcrypt' formatında değil. Lütfen kullanıcının parolasını sıfırlayın. "
            f"Mevcut hash: '{hashed_password}'"
        )
        return False
    except Exception as e:
        logger.error(f"Parola doğrulanırken beklenmedik bir hata oluştu: {e}")
        return False

def get_password_hash(password: str) -> str:
    """Şifre hash'leme.
    
    Args:
        password: Hash'lenecek düz metin şifre
        
    Returns:
        str: Hash'lenmiş şifre
    """
    return pwd_context.hash(password)

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
