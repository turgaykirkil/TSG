"""
Job History API endpoints
"""
from datetime import datetime, timedelta
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query, BackgroundTasks
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.schemas.job_history_process import (
    JobStartRequest,
    JobUpdateRequest,
    JobFilter,
    JobStats,
    JobStatusResponse,
    JobResultSummary,
    JobProgressUpdate
)
from app.utils.background import run_background_task

router = APIRouter()

def get_job_or_404(
    db: Session, 
    job_id: int, 
    current_user: models.User
) -> models.JobHistory:
    """Get a job by ID or raise 404 if not found or not authorized."""
    job = crud.job_history.get(db, id=job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    # Only admin can access jobs of other users
    if not crud.user.is_superuser(current_user) and job.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this job"
        )
    
    return job

@router.post("/", response_model=schemas.JobHistory, status_code=status.HTTP_201_CREATED)
def create_job(
    *,
    db: Session = Depends(deps.get_db),
    job_in: JobStartRequest,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create a new background job.
    """
    # Check file upload exists if provided
    if job_in.file_upload_id is not None:
        file_upload = crud.file_upload.get(db, id=job_in.file_upload_id)
        if not file_upload:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File upload not found"
            )
    
    # Create the job
    job = crud.job_history.create_job(
        db,
        job_type=job_in.job_type,
        job_name=job_in.job_name,
        description=job_in.description,
        user_id=current_user.id,
        file_upload_id=job_in.file_upload_id,
        parameters=job_in.parameters
    )
    
    return job

@router.get("/{job_id}", response_model=schemas.JobHistory)
def read_job(
    *,
    db: Session = Depends(deps.get_db),
    job_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get job by ID.
    """
    return get_job_or_404(db, job_id, current_user)

@router.get("/", response_model=List[schemas.JobHistory])
def read_jobs(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    job_type: Optional[str] = None,
    user_id: Optional[int] = None,
    file_upload_id: Optional[int] = None,
    search: Optional[str] = None,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve jobs with optional filtering.
    """
    # Non-admin users can only see their own jobs
    if not crud.user.is_superuser(current_user):
        user_id = current_user.id
    
    query = db.query(models.JobHistory)
    
    # Apply filters
    if status:
        query = query.filter(models.JobHistory.status == status)
    if job_type:
        query = query.filter(models.JobHistory.job_type == job_type)
    if user_id is not None:
        query = query.filter(models.JobHistory.user_id == user_id)
    if file_upload_id is not None:
        query = query.filter(models.JobHistory.file_upload_id == file_upload_id)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (models.JobHistory.job_name.ilike(search_term)) |
            (models.JobHistory.description.ilike(search_term))
        )
    
    return query.order_by(models.JobHistory.created_at.desc()).offset(skip).limit(limit).all()

@router.get("/stats/", response_model=JobStats)
def get_job_stats(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get job statistics.
    """
    # Non-admin users can only see their own stats
    filter_kwargs = {}
    if not crud.user.is_superuser(current_user):
        filter_kwargs["user_id"] = current_user.id
    
    # Get total counts
    total = db.query(models.JobHistory).filter_by(**filter_kwargs).count()
    pending = db.query(models.JobHistory).filter_by(
        status="pending", **filter_kwargs
    ).count()
    running = db.query(models.JobHistory).filter_by(
        status="running", **filter_kwargs
    ).count()
    completed = db.query(models.JobHistory).filter_by(
        status="completed", **filter_kwargs
    ).count()
    failed = db.query(models.JobHistory).filter_by(
        status="failed", **filter_kwargs
    ).count()
    cancelled = db.query(models.JobHistory).filter_by(
        status="cancelled", **filter_kwargs
    ).count()
    
    # Get counts by job type
    from sqlalchemy import func
    type_counts = {}
    rows = db.query(
        models.JobHistory.job_type,
        func.count(models.JobHistory.id)
    ).filter_by(**filter_kwargs).group_by(models.JobHistory.job_type).all()
    
    for job_type, count in rows:
        type_counts[job_type] = count
    
    # Calculate average duration for completed jobs
    avg_duration = None
    if completed > 0:
        duration_expr = func.extract('epoch', models.JobHistory.completed_at - models.JobHistory.started_at)
        avg_duration = db.query(
            func.avg(duration_expr)
        ).filter(
            models.JobHistory.status == "completed",
            models.JobHistory.started_at.isnot(None),
            models.JobHistory.completed_at.isnot(None),
            **filter_kwargs
        ).scalar()
    
    return JobStats(
        total_jobs=total,
        pending=pending,
        running=running,
        completed=completed,
        failed=failed,
        cancelled=cancelled,
        by_type=type_counts,
        avg_duration_seconds=avg_duration
    )

@router.post("/{job_id}/start/", response_model=schemas.JobHistory)
def start_job(
    *,
    db: Session = Depends(deps.get_db),
    job_id: int,
    background_tasks: BackgroundTasks,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Start a pending job.
    """
    job = get_job_or_404(db, job_id, current_user)
    
    try:
        # Mark job as running
        job = crud.job_history.start_job(db, db_obj=job)
        
        # Run the job in background
        background_tasks.add_task(
            run_background_task,
            db=db,
            job_id=job.id,
            job_type=job.job_type,
            parameters=job.parameters or {}
        )
        
        return job
    except HTTPException as e:
        raise e
    except Exception as e:
        # Update job status to failed
        crud.job_history.update(
            db,
            db_obj=job,
            obj_in={
                "status": "failed",
                "error_message": str(e),
                "completed_at": datetime.utcnow()
            }
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start job: {str(e)}"
        )

@router.post("/{job_id}/cancel/", response_model=schemas.JobHistory)
def cancel_job(
    *,
    db: Session = Depends(deps.get_db),
    job_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Cancel a running or pending job.
    """
    job = get_job_or_404(db, job_id, current_user)
    
    if job.status not in ["pending", "running"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot cancel job with status: {job.status}"
        )
    
    job = crud.job_history.cancel_job(
        db,
        db_obj=job,
        reason="Cancelled by user"
    )
    
    # TODO: Implement actual task cancellation if needed
    
    return job

@router.post("/{job_id}/progress/", response_model=schemas.JobHistory)
def update_job_progress(
    *,
    db: Session = Depends(deps.get_db),
    job_id: int,
    progress_in: JobProgressUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update job progress.
    """
    job = get_job_or_404(db, job_id, current_user)
    
    if job.status != "running":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot update progress for job with status: {job.status}"
        )
    
    update_data = {
        "progress": progress_in.progress,
        "result_summary": progress_in.result_summary.dict() if progress_in.result_summary else None
    }
    
    return crud.job_history.update_progress(
        db,
        db_obj=job,
        progress=progress_in.progress,
        result_summary=update_data["result_summary"]
    )

@router.get("/{job_id}/status/", response_model=JobStatusResponse)
def get_job_status(
    *,
    db: Session = Depends(deps.get_db),
    job_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get job status.
    """
    job = get_job_or_404(db, job_id, current_user)
    
    return JobStatusResponse(
        job_id=job.id,
        status=job.status,
        progress=job.progress,
        message=job.error_message,
        result_summary=job.result_summary,
        created_at=job.created_at,
        started_at=job.started_at,
        completed_at=job.completed_at
    )

@router.get("/stuck/", response_model=List[schemas.JobHistory])
def get_stuck_jobs(
    db: Session = Depends(deps.get_db),
    older_than_minutes: int = 120,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Get jobs that have been running for too long (admin only).
    """
    return crud.job_history.get_stuck_jobs(
        db,
        older_than_minutes=older_than_minutes
    )

@router.post("/{job_id}/retry/", response_model=schemas.JobHistory)
def retry_job(
    *,
    db: Session = Depends(deps.get_db),
    job_id: int,
    background_tasks: BackgroundTasks,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retry a failed or cancelled job.
    """
    job = get_job_or_404(db, job_id, current_user)
    
    if job.status not in ["failed", "cancelled"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot retry job with status: {job.status}"
        )
    
    # Create a new job with the same parameters
    new_job = crud.job_history.create_job(
        db,
        job_type=job.job_type,
        job_name=f"Retry: {job.job_name}",
        description=f"Retry of job #{job.id}",
        user_id=current_user.id,
        file_upload_id=job.file_upload_id,
        parameters=job.parameters or {}
    )
    
    # Start the new job
    background_tasks.add_task(
        run_background_task,
        db=db,
        job_id=new_job.id,
        job_type=new_job.job_type,
        parameters=new_job.parameters or {}
    )
    
    return new_job
