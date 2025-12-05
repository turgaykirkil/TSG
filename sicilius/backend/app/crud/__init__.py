"""
CRUD (Create, Read, Update, Delete) operations for the application.
"""

# Base CRUD class
from .base import CRUDBase

# User CRUD operations
from .crud_user import user

# Company CRUD operations
from .crud_company import company

# Gazette CRUD operations
from .crud_gazette import gazette

# Gazette Entry CRUD operations
from .crud_gazette_entry import gazette_entry

# Person CRUD operations
from .crud_person import person

# Company-Person Relation CRUD operations
from .crud_relation import company_person_relation

# File Upload CRUD operations
from .crud_file_upload import file_upload

# Job History CRUD operations
from .crud_job_history import job_history

# Announcement CRUD operations
from .crud_announcement import announcement

# Company Error CRUD operations
from .crud_company_error import company_error

# Company Scrape CRUD operations


__all__ = [
    # Base
    "CRUDBase",
    
    # Models
    "user",
    "company",
    "gazette",
    "gazette_entry",
    "person",
    "company_person_relation",
    "file_upload",
    "job_history",
    "company_scrape",
    "announcement",
    "company_error",
]
