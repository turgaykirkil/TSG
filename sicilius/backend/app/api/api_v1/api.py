"""
TSG Araştırma Platformu - API v1 Router
"""
from fastapi import APIRouter
import logging

from app.api.api_v1.endpoints import (
    auth,
    users,
    announcements,
    companies,
    gazettes,
    persons,
    file_uploads,
    jobs,
    ocr,
    scraping,
    search,
    stats,
    storage,
    tools,
    processing,
    utils
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
api_router.include_router(ocr.router, prefix="/parsing", tags=["OCR & Parsing"])
api_router.include_router(scraping.router, prefix="/scraping", tags=["Scraping"])
api_router.include_router(search.router, prefix="/search", tags=["Search"])
api_router.include_router(processing.router, prefix="/process", tags=["Processing"])

# File & Job Handling
api_router.include_router(file_uploads.router, prefix="/files", tags=["File Handling"])
api_router.include_router(storage.router, prefix="/storage", tags=["Storage"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])

# Supporting
api_router.include_router(stats.router, prefix="/stats", tags=["Statistics"])
api_router.include_router(tools.router, prefix="/tools", tags=["Tools"])
api_router.include_router(utils.router, prefix="/utils", tags=["Utilities"])
