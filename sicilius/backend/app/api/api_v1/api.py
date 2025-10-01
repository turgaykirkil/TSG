"""
TSG Araştırma Platformu - API v1 Router
"""
from fastapi import APIRouter
import logging
from app.core.config import settings

from app.api.api_v1.endpoints import (
    auth,
    users,
    announcements,
    companies,
    gazettes,
    persons,
    file_uploads,
    jobs,
    search,
    stats,
    storage,
    tools,
    processing,
    utils,
    usage,
    settings as settings_ep,
)

api_router = APIRouter()
logger = logging.getLogger(__name__)

# Core
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])

# Data Models
api_router.include_router(announcements.router, prefix="/announcements", tags=["Announcements"])
api_router.include_router(companies.router, prefix="/companies", tags=["Companies"])
api_router.include_router(gazettes.router, prefix="/gazettes", tags=["Gazettes"])
api_router.include_router(persons.router, prefix="/persons", tags=["Persons"])

# Functionality
# OCR/Parsing endpointleri yalnızca API_ONLY=False iken dahil edilir (ör. local geliştirme).
if not getattr(settings, "API_ONLY", False):
    from app.api.api_v1.endpoints import ocr, parsing  # type: ignore
    api_router.include_router(ocr.router, prefix="/parsing", tags=["OCR & Parsing"])
    api_router.include_router(parsing.router, prefix="/parsing", tags=["Parsing"])

# Scraping endpointleri de ağır bağımlılıklar içerir (Playwright). API_ONLY=True iken dahil etmeyelim.
if not getattr(settings, "API_ONLY", False):
    from app.api.api_v1.endpoints import scraping  # type: ignore
    api_router.include_router(scraping.router, prefix="/scraping", tags=["Scraping"])
api_router.include_router(search.router, prefix="/search", tags=["Search"])
api_router.include_router(processing.router, prefix="/process", tags=["Processing"])

# File & Job Handling
api_router.include_router(file_uploads.router, prefix="/files", tags=["File Handling"])
api_router.include_router(storage.router, prefix="/storage", tags=["Storage"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])

# NLP sadece API_ONLY=False iken dahil edilir (spacy gibi ağır bağımlılıklar nedeniyle)
if not getattr(settings, "API_ONLY", False):
    from app.api.api_v1.endpoints import nlp  # type: ignore
    api_router.include_router(nlp.router, prefix="/nlp", tags=["NLP"])

# Supporting
api_router.include_router(stats.router, prefix="/stats", tags=["Statistics"])
api_router.include_router(tools.router, prefix="/tools", tags=["Tools"])
api_router.include_router(utils.router, prefix="/utils", tags=["Utilities"])
api_router.include_router(usage.router, prefix="/usage", tags=["Usage"])
api_router.include_router(settings_ep.router, prefix="/settings", tags=["Settings"])
