"""
TSG Araştırma Platformu - API v1 Router
"""
from fastapi import APIRouter
import logging
import os
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
    incoming_emails,
    cloudflare_webhook,
    company_errors,
    contact_messages,
    nexus,
    operations,
    admin,
    worker_node,
    b2b_customers,
    tasks,
    gamification,
)

api_router = APIRouter()
logger = logging.getLogger(__name__)

# Core
api_router.include_router(admin.router, prefix="/admin", tags=["Admin DB Control"])

# Ortam bayrakları ile modüler include kontrolü
INCLUDE_NLP = os.getenv("INCLUDE_NLP", "true").lower() == "true"
INCLUDE_SCRAPING = os.getenv("INCLUDE_SCRAPING", "true").lower() == "true"
INCLUDE_OCR = os.getenv("INCLUDE_OCR", "true").lower() == "true"
INCLUDE_PARSING = os.getenv("INCLUDE_PARSING", "true").lower() == "true"

# Core
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])

# Data Models
api_router.include_router(announcements.router, prefix="/announcements", tags=["Announcements"])
api_router.include_router(companies.router, prefix="/companies", tags=["Companies"])
api_router.include_router(gazettes.router, prefix="/gazettes", tags=["Gazettes"])
api_router.include_router(persons.router, prefix="/persons", tags=["Persons"])
api_router.include_router(company_errors.router, prefix="/errors", tags=["Company Errors"])
api_router.include_router(contact_messages.router, prefix="/contact", tags=["Contact Messages"])
api_router.include_router(nexus.router, prefix="/nexus", tags=["NEXUS Risk Engine"])
api_router.include_router(b2b_customers.router, prefix="/b2b-customers", tags=["B2B Customers"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
api_router.include_router(gamification.router, prefix="/gamification", tags=["Gamification Engine"])

# Functionality
# OCR/Parsing endpointleri yalnızca API_ONLY=False iken ve ilgili bayraklar true ise dahil edilir
if not getattr(settings, "API_ONLY", False):
    if INCLUDE_OCR:
        from app.api.api_v1.endpoints import ocr  # type: ignore
        api_router.include_router(ocr.router, prefix="/ocr", tags=["OCR & Parsing"])
    if INCLUDE_PARSING:
        from app.api.api_v1.endpoints import parsing  # type: ignore
        api_router.include_router(parsing.router, prefix="/parsing", tags=["Parsing"])

# Scraping endpointleri de ağır bağımlılıklar içerir (Playwright). API_ONLY=True iken dahil etmeyelim.
if not getattr(settings, "API_ONLY", False):
    if INCLUDE_SCRAPING:
        from app.api.api_v1.endpoints import scraping  # type: ignore
        api_router.include_router(scraping.router, prefix="/scraping", tags=["Scraping"])
api_router.include_router(search.router, prefix="/search", tags=["Search"])
api_router.include_router(processing.router, prefix="/process", tags=["Processing"])
api_router.include_router(processing.router, prefix="/processing", tags=["Processing"])
api_router.include_router(worker_node.router, prefix="/worker-node", tags=["Worker Node (Distributed)"])

# File & Job Handling
api_router.include_router(file_uploads.router, prefix="/files", tags=["File Handling"])
api_router.include_router(storage.router, prefix="/storage", tags=["Storage"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])

# NLP yalnızca API_ONLY=False iken ve INCLUDE_NLP=true ise dahil edilir (spacy gibi ağır bağımlılıklar nedeniyle)
if not getattr(settings, "API_ONLY", False):
    if INCLUDE_NLP:
        from app.api.api_v1.endpoints import nlp  # type: ignore
        api_router.include_router(nlp.router, prefix="/nlp", tags=["NLP"])

# Supporting
api_router.include_router(stats.router, prefix="/stats", tags=["Statistics"])
api_router.include_router(tools.router, prefix="/tools", tags=["Tools"])
api_router.include_router(utils.router, prefix="/utils", tags=["Utilities"])
api_router.include_router(usage.router, prefix="/usage", tags=["Usage"])
api_router.include_router(settings_ep.router, prefix="/settings", tags=["Settings"])
api_router.include_router(operations.router, prefix="/operations", tags=["Operations Center"])

# Email System (Admin inbox + Cloudflare webhook)
api_router.include_router(incoming_emails.router, tags=["Incoming Emails"])
api_router.include_router(cloudflare_webhook.router, tags=["Webhooks"])
