"""
TSG Araştırma Platformu - API v1 Endpoints
"""

from fastapi import APIRouter

from .parsing import router as parsing_router

router = APIRouter()

# Endpoint'leri router'a ekle

router.include_router(parsing_router)
