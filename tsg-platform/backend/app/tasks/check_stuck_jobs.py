"""
Check for and handle stuck jobs.

This module provides functionality to identify and handle jobs that have been
running for too long and may be stuck.
"""
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

from sqlalchemy.orm import Session

from app import crud, models
from app.core.config import settings
from app.db.session import SessionLocal
from app.schemas.job_history_process import JobStatusResponse

logger = logging.getLogger(__name__)

def find_stuck_jobs(
    db: Session,
    older_than_minutes: Optional[int] = None,
    job_type: Optional[str] = None
) -> List[models.JobHistory]:
    """
    Find jobs that have been running for too long and may be stuck.
    
    Args:
        db: Database session
        older_than_minutes: Consider jobs older than this many minutes as stuck
        job_type: Only check jobs of this type
        
    Returns:
        List of stuck jobs
    """
    if older_than_minutes is None:
        older_than_minutes = settings.JOB_STUCK_AFTER_SECONDS // 60
    
    time_threshold = datetime.utcnow() - timedelta(minutes=older_than_minutes)
    
    query = db.query(models.JobHistory).filter(
        models.JobHistory.status == "running",
        models.JobHistory.started_at < time_threshold
    )
    
    if job_type:
        query = query.filter(models.JobHistory.job_type == job_type)
    
    return query.all()

def handle_stuck_job(
    db: Session,
    job: models.JobHistory,
    max_retries: Optional[int] = None,
    auto_retry: Optional[bool] = None,
) -> Dict[str, Any]:
    """
    Handle a stuck job by marking it as failed or retrying it.
    
    Args:
        db: Database session
        job: The stuck job
        max_retries: Maximum number of retries before giving up
        auto_retry: Whether to automatically retry the job
        
    Returns:
        Dictionary with the result of the operation
    """
    if max_retries is None:
        max_retries = settings.MAX_JOB_RETRIES
    if auto_retry is None:
        auto_retry = settings.AUTO_RETRY_FAILED_JOBS
    
    job_id = job.id
    retry_count = job.retry_count or 0
    
    result = {
        "job_id": job_id,
        "job_type": job.job_type,
        "status": job.status,
        "started_at": job.started_at.isoformat() if job.started_at else None,
        "retry_count": retry_count,
        "action_taken": None,
        "message": None,
        "error": None
    }
    
    try:
        # Check if we should retry the job
        if auto_retry and retry_count < max_retries:
            # Mark the job as failed with a retry message
            error_msg = (
                f"Job was running for too long and was marked as failed. "
                f"Retry {retry_count + 1}/{max_retries}."
            )
            
            # Update the job status
            job = crud.job_history.update(
                db,
                db_obj=job,
                obj_in={
                    "status": "failed",
                    "error_message": error_msg,
                    "completed_at": datetime.utcnow(),
                    "retry_count": retry_count + 1
                }
            )
            
            # Create a new job to retry the operation
            new_job = crud.job_history.create(
                db,
                obj_in={
                    "job_type": job.job_type,
                    "job_name": f"Retry: {job.job_name}",
                    "status": "pending",
                    "description": f"Retry of job #{job.id} after being stuck",
                    "parameters": job.parameters or {},
                    "user_id": job.user_id,
                    "file_upload_id": job.file_upload_id,
                    "retry_count": retry_count + 1
                }
            )
            
            result.update({
                "action_taken": "retried",
                "message": f"Job marked as failed and queued for retry (attempt {retry_count + 1}/{max_retries})",
                "new_job_id": new_job.id
            })
            
            logger.info(
                "Marked stuck job %d as failed and queued retry %d/%d as job %d",
                job_id, retry_count + 1, max_retries, new_job.id
            )
            
        else:
            # Mark the job as failed permanently
            error_msg = "Job was running for too long and was terminated"
            if retry_count >= max_retries:
                error_msg += f" (max retries {max_retries} reached)"
            
            job = crud.job_history.update(
                db,
                db_obj=job,
                obj_in={
                    "status": "failed",
                    "error_message": error_msg,
                    "completed_at": datetime.utcnow(),
                    "retry_count": retry_count
                }
            )
            
            result.update({
                "action_taken": "failed",
                "message": error_msg
            })
            
            logger.warning(
                "Marked stuck job %d as failed permanently (retry %d/%d)",
                job_id, retry_count, max_retries
            )
        
        db.commit()
        return result
        
    except Exception as e:
        db.rollback()
        error_msg = f"Error handling stuck job {job_id}: {str(e)}"
        logger.exception(error_msg)
        
        result.update({
            "action_taken": "error",
            "error": str(e),
            "message": "Error handling stuck job"
        })
        
        return result

