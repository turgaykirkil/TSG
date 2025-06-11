"""
TSG Araştırma Platformu - API v1 Endpoints
"""

from fastapi import APIRouter
from . import company_scrape

router = APIRouter()

# Endpoint'leri router'a ekle
router.include_router(company_scrape.router)
