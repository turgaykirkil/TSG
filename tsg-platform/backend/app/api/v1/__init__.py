"""
TSG Araştırma Platformu - API v1
"""

from fastapi import APIRouter
from .endpoints import router as endpoints_router

api_router = APIRouter()
api_router.include_router(endpoints_router, prefix="/v1")
