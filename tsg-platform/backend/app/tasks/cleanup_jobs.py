"""
Cleanup old job records.

This module provides functionality to clean up old job records from the database.
"""
import logging
from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy.orm import Session

from app import crud, models
from app.core.config import settings
from app.db.session import SessionLocal

logger = logging.getLogger(__name__)

def cleanup_old_jobs(
    db: Session,
    completed_days: Optional[int] = None,
    failed_days: Optional[int] = None,
) -> dict:
    """
    Clean up old job records from the database.
    
    Args:
        db: Database session
        completed_days: Number of days to keep completed jobs (defaults to settings)
        failed_days: Number of days to keep failed jobs (defaults to settings)
        
    Returns:
        Dictionary with cleanup statistics
    """
    if completed_days is None:
        completed_days = settings.COMPLETED_JOB_RETENTION_DAYS
    if failed_days is None:
        failed_days = settings.FAILED_JOB_RETENTION_DAYS
    
    # Calculate cutoff dates
    now = datetime.utcnow()
    completed_cutoff = now - timedelta(days=completed_days)
    failed_cutoff = now - timedelta(days=failed_days)
    
    # Initialize counters
    stats = {
        "total_deleted": 0,
        "completed_deleted": 0,
        "failed_deleted": 0,
        "cancelled_deleted": 0,
        "other_deleted": 0,
        "remaining": 0,
    }
    
    try:
        # Delete old completed jobs
        result = db.query(models.JobHistory).filter(
            models.JobHistory.status == "completed",
            models.JobHistory.completed_at < completed_cutoff
        ).delete(synchronize_session=False)
        stats["completed_deleted"] = result
        stats["total_deleted"] += result
        
        # Delete old failed jobs
        result = db.query(models.JobHistory).filter(
            models.JobHistory.status == "failed",
            models.JobHistory.completed_at < failed_cutoff
        ).delete(synchronize_session=False)
        stats["failed_deleted"] = result
        stats["total_deleted"] += result
        
        # Delete old cancelled jobs
        result = db.query(models.JobHistory).filter(
            models.JobHistory.status == "cancelled",
            models.JobHistory.completed_at < completed_cutoff
        ).delete(synchronize_session=False)
        stats["cancelled_deleted"] = result
        stats["total_deleted"] += result
        
        # Count remaining jobs
        stats["remaining"] = db.query(models.JobHistory).count()
        
        # Commit the transaction
        db.commit()
        
        logger.info(
            "Cleaned up %d old job records (%d completed, %d failed, %d cancelled), %d remaining",
            stats["total_deleted"],
            stats["completed_deleted"],
            stats["failed_deleted"],
            stats["cancelled_deleted"],
            stats["remaining"]
        )
        
        return stats
        
    except Exception as e:
        db.rollback()
        logger.exception("Error cleaning up old job records")
        raise

def run_cleanup_jobs(
    context: dict = None,
    completed_days: int = None,
    failed_days: int = None
) -> dict:
    """
    Run the job cleanup task.
    
    This function is called by the background task system.
    
    Args:
        context: Task context (optional)
        completed_days: Number of days to keep completed jobs
        failed_days: Number of days to keep failed jobs
        
    Returns:
        Dictionary with cleanup statistics
    """
    # Initialize variables
    update_progress = None
    db = None
    
    # Handle context if provided
    if context is not None and isinstance(context, dict):
        update_progress = context.get("update_progress")
        db = context.get("db")
        
        # Get parameters from context if not provided directly
        if completed_days is None or failed_days is None:
            params = context.get("parameters", {})
            if completed_days is None:
                completed_days = params.get("completed_days")
            if failed_days is None:
                failed_days = params.get("failed_days")
    
    # Create a new database session if none was provided
    if db is None:
        db = SessionLocal()
        created_db = True
    else:
        created_db = False
    
    try:
        # Update progress if callback is provided
        if update_progress:
            update_progress(10, "Starting job cleanup")
        
        # Clean up old jobs
        if update_progress:
            update_progress(50, "Cleaning up old job records")
        
        stats = cleanup_old_jobs(
            db=db,
            completed_days=completed_days,
            failed_days=failed_days,
        )
        
        # Update progress
        if update_progress:
            update_progress(100, "Job cleanup completed")
        
        return {
            "status": "completed",
            "stats": stats,
            "message": f"Cleaned up {stats['total_deleted']} old job records"
        }
        
    except Exception as e:
        logger.exception("Error in job cleanup task")
        return {
            "status": "failed",
            "error": str(e),
            "message": "Failed to clean up job records"
        }
    finally:
        # Only close the session if we created it
        if db and created_db:
            db.close()

# This allows the task to be run directly for testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    db = SessionLocal()
    try:
        result = run_cleanup_jobs({"db": db})
        print(f"Cleanup result: {result}")
    finally:
        db.close()
