import logging

from celery import Celery
from celery.signals import after_setup_logger

from app.core.config import get_settings

# Proje ayarlarını yükle
settings = get_settings()

# Celery uygulamasını oluştur ve yapılandır
celery_app = Celery(
    "worker",  # Uygulama adı
    broker=str(settings.REDIS_URL),  # Görev kuyruğu için Redis bağlantısı
    backend=str(settings.REDIS_URL),  # Sonuçları saklamak için Redis bağlantısı
    include=["app.tasks.scraping_tasks", "app.tasks.ocr_tasks"]  # Görevlerin bulunduğu modülü belirt
)

# Celery için ek yapılandırma ayarları
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Europe/Istanbul",
    enable_utc=True,
    # Ayar dosyasından zaman aşımlarını al
    task_soft_time_limit=settings.JOB_TIMEOUT_SECONDS,  # 1 saat sonra uyarı
    task_time_limit=settings.JOB_TIMEOUT_SECONDS + 300, # 1 saat 5 dk sonra sonlandır
)

@after_setup_logger.connect
def setup_loggers(logger, **kwargs):
    """
    Redirect Celery log output to the console.
    """
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

# Bu dosya doğrudan çalıştırıldığında Celery worker'ını başlatmak için kullanılır.
if __name__ == "__main__":
    celery_app.start()
