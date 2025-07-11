"""
TSG Araştırma Platformu - Ana Uygulama
"""
import os
import logging
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import httpx
import base64
import random

from app.core.config import settings
from app.db.base import Base, engine
from app.api.api_v1.api import api_router
from app.api import upload_api


# Logging ayarları
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)
logger.info("MAIN.PY: Top-level logger configured.")


# Uygulama oluştur
app = FastAPI(
    title=settings.APP_NAME,
    description="TSG Araştırma Platformu API",
    version=settings.APP_VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

@app.on_event("startup")
async def startup_event():
    logger.info("STARTUP_EVENT: Application is starting up. Logging should be working.")
    # start_scheduler()

@app.on_event("shutdown")
def shutdown_event():
    logger.info("SHUTDOWN_EVENT: Application is shutting down.")
    # stop_scheduler()

# Session Middleware (Cookie ayarları için)
# Geliştirme ortamında SameSite=None kullanabilmek için https_only=False olarak ayarlandı.
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,  # .env dosyasından güvenli bir anahtar okunmalı
    https_only=False,  # Geliştirme ortamı için False, production için True olmalı
    same_site="none",
)

# CORS ayarları
# Geliştirme ortamında frontend'den (localhost:3000) gelen isteklere izin ver.
# Production'da bu ayarlar daha kısıtlayıcı olmalıdır.
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=[
        "Accept",
        "Accept-Encoding",
        "Authorization",
        "Content-Type",
        "Origin",
        "X-Requested-With",
        "X-CSRF-Token",
    ],
    expose_headers=["Content-Length", "Set-Cookie", "X-CSRF-Token"],
    max_age=86400,  # 24 hours
)



# Captcha proxy endpoint
@app.get("/captcha")
async def get_captcha():
    try:
        rnd = random.random()
        url = f"https://www.ticaretsicil.gov.tr/captcha/captcha.php?{rnd}"
        async with httpx.AsyncClient() as client:
            resp = await client.get(url)
            resp.raise_for_status()
            encoded = base64.b64encode(resp.content).decode()
        return {"image": f"data:image/jpeg;base64,{encoded}"}
    except Exception as e:
        logger.error("Captcha fetch error: %s", e)
        raise HTTPException(status_code=500, detail="Captcha fetch failed")

# API Routers
app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(upload_api.router, prefix=settings.API_V1_STR)

# Static dosyalar
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Kök endpoint
@app.get("/")
async def root():
    return {
        "message": f"{settings.APP_NAME} API'ye hoş geldiniz!",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "docs": "/api/docs",
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Scheduler durum endpoint'i
@app.get("/scheduler/status")
async def get_scheduler_status():
    from app.core.scheduler import scheduler
    return {
        "status": "running" if scheduler._running else "stopped",
        "tasks": scheduler.get_status() if hasattr(scheduler, 'get_status') else []
    }

# Hata yönetimi
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

# Uygulama başlangıcında yapılacak işlemler
@app.on_event("startup")
async def startup_event():
    logger.info("Uygulama başlangıç olayı (startup event) tetiklendi.")

    try:
        logger.info("Veritabanı bağlantısı deneniyor...")
        # Bağlantıyı test etmek için kısa bir sorgu çalıştır
        with engine.connect() as connection:
            logger.info("Veritabanı bağlantısı başarılı.")
        
        # Tabloları oluştur
        logger.info("Veritabanı tabloları senkronize ediliyor...")
        Base.metadata.create_all(bind=engine)
        logger.info("Veritabanı tabloları başarıyla senkronize edildi.")
    except Exception as e:
        logger.warning("Veritabanı bağlantısı kurulamadı: %s", str(e))
        logger.warning("Uygulama, veritabanı olmadan devam edecek. Veritabanı gerektiren endpoint'ler çalışmayabilir.")
    
    # Scheduler'ı başlat
    try:
        logger.info("Scheduler başlatılıyor...")
        # start_scheduler()
        logger.info("Uygulama başlangıç olayı tamamlandı.")
    except Exception as e:
        logger.error("Arka plan görev planlayıcısı başlatılırken hata oluştu: %s", str(e))

# Uygulama kapanırken yapılacak işlemler
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Uygulama kapatılıyor...")
    
    # Scheduler'ı durdur
    try:
        # stop_scheduler()
        logger.info("Uygulama kapatılıyor...")
    except Exception as e:
        logger.error("Arka plan görev planlayıcısı durdurulurken hata oluştu: %s", str(e))

# Geliştirme modunda çalıştırma
if __name__ == "__main__":
    import uvicorn
    
    # Geliştirme için log seviyesini ayarla
    logging.basicConfig(level=logging.INFO)
    
    # Uygulamayı başlat
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
