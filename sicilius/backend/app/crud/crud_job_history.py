from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union, TypeVar, Generic, Type

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from fastapi import HTTPException, status

from app.crud.base import CRUDBase
from app.models.job_history import JobHistory, JobStatus, JobType
from app.schemas.job_history import JobHistoryCreate, JobHistoryUpdate

class CRUDJobHistory(CRUDBase[JobHistory, JobHistoryCreate, JobHistoryUpdate]):
    def get_by_status(
        self, 
        db: Session, 
        *, 
        status: JobStatus, 
        job_type: Optional[JobType] = None,
        skip: int = 0, 
        limit: int = 100
    ) -> List[JobHistory]:
        """Belirli bir durumdaki iş geçmişi kayıtlarını getirir."""
        query = db.query(JobHistory).filter(JobHistory.status == status)
        
        if job_type is not None:
            query = query.filter(JobHistory.job_type == job_type)
            
        return (
            query.order_by(desc(JobHistory.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_type(
        self, 
        db: Session, 
        *, 
        job_type: JobType, 
        status: Optional[JobStatus] = None,
        skip: int = 0, 
        limit: int = 100
    ) -> List[JobHistory]:
        """Belirli bir iş türündeki iş geçmişi kayıtlarını getirir."""
        query = db.query(JobHistory).filter(JobHistory.job_type == job_type)
        
        if status is not None:
            query = query.filter(JobHistory.status == status)
            
        return (
            query.order_by(desc(JobHistory.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_user(
        self, 
        db: Session, 
        *, 
        user_id: int, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[JobHistory]:
        """Belirli bir kullanıcıya ait iş geçmişi kayıtlarını getirir."""
        return (
            db.query(JobHistory)
            .filter(JobHistory.user_id == user_id)
            .order_by(desc(JobHistory.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_running_jobs(
        self, 
        db: Session, 
        *, 
        job_type: Optional[JobType] = None,
        older_than_minutes: int = 30
    ) -> List[JobHistory]:
        """Çalışmakta olan işleri getirir."""
        time_threshold = datetime.utcnow() - timedelta(minutes=older_than_minutes)
        
        query = db.query(JobHistory).filter(
            and_(
                JobHistory.status == JobStatus.RUNNING,
                JobHistory.started_at > time_threshold
            )
        )
        
        if job_type is not None:
            query = query.filter(JobHistory.job_type == job_type)
            
        return query.all()
    
    def get_stuck_jobs(
        self, 
        db: Session, 
        *, 
        job_type: Optional[JobType] = None,
        older_than_minutes: int = 120
    ) -> List[JobHistory]:
        """Uzun süredir çalışan veya takılmış işleri getirir."""
        time_threshold = datetime.utcnow() - timedelta(minutes=older_than_minutes)
        
        query = db.query(JobHistory).filter(
            and_(
                JobHistory.status == JobStatus.RUNNING,
                JobHistory.started_at < time_threshold
            )
        )
        
        if job_type is not None:
            query = query.filter(JobHistory.job_type == job_type)
            
        return query.all()
    
    def create_job(
        self, 
        db: Session, 
        *, 
        job_type: JobType,
        job_name: str,
        user_id: Optional[int] = None,
        file_upload_id: Optional[int] = None,
        parameters: Optional[Dict[str, Any]] = None,
        description: Optional[str] = None
    ) -> JobHistory:
        """Yeni bir iş kaydı oluşturur."""
        job_in = JobHistoryCreate(
            job_type=job_type,
            job_name=job_name,
            status=JobStatus.PENDING,
            description=description,
            user_id=user_id,
            file_upload_id=file_upload_id,
            parameters=parameters or {}
        )
        return self.create(db, obj_in=job_in)
    
    def start_job(
        self, 
        db: Session, 
        *, 
        db_obj: JobHistory
    ) -> JobHistory:
        """İşi başlatılmış olarak işaretler."""
        if db_obj.status != JobStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Job is not in PENDING status. Current status: {db_obj.status}"
            )
            
        update_data = {
            "status": JobStatus.RUNNING,
            "started_at": datetime.utcnow(),
            "progress": 0
        }
        
        return self.update(db, db_obj=db_obj, obj_in=update_data)
    
    def update_progress(
        self, 
        db: Session, 
        *, 
        db_obj: JobHistory,
        progress: int,
        result_summary: Optional[Dict[str, Any]] = None
    ) -> JobHistory:
        """İşin ilerleme durumunu günceller."""
        if db_obj.status != JobStatus.RUNNING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Job is not in RUNNING status. Current status: {db_obj.status}"
            )
            
        update_data = {"progress": min(max(progress, 0), 100)}
        
        if result_summary is not None:
            update_data["result_summary"] = result_summary
            
        return self.update(db, db_obj=db_obj, obj_in=update_data)
    
    def complete_job(
        self, 
        db: Session, 
        *, 
        db_obj: JobHistory,
        result_summary: Optional[Dict[str, Any]] = None,
        error_message: Optional[str] = None
    ) -> JobHistory:
        """İşi tamamlanmış olarak işaretler."""
        update_data = {
            "status": JobStatus.COMPLETED if not error_message else JobStatus.FAILED,
            "completed_at": datetime.utcnow(),
            "progress": 100,
            "result_summary": result_summary or {},
            "error_message": error_message
        }
        
        if error_message:
            update_data["status"] = JobStatus.FAILED
        
        return self.update(db, db_obj=db_obj, obj_in=update_data)
    
    def cancel_job(
        self, 
        db: Session, 
        *, 
        db_obj: JobHistory,
        reason: Optional[str] = None
    ) -> JobHistory:
        """İptal edilmiş olarak işaretler."""
        update_data = {
            "status": JobStatus.CANCELLED,
            "completed_at": datetime.utcnow(),
            "error_message": reason or "Job was cancelled by user"
        }
        
        return self.update(db, db_obj=db_obj, obj_in=update_data)

# JobHistory CRUD işlemleri için singleton örneği
job_history = CRUDJobHistory(JobHistory)
