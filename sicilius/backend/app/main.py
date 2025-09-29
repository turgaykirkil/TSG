import logging
import json
import os
import httpx
import base64
import random
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

from fastapi import FastAPI, Request, status, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.api_v1.api import api_router
from app.core.config import settings
from app.db.session import engine, Base
from app import models  # Bütün modelleri Base'e kaydetmek için
from app.api import upload_api

# --- Logging Configuration ---
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Reduce noisy access logs from Uvicorn in development
try:
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
except Exception:
    pass

# --- Sentry Initialization (optional) ---
if settings.sentry_dsn:
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        integrations=[FastApiIntegration(), LoggingIntegration(level=logging.INFO, event_level=logging.ERROR)],
        traces_sample_rate=float(getattr(settings, "sentry_traces_sample_rate", 0.0) or 0.0),
        environment=getattr(settings, "sentry_env", None),
        release=getattr(settings, "sentry_release", None),
    )
    logger.info("Sentry initialized")

# --- Application Event Handlers ---

async def startup_event():
    """
    Actions to perform on application startup.
    - Create database tables.
    """
    logger.info("Application startup event triggered.")
    try:
        logger.info("Synchronizing database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables synchronized successfully.")
    except Exception as e:
        logger.error(f"Database error during startup: {e}", exc_info=True)
    logger.info("Application startup event finished.")

async def shutdown_event():
    """
    Actions to perform on application shutdown.
    """
    logger.info("Application shutdown event triggered.")
    logger.info("Application shutdown event finished.")


# --- FastAPI App Initialization ---

app = FastAPI(
    title=settings.APP_NAME,  # Corrected to use APP_NAME from config
    description="TSG Araştırma Platformu API",
    version=settings.APP_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    on_startup=[startup_event],
    on_shutdown=[shutdown_event],
)

# --- Logging Middleware ---
@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Skip verbose logs for frequent polling endpoint
    if request.url.path == f"{settings.API_V1_STR}/scraping/browser/status":
        return await call_next(request)
    logger.info(f"--> Incoming request: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"<-- Response status: {response.status_code} for path: {request.url.path}")
    return response

# --- Exception Handlers ---

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Log 422 Unprocessable Entity errors to see the malformed request body.
    """
    try:
        body = await request.json()
        logger.error(f"[422 HATA] Gelen hatalı istek body'si: {json.dumps(body)}")
    except Exception as e:
        logger.error(f"[422 HATA] İstek body'si JSON olarak parse edilemedi: {e}")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )


# --- Middleware Configuration ---

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    https_only=settings.SECURE_COOKIE,
    same_site="none",
)

# CORS Middleware Configuration
logger.info(f"CORS ayarları kontrol ediliyor. Yüklenen originler: {settings.CORS_ORIGINS}")
origins = [str(origin) for origin in settings.CORS_ORIGINS]
# Add frontend origin as a fallback to ensure it's always allowed.
if "http://localhost:3000" not in origins:
    origins.append("http://localhost:3000")

if origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# --- API Routers ---
logger.info("Attempting to include main API router with prefix: %s", settings.API_V1_STR)
app.include_router(api_router, prefix=settings.API_V1_STR)
logger.info("Main API router included successfully.")



# --- Static Files ---

os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# --- Root & Health Check Endpoints ---

@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.APP_NAME} API!",
        "version": settings.APP_VERSION,
        "docs": "/api/docs",
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Convenience health endpoint for Caddy checks
@app.get("/api/health")
async def api_health_check():
    return {"status": "healthy"}
