from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
from app.models.job_history import JobStatus, JobType

class JobResultSummary(BaseModel):
    """
    Job işlemi sonucunda oluşan özet bilgileri içerir.
    """
    total_items: int = Field(0, description="Toplam işlenen öğe sayısı")
    success_count: int = Field(0, description="Başarılı işlem sayısı")
    error_count: int = Field(0, description="Hata sayısı")
    warnings: List[str] = Field(default_factory=list, description="Uyarı mesajları")
    details: Optional[Dict[str, Any]] = Field(None, description="Detaylı sonuçlar")

class JobProgressUpdate(BaseModel):
    """
    Job ilerleme durumu güncellemeleri için şema.
    """
    progress: int = Field(..., ge=0, le=100, description="İlerleme yüzdesi (0-100)")
    message: Optional[str] = Field(None, description="İlerleme durum mesajı")
    result_summary: Optional[JobResultSummary] = Field(None, description="Şu ana kadarki işlem özeti")

class JobStartRequest(BaseModel):
    """
    Yeni bir iş başlatma isteği için şema.
    """
    job_type: JobType = Field(..., description="İş türü")
    job_name: str = Field(..., max_length=255, description="İş adı")
    description: Optional[str] = Field(None, description="İş açıklaması")
    parameters: Dict[str, Any] = Field(
        default_factory=dict, 
        description="İşlem parametreleri"
    )
    file_upload_id: Optional[int] = Field(
        None, 
        description="İlişkili dosya yükleme ID'si (varsa)"
    )

class JobUpdateRequest(BaseModel):
    """
    Mevcut bir işi güncellemek için şema.
    """
    status: Optional[JobStatus] = Field(None, description="Yeni durum")
    progress: Optional[int] = Field(None, ge=0, le=100, description="İlerleme yüzdesi (0-100)")
    message: Optional[str] = Field(None, description="Durum mesajı")
    error_message: Optional[str] = Field(None, description="Hata mesajı (varsa)")
    result_summary: Optional[Dict[str, Any]] = Field(None, description="İşlem sonuç özeti")

class JobFilter(BaseModel):
    """
    İş geçmişi filtreleme için şema.
    """
    status: Optional[JobStatus] = Field(None, description="İş durumuna göre filtreleme")
    job_type: Optional[JobType] = Field(None, description="İş türüne göre filtreleme")
    user_id: Optional[int] = Field(None, description="Kullanıcı ID'sine göre filtreleme")
    file_upload_id: Optional[int] = Field(None, description="Dosya yükleme ID'sine göre filtreleme")
    start_date: Optional[datetime] = Field(None, description="Başlangıç tarihine göre filtreleme")
    end_date: Optional[datetime] = Field(None, description="Bitiş tarihine göre filtreleme")
    search: Optional[str] = Field(None, description="İş adı veya açıklamasında arama")

class JobStats(BaseModel):
    """
    İş istatistikleri için şema.
    """
    total_jobs: int = 0
    pending: int = 0
    running: int = 0
    completed: int = 0
    failed: int = 0
    cancelled: int = 0
    by_type: Dict[str, int] = Field(default_factory=dict)
    avg_duration_seconds: Optional[float] = None

class JobStatusResponse(BaseModel):
    """İş durumu yanıtı için şema."""
    job_id: int
    status: JobStatus
    progress: int
    message: Optional[str] = None
    result_summary: Optional[Dict[str, Any]] = None
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "job_id": 1,
                "status": "completed",
                "progress": 100,
                "message": "İşlem başarıyla tamamlandı",
                "result_summary": {"imported": 10, "failed": 0},
                "created_at": "2023-01-01T00:00:00",
                "started_at": "2023-01-01T00:00:00",
                "completed_at": "2023-01-01T00:05:00"
            }
        }
    }
