"""
TSG Araştırma Platformu - API v1 Router
"""
from fastapi import APIRouter

from app.api.api_v1.endpoints import (
    auth,
    users,
    companies,
    gazettes,
    persons,
    file_uploads,
    jobs,
    utils,
    parsing
)
from app.api.v1.endpoints import company_scrape

api_router = APIRouter()

# Auth endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# User endpoints
api_router.include_router(users.router, prefix="/users", tags=["Users"])

# Company endpoints
api_router.include_router(companies.router, prefix="/companies", tags=["Companies"])

# Gazette endpoints
api_router.include_router(gazettes.router, prefix="/gazettes", tags=["Gazettes"])

# Person endpoints
api_router.include_router(persons.router, prefix="/persons", tags=["Persons"])

# File upload endpoints
api_router.include_router(file_uploads.router, prefix="/file-uploads", tags=["File Uploads"])

# Company scrape endpoints
api_router.include_router(company_scrape.router, prefix="/company-scrapes", tags=["Company Scrapes"])

# Job endpoints
api_router.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])

# Utility endpoints
api_router.include_router(utils.router, prefix="/utils", tags=["Utilities"])

# Parsing endpoints
api_router.include_router(parsing.router, prefix="/parsing", tags=["Parsing"])
