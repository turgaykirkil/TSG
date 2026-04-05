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
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from app.api.api_v1.api import api_router
from app.core.config import settings
from app.db.session import engine, Base
from app import models  # Bütün modelleri Base'e kaydetmek için
from app.api import upload_api
from app.core.rate_limit import limiter, RateLimitExceeded, _rate_limit_exceeded_handler

# --- Logging Configuration ---
# LOG_LEVEL can be set to DEBUG/INFO/WARNING/ERROR. Default: WARNING
log_level_str = os.getenv("LOG_LEVEL", "WARNING").upper()
log_level = getattr(logging, log_level_str, logging.INFO)
logging.basicConfig(
    level=log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Reduce noisy logs from common third-party libraries unless explicitly overridden
for noisy_logger in [
    "uvicorn",
    "uvicorn.access",
    "httpx",
    "httpcore",
    "anyio",
    "asyncio",
    "sqlalchemy.engine",
]:
    try:
        logging.getLogger(noisy_logger).setLevel(logging.WARNING)
    except Exception:
        pass

# Completely suppress urllib3 retry warnings (MinIO connection attempts)
# These generate excessive logs (5 retries per bucket = 10+ lines)
for silent_logger in ["urllib3", "urllib3.connectionpool"]:
    try:
        logging.getLogger(silent_logger).setLevel(logging.ERROR)
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
    - Establish SSH database tunnel if local.
    - Create database tables.
    """
    logger.debug("Application startup event triggered.")
    
    # Auto-start SSH Tunnels if not in production and ports aren't in use
    try:
        if os.getenv("ENVIRONMENT", "local") == "local":
            import subprocess
            import socket
            
            def check_port(port):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = s.connect_ex(('127.0.0.1', port))
                s.close()
                return result == 0

            # 1. Check Database Port (5434)
            if not check_port(5434):
                logger.info("DB tunnel not detected on 5434 — managed by start_local.sh, skipping.")

            # 2. Check MinIO Port (9000)
            if not check_port(9000):
                logger.info("MinIO tunnel not detected on 9000 — managed externally, skipping.")
                
    except Exception as e:
        logger.warning(f"Failed to verify/start SSH tunnels: {e}")

    try:
        logger.debug("Synchronizing database tables...")
        Base.metadata.create_all(bind=engine)
        logger.debug("Database tables synchronized successfully.")
    except Exception as e:
        logger.error(f"Database error during startup: {e}")

    logger.debug("Application startup event finished.")

async def shutdown_event():
    """
    Actions to perform on application shutdown.
    """
    logger.debug("Application shutdown event triggered.")
    logger.debug("Application shutdown event finished.")


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

# Add rate limiter state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Ensure scheme/host are derived from reverse proxy headers (X-Forwarded-Proto, etc.)
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")

# --- Request Logging Toggle ---
# REQUEST_LOGGING=true enables per-request logs; default is off to keep terminal clean.
REQUEST_LOGGING = os.getenv("REQUEST_LOGGING", "false").lower() == "true"
# Gate 422 detailed body logs behind an env flag (default off)
LOG_422_DETAILS = os.getenv("LOG_422_DETAILS", "false").lower() == "true"

# --- Logging Middleware ---
@app.middleware("http")
async def log_requests(request: Request, call_next):
    # If request logging is disabled, just continue
    if not REQUEST_LOGGING:
        return await call_next(request)
    # Skip verbose logs for frequent polling endpoint
    if request.url.path == f"{settings.API_V1_STR}/scraping/browser/status":
        return await call_next(request)
    logger.info(f"--> {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"<-- {response.status_code} {request.url.path}")
    return response

# --- Exception Handlers ---

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    422 Unprocessable Entity - detay gövde logları LOG_422_DETAILS=true ise yazılır.
    """
    if LOG_422_DETAILS:
        try:
            body = await request.json()
            logger.warning(f"[422 DETAY] Hatalı istek body: {json.dumps(body)}")
        except Exception as e:
            logger.warning(f"[422 DETAY] Body JSON parse edilemedi: {e}")

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
logger.debug(f"CORS ayarları kontrol ediliyor. Yüklenen originler: {settings.CORS_ORIGINS}")
origins = [str(origin) for origin in settings.CORS_ORIGINS]
# Add frontend origin as a fallback to ensure it's always allowed.
if "http://localhost:3000" not in origins:
    origins.append("http://localhost:3000")
# Also ensure production domains are allowed even if env parsing fails
for _o in ("https://sicilius.com.tr", "https://www.sicilius.com.tr"):
    if _o not in origins:
        origins.append(_o)

if origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# --- API Routers ---
logger.debug("Attempting to include main API router with prefix: %s", settings.API_V1_STR)
app.include_router(api_router, prefix=settings.API_V1_STR)
logger.debug("Main API router included successfully.")



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
