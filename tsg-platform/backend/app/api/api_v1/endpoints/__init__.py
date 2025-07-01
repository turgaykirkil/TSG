"""
API v1 endpoints
"""
from app.api.v1.endpoints import company_scrape
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(company_scrape.router, prefix="/company-scrapes", tags=["company-scrapes"])

from app.api.api_v1.endpoints import (
    auth,
    users,
    companies,
    gazettes,
    persons,
    file_uploads,
    jobs,
    utils
)

__all__ = [
    "auth",
    "users",
    "companies",
    "gazettes",
    "persons",
    "file_uploads",
    "jobs",
    "utils"
]
