from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_


from app.crud.base import CRUDBase
from app.models.file_upload import FileUpload, FileUploadStatus, FileUploadType
from app.schemas.file_upload import FileUploadCreate, FileUploadUpdate

class CRUDFileUpload(CRUDBase[FileUpload, FileUploadCreate, FileUploadUpdate]):
    def get_by_filename(self, db: Session, *, filename: str) -> Optional[FileUpload]:
        """Dosya adına göre dosya yükleme kaydı getirir."""
        return db.query(FileUpload).filter(FileUpload.file_name == filename).first()
    
    def get_by_status(
        self, db: Session, *, status: FileUploadStatus, skip: int = 0, limit: int = 100
    ) -> List[FileUpload]:
        """Belirli bir durumdaki dosya yükleme kayıtlarını getirir."""
        return (
            db.query(FileUpload)
            .filter(FileUpload.status == status)
            .order_by(FileUpload.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_upload_type(
        self, db: Session, *, upload_type: FileUploadType, skip: int = 0, limit: int = 100
    ) -> List[FileUpload]:
        """Belirli bir yükleme türündeki dosya yükleme kayıtlarını getirir."""
        return (
            db.query(FileUpload)
            .filter(FileUpload.upload_type == upload_type)
            .order_by(FileUpload.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_uploader(
        self, db: Session, *, uploaded_by_id: int, skip: int = 0, limit: int = 100
    ) -> List[FileUpload]:
        """Belirli bir kullanıcı tarafından yüklenen dosyaları getirir."""
        return (
            db.query(FileUpload)
            .filter(FileUpload.uploaded_by_id == uploaded_by_id)
            .order_by(FileUpload.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def search(
        self, 
        db: Session, 
        *, 
        query: str, 
        skip: int = 0, 
        limit: int = 100,
        upload_type: Optional[FileUploadType] = None
    ) -> List[FileUpload]:
        """Dosya adı veya açıklamasında arama yapar."""
        search = f"%{query}%"
        query_filter = [
            or_(
                FileUpload.file_name.ilike(search),
                FileUpload.description.ilike(search)
            )
        ]
        
        if upload_type is not None:
            query_filter.append(FileUpload.upload_type == upload_type)
        
        return (
            db.query(FileUpload)
            .filter(and_(*query_filter))
            .order_by(FileUpload.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def update_status(
        self, 
        db: Session, 
        *, 
        db_obj: FileUpload, 
        status: FileUploadStatus,
        error_message: Optional[str] = None,
        processed_records: Optional[int] = None,
        failed_records: Optional[int] = None
    ) -> FileUpload:
        """Dosya yükleme durumunu günceller."""
        update_data = {
            "status": status,
            "processed_at": datetime.utcnow() if status == FileUploadStatus.PROCESSED else None,
            "error_message": error_message
        }
        
        if processed_records is not None:
            update_data["processed_records"] = processed_records
        
        if failed_records is not None:
            update_data["failed_records"] = failed_records
        
        return self.update(db, db_obj=db_obj, obj_in=update_data)
    
    def mark_as_processed(
        self, 
        db: Session, 
        *, 
        db_obj: FileUpload,
        processed_records: int,
        failed_records: int = 0,
        error_message: Optional[str] = None
    ) -> FileUpload:
        """Dosyayı işlendi olarak işaretler."""
        return self.update_status(
            db,
            db_obj=db_obj,
            status=FileUploadStatus.PROCESSED,
            error_message=error_message,
            processed_records=processed_records,
            failed_records=failed_records
        )
    
    def mark_as_failed(
        self, 
        db: Session, 
        *, 
        db_obj: FileUpload,
        error_message: str
    ) -> FileUpload:
        """Dosyayı başarısız olarak işaretler."""
        return self.update_status(
            db,
            db_obj=db_obj,
            status=FileUploadStatus.FAILED,
            error_message=error_message
        )

# FileUpload CRUD işlemleri için singleton örneki
file_upload = CRUDFileUpload(FileUpload)
