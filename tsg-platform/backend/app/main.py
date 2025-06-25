"""
TSG Araştırma Platformu - Ana Uygulama
"""
import os
import logging
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.scheduler import start_scheduler, stop_scheduler
from app.api.v1 import api_router
from app.db.base import Base, engine
from app.api import upload_api

# Logging ayarları
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Uygulama oluştur
app = FastAPI(
    title=settings.APP_NAME,
    description="TSG Araştırma Platformu API",
    version=settings.APP_VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tüm origin'lere izin ver
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Tüm yanıtlara CORS başlıkları ekle
@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, DELETE, PUT, PATCH, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

# Static dosyalar
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# API router'larını ekle
app.include_router(api_router, prefix="/api")
app.include_router(upload_api.router, prefix="/api")

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
    # Veritabanı bağlantısını test et ve gerekirse tabloları oluştur
    try:
        # Bağlantıyı test etmek için kısa bir sorgu çalıştır
        with engine.connect() as connection:
            logger.info("Veritabanı bağlantısı başarılı.")
        
        # Tabloları oluştur
        Base.metadata.create_all(bind=engine)
        logger.info("Veritabanı tabloları başarıyla senkronize edildi.")
    except Exception as e:
        logger.warning("Veritabanı bağlantısı kurulamadı: %s", str(e))
        logger.warning("Uygulama, veritabanı olmadan devam edecek. Veritabanı gerektiren endpoint'ler çalışmayabilir.")
    
    # Scheduler'ı başlat
    try:
        start_scheduler()
        logger.info("Arka plan görev planlayıcısı başlatıldı")
    except Exception as e:
        logger.error("Arka plan görev planlayıcısı başlatılırken hata oluştu: %s", str(e))

# Uygulama kapanırken yapılacak işlemler
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Uygulama kapatılıyor...")
    
    # Scheduler'ı durdur
    try:
        stop_scheduler()
        logger.info("Arka plan görev planlayıcısı durduruldu")
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
