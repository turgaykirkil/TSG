"""
Background task execution utilities.
"""
import importlib
import logging
from typing import Any, Dict, Optional, Callable, TypeVar, cast
from concurrent.futures import ThreadPoolExecutor, Future
import asyncio

from fastapi import BackgroundTasks
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.core.config import settings
from app.db.session import SessionLocal

# Configure logging
logger = logging.getLogger(__name__)

# Type variable for generic function return type
R = TypeVar('R')

# Global thread pool for background tasks
background_tasks_executor = ThreadPoolExecutor(
    max_workers=settings.BACKGROUND_TASKS_MAX_WORKERS,
    thread_name_prefix="bg_task_"
)

def run_in_background(
    func: Callable[..., R],
    *args: Any,
    **kwargs: Any
) -> Future[R]:
    """
    Run a function in the background thread pool.
    
    Args:
        func: The function to run
        *args: Positional arguments to pass to the function
        **kwargs: Keyword arguments to pass to the function
        
    Returns:
        A Future representing the result of the function call.
    """
    return background_tasks_executor.submit(func, *args, **kwargs)

async def run_async_in_background(
    func: Callable[..., R],
    *args: Any,
    **kwargs: Any
) -> R:
    """
    Run a function in the background thread pool asynchronously.
    
    Args:
        func: The function to run
        *args: Positional arguments to pass to the function
        **kwargs: Keyword arguments to pass to the function
        
    Returns:
        The result of the function call.
    """
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        background_tasks_executor,
        lambda: func(*args, **kwargs)
    )

def run_background_task(
    db: Session,
    job_id: int,
    job_type: str,
    parameters: Dict[str, Any],
) -> None:
    """
    Run a background task based on job type and parameters.
    
    This function is called in a background thread and should handle its own errors.
    """
    db_job = None
    
    try:
        # Get a new database session for this background task
        db = SessionLocal()
        
        # Get the job from the database
        db_job = crud.job_history.get(db, id=job_id)
        if not db_job:
            logger.error(f"Job {job_id} not found in database")
            return
        
        # Mark job as running
        db_job = crud.job_history.start_job(db, db_obj=db_job)
        db.commit()
        
        logger.info(f"Starting background job {job_id} of type {job_type}")
        
        # Import the appropriate task module and function
        module_name = f"app.tasks.{job_type.lower()}"
        function_name = f"run_{job_type.lower()}"
        
        try:
            module = importlib.import_module(module_name)
            task_func = getattr(module, function_name)
        except (ImportError, AttributeError) as e:
            error_msg = f"Could not find task function {function_name} in module {module_name}: {str(e)}"
            logger.error(error_msg)
            raise ValueError(error_msg) from e
        
        # Prepare the task context
        task_context = {
            "job_id": job_id,
            "job_type": job_type,
            "parameters": parameters,
            "db": db,
            "update_progress": lambda progress, message=None, result_summary=None: update_job_progress(
                db, job_id, progress, message, result_summary
            )
        }
        
        # Run the task
        result = task_func(task_context)
        
        # Mark job as completed
        db.refresh(db_job)
        crud.job_history.complete_job(
            db,
            db_obj=db_job,
            result_summary={"result": result} if result is not None else None
        )
        db.commit()
        
        logger.info(f"Completed background job {job_id} of type {job_type}")
        
    except Exception as e:
        logger.exception(f"Error in background job {job_id}")
        
        # Update job status to failed
        if db_job:
            try:
                crud.job_history.complete_job(
                    db,
                    db_obj=db_job,
                    error_message=str(e)
                )
                db.commit()
            except Exception as db_error:
                logger.exception(f"Error updating job status to failed: {str(db_error)}")
    
    finally:
        # Ensure the database session is closed
        if 'db' in locals():
            db.close()

def update_job_progress(
    db: Session,
    job_id: int,
    progress: int,
    message: Optional[str] = None,
    result_summary: Optional[Dict[str, Any]] = None
) -> None:
    """
    Update job progress in the database.
    
    Args:
        db: Database session
        job_id: Job ID
        progress: Progress percentage (0-100)
        message: Optional progress message
        result_summary: Optional result summary
    """
    try:
        # Get the job
        job = crud.job_history.get(db, id=job_id)
        if not job:
            logger.warning(f"Job {job_id} not found when updating progress")
            return
        
        # Update progress
        update_data = {
            "progress": max(0, min(100, progress))
        }
        
        if message:
            update_data["message"] = message
            
        if result_summary is not None:
            # Merge with existing result summary if any
            current_summary = job.result_summary or {}
            if isinstance(current_summary, dict):
                current_summary.update(result_summary)
                update_data["result_summary"] = current_summary
            else:
                update_data["result_summary"] = result_summary
        
        # Save to database
        crud.job_history.update(db, db_obj=job, obj_in=update_data)
        db.commit()
        
    except Exception as e:
        logger.exception(f"Error updating job {job_id} progress: {str(e)}")
        # Don't re-raise to avoid crashing the background task

def add_background_task(
    background_tasks: BackgroundTasks,
    job_type: str,
    job_name: str,
    parameters: Dict[str, Any],
    description: Optional[str] = None,
    file_upload_id: Optional[int] = None,
    current_user: Optional[models.User] = None,
) -> models.JobHistory:
    """
    Add a background task to be executed.
    
    This is a convenience function that creates a job record and schedules
    the task to run in the background.
    
    Args:
        background_tasks: FastAPI BackgroundTasks instance
        job_type: Type of job (must match a task module name)
        job_name: Human-readable name for the job
        parameters: Parameters to pass to the task
        description: Optional description
        file_upload_id: Optional ID of a file upload this job is related to
        current_user: Current user (if any)
        
    Returns:
        The created JobHistory record
    """
    db = SessionLocal()
    try:
        # Create the job record
        job = crud.job_history.create_job(
            db,
            job_type=job_type,
            job_name=job_name,
            description=description,
            user_id=current_user.id if current_user else None,
            file_upload_id=file_upload_id,
            parameters=parameters
        )
        
        # Schedule the task to run in the background
        background_tasks.add_task(
            run_background_task,
            db=db,
            job_id=job.id,
            job_type=job_type,
            parameters=parameters
        )
        
        return job
    finally:
        db.close()
