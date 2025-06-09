"""
API v1 endpoints
"""
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
