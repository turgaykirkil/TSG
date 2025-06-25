"""
TSG Araştırma Platformu - API v1 Endpoints
"""

from fastapi import APIRouter
from .company_scrape import router as company_scrape_router
from .parsing import router as parsing_router

router = APIRouter()

# Endpoint'leri router'a ekle
router.include_router(company_scrape_router)
router.include_router(parsing_router)
