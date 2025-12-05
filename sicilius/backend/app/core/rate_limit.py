"""
Rate limiting utility using slowapi
"""
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Create limiter instance
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])

__all__ = ["limiter", "RateLimitExceeded", "_rate_limit_exceeded_handler"]
