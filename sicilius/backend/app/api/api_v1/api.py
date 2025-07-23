"""
TSG Araştırma Platformu - API v1 Router
"""
from fastapi import APIRouter

from app.api.api_v1.endpoints import (
    auth,
    users,
    batch_ocr,
    announcements,
    companies,
    gazettes,
    persons,
    file_uploads,
    jobs,
    utils,
    parsing,
    scraping,
    search,
    stats,
    tools,
    processing,
    ocr,
    announcements
)


api_router = APIRouter()

# Auth endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# User endpoints
api_router.include_router(users.router, prefix="/users", tags=["Users"])

# Announcement endpoints
api_router.include_router(announcements.router, prefix="/announcements", tags=["Announcements"])

# Company endpoints
api_router.include_router(companies.router, prefix="/companies", tags=["Companies"])

# Gazette endpoints
api_router.include_router(gazettes.router, prefix="/gazettes", tags=["Gazettes"])

# Person endpoints
api_router.include_router(persons.router, prefix="/persons", tags=["Persons"])

# File upload endpoints
api_router.include_router(file_uploads.router, prefix="/file-uploads", tags=["File Uploads"])

# Company scrape endpoints


# Job endpoints
api_router.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])

# Utility endpoints
api_router.include_router(utils.router, prefix="/utils", tags=["Utilities"])

# Stats endpoints
api_router.include_router(stats.router, prefix="/stats", tags=["Stats"])



# Parsing endpoints
api_router.include_router(parsing.router, prefix="/parsing", tags=["Parsing"])
api_router.include_router(ocr.router, prefix="/ocr", tags=["OCR"])
api_router.include_router(batch_ocr.router, prefix="/batch_ocr", tags=["Batch OCR"])


# Scraping endpoints
api_router.include_router(scraping.router, prefix="/scraping", tags=["Scraping"])

# Search endpoints
api_router.include_router(search.router, prefix="/search", tags=["Search"])

# Stats endpoints


# Tools endpoints
api_router.include_router(tools.router, prefix="/tools", tags=["Tools"])

# Processing endpoints
api_router.include_router(processing.router, prefix="/process", tags=["Processing"])
