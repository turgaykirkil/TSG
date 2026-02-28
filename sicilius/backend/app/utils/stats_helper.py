from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from app.models.app_setting import AppSetting

STATS_KEY = "storage_stats"

def get_storage_file_count(db: Session, default: int = 0) -> int:
    """Retrieves the current total file count from AppSettings."""
    setting = db.query(AppSetting).filter(AppSetting.key == STATS_KEY).first()
    if setting and setting.value:
        return int(setting.value.get("total_files", default))
    return default

def increment_storage_file_count(db: Session, delta: int = 1) -> int:
    """
    Increments (or decrements if negative) the total file count safely.
    Uses atomic update pattern if possible, but for JSONB simple read-modify-write is okay for low concurrency.
    For high concurrency, this should be a raw SQL UPDATE.
    """
    try:
        # Fetch existing
        setting = db.query(AppSetting).with_for_update().filter(AppSetting.key == STATS_KEY).first()
        
        current_val = 0
        if setting:
            current_val = int(setting.value.get("total_files", 0))
            new_val = max(0, current_val + delta)
            # Update existing
            # Note: We must create a new dict to ensure SQLAlchemy detects change on JSONB
            setting.value = {"total_files": new_val, "updated_at": str(import_datetime().utcnow())}
        else:
            # Create new
            new_val = max(0, delta) # Assume starting from 0 if not exists
            setting = AppSetting(
                key=STATS_KEY,
                value={"total_files": new_val, "updated_at": str(import_datetime().utcnow())}
            )
            db.add(setting)
        
        db.commit()
        return new_val
    except Exception:
        db.rollback()
        return -1

def set_initial_storage_file_count(db: Session, count: int) -> None:
    """Sets the counter to a specific value (for seeding)."""
    try:
        setting = db.query(AppSetting).filter(AppSetting.key == STATS_KEY).first()
        if setting:
            setting.value = {"total_files": count}
        else:
            setting = AppSetting(key=STATS_KEY, value={"total_files": count})
            db.add(setting)
        db.commit()
    except Exception:
        db.rollback()
        raise

def import_datetime():
    from datetime import datetime
    return datetime