def check_and_handle_stuck_jobs(
    db: Session,
    older_than_minutes: Optional[int] = None,
    job_type: Optional[str] = None,
    max_retries: Optional[int] = None,
    auto_retry: Optional[bool] = None,
) -> Dict[str, Any]:
    """
    Check for stuck jobs and handle them.
    
    Args:
        db: Database session
        older_than_minutes: Consider jobs older than this many minutes as stuck
        job_type: Only check jobs of this type
        max_retries: Maximum number of retries before giving up
        auto_retry: Whether to automatically retry the job
        
    Returns:
        Dictionary with the results of the operation
    """
    try:
        # Find stuck jobs
        stuck_jobs = find_stuck_jobs(db, older_than_minutes, job_type)
        
        if not stuck_jobs:
            return {
                "status": "completed",
                "message": "No stuck jobs found",
                "stuck_jobs_found": 0,
                "handled_jobs": []
            }
        
        # Handle each stuck job
        handled_jobs = []
        for job in stuck_jobs:
            result = handle_stuck_job(
                db=db,
                job=job,
                max_retries=max_retries,
                auto_retry=auto_retry
            )
            handled_jobs.append(result)
        
        # Return results
        return {
            "status": "completed",
            "message": f"Found and handled {len(stuck_jobs)} stuck jobs",
            "stuck_jobs_found": len(stuck_jobs),
            "handled_jobs": handled_jobs
        }
        
    except Exception as e:
        error_msg = f"Error checking for stuck jobs: {str(e)}"
        logger.exception(error_msg)
        
        return {
            "status": "failed",
            "error": str(e),
            "message": "Error checking for stuck jobs"
        }

def run_check_stuck_jobs(
    context: dict = None,
    older_than_minutes: int = None,
    job_type: str = None,
    max_retries: int = None,
    auto_retry: bool = None
) -> dict:
    """
    Run the stuck jobs check task.
    
    This function is called by the background task system.
    
    Args:
        context: Task context (optional)
        older_than_minutes: Consider jobs older than this many minutes as stuck
        job_type: Only check jobs of this type
        max_retries: Maximum number of retries before giving up
        auto_retry: Whether to automatically retry the job
        
    Returns:
        Dictionary with the results of the operation
    """
    # Initialize variables
    update_progress = None
    db = None
    
    # Handle context if provided
    if context is not None and isinstance(context, dict):
        update_progress = context.get("update_progress")
        db = context.get("db")
        
        # Get parameters from context if not provided directly
        if older_than_minutes is None or max_retries is None or auto_retry is None:
            params = context.get("parameters", {})
            if older_than_minutes is None:
                older_than_minutes = params.get("older_than_minutes")
            if job_type is None:
                job_type = params.get("job_type")
            if max_retries is None:
                max_retries = params.get("max_retries")
            if auto_retry is None:
                auto_retry = params.get("auto_retry")
    
    # Create a new database session if none was provided
    if db is None:
        db = SessionLocal()
        created_db = True
    else:
        created_db = False
    
    try:
        # Update progress if callback is provided
        if update_progress:
            update_progress(10, "Starting stuck jobs check")
        
        # Check for stuck jobs
        if update_progress:
            update_progress(50, "Checking for stuck jobs")
        
        result = check_and_handle_stuck_jobs(
            db=db,
            older_than_minutes=older_than_minutes,
            job_type=job_type,
            max_retries=max_retries,
            auto_retry=auto_retry
        )
        
        # Update progress
        if update_progress:
            update_progress(100, "Stuck jobs check completed")
        
        return result
        
    except Exception as e:
        logger.exception("Error in stuck jobs check task")
        return {
            "status": "failed",
            "error": str(e),
            "message": "Failed to check for stuck jobs"
        }
    finally:
        # Only close the session if we created it
        if db and not context.get("db"):
            db.close()

# This allows the task to be run directly for testing
if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO)
    
    # Parse command line arguments
    older_than = None
    job_type = None
    
    if len(sys.argv) > 1:
        try:
            older_than = int(sys.argv[1])
        except (ValueError, IndexError):
            pass
    
    if len(sys.argv) > 2:
        job_type = sys.argv[2]
    
    # Run the check
    db = SessionLocal()
    try:
        result = run_check_stuck_jobs({
            "db": db,
            "parameters": {
                "older_than_minutes": older_than,
                "job_type": job_type
            }
        })
        print(f"Check result: {result}")
    finally:
        db.close()
