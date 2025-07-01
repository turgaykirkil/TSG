"""
Periodic task scheduler for background jobs.

This module provides functionality to schedule and run periodic background tasks.
"""
import logging
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, Any, Callable, Optional, List

from sqlalchemy.orm import Session

from app import crud, models
from app.core.config import settings
from app.db.session import SessionLocal
from app.schemas.job_history import JobHistoryCreate
from app.utils.background import run_in_background, background_tasks_executor

logger = logging.getLogger(__name__)

class Scheduler:
    """
    A simple scheduler for running periodic background tasks.
    
    This scheduler runs in a separate thread and executes tasks at specified intervals.
    """
    
    def __init__(self):
        """Initialize the scheduler."""
        self._running = False
        self._thread = None
        self._tasks = []
        self._stop_event = threading.Event()
        self._lock = threading.Lock()
    
    def add_task(
        self,
        func: Callable,
        interval: int,
        name: str,
        args: Optional[tuple] = None,
        kwargs: Optional[dict] = None,
        run_immediately: bool = False,
        max_concurrent: int = 1,
    ) -> None:
        """
        Add a task to the scheduler.
        
        Args:
            func: The function to run
            interval: Interval in seconds between runs
            name: Name of the task (for logging)
            args: Positional arguments to pass to the function
            kwargs: Keyword arguments to pass to the function
            run_immediately: Whether to run the task immediately when added
            max_concurrent: Maximum number of concurrent executions of this task
        """
        if args is None:
            args = ()
        if kwargs is None:
            kwargs = {}
            
        task = {
            "func": func,
            "interval": interval,
            "name": name,
            "args": args,
            "kwargs": kwargs,
            "last_run": None,
            "next_run": datetime.utcnow() if run_immediately else None,
            "is_running": False,
            "max_concurrent": max_concurrent,
            "current_runs": 0,
        }
        
        with self._lock:
            self._tasks.append(task)
        
        logger.info("Added scheduled task '%s' with interval %d seconds", name, interval)
    
    def start(self) -> None:
        """Start the scheduler."""
        if self._running:
            logger.warning("Scheduler is already running")
            return
        
        self._running = True
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, daemon=True, name="Scheduler")
        self._thread.start()
        logger.info("Scheduler started")
    
    def stop(self, wait: bool = True) -> None:
        """
        Stop the scheduler.
        
        Args:
            wait: Whether to wait for the scheduler thread to finish
        """
        if not self._running:
            return
            
        logger.info("Stopping scheduler...")
        self._running = False
        self._stop_event.set()
        
        if wait and self._thread and self._thread.is_alive():
            self._thread.join(timeout=5.0)
            if self._thread.is_alive():
                logger.warning("Scheduler thread did not stop gracefully")
    
    def _run(self) -> None:
        """Main scheduler loop."""
        logger.info("Scheduler started with %d tasks", len(self._tasks))
        
        while self._running and not self._stop_event.is_set():
            try:
                now = datetime.utcnow()
                
                with self._lock:
                    for task in self._tasks:
                        # Skip if task is already running and we've reached max concurrency
                        if task["is_running"] and task["current_runs"] >= task["max_concurrent"]:
                            continue
                        
                        # Check if it's time to run the task
                        if task["next_run"] is None or now >= task["next_run"]:
                            # Update task state
                            task["last_run"] = now
                            task["next_run"] = now + timedelta(seconds=task["interval"])
                            task["is_running"] = True
                            task["current_runs"] += 1
                            
                            # Run the task in a background thread
                            self._run_task(task)
                
                # Sleep for a short time to prevent high CPU usage
                time.sleep(0.1)
                
            except Exception as e:
                logger.exception("Error in scheduler loop")
                time.sleep(1)  # Prevent tight loop on errors
    
    def _run_task(self, task: Dict[str, Any]) -> None:
        """
        Run a task in a background thread.
        
        Args:
            task: The task to run
        """
        def task_wrapper():
            task_name = task["name"]
            logger.info("Starting scheduled task '%s'", task_name)
            
            try:
                # Call the task function
                task["func"](*task["args"], **task["kwargs"])
                logger.info("Completed scheduled task '%s'", task_name)
                
            except Exception as e:
                logger.exception("Error in scheduled task '%s'", task_name)
                
            finally:
                # Update task state
                with self._lock:
                    task["is_running"] = False
                    task["current_runs"] -= 1
        
        # Submit the task to the thread pool
        run_in_background(task_wrapper)
    
    def get_status(self) -> List[Dict[str, Any]]:
        """
        Get the status of all scheduled tasks.
        
        Returns:
            List of task status dictionaries
        """
        status = []
        
        with self._lock:
            for task in self._tasks:
                status.append({
                    "name": task["name"],
                    "interval": task["interval"],
                    "last_run": task["last_run"],
                    "next_run": task["next_run"],
                    "is_running": task["is_running"],
                    "current_runs": task["current_runs"],
                    "max_concurrent": task["max_concurrent"],
                })
        
        return status

# Global scheduler instance
scheduler = Scheduler()

def init_scheduler() -> None:
    """Initialize the scheduler with default tasks."""
    from app.tasks.check_stuck_jobs import run_check_stuck_jobs
    from app.tasks.cleanup_jobs import run_cleanup_jobs
    
    # # Add task to check for stuck jobs (Temporarily disabled)
    # scheduler.add_task(
    #     func=run_check_stuck_jobs,
    #     interval=settings.STUCK_JOB_CHECK_INTERVAL,
    #     name="check_stuck_jobs",
    #     kwargs={
    #         "older_than_minutes": settings.JOB_STUCK_AFTER_SECONDS // 60,
    #         "max_retries": settings.MAX_JOB_RETRIES,
    #         "auto_retry": settings.AUTO_RETRY_FAILED_JOBS,
    #     },
    #     run_immediately=False,
    # )
    
    # # Add task to clean up old job records (run once per day) (Temporarily disabled)
    # scheduler.add_task(
    #     func=run_cleanup_jobs,
    #     interval=24 * 60 * 60,  # 24 hours
    #     name="cleanup_jobs",
    #     kwargs={
    #         "completed_days": settings.COMPLETED_JOB_RETENTION_DAYS,
    #         "failed_days": settings.FAILED_JOB_RETENTION_DAYS,
    #     },
    #     run_immediately=False,
    # )
    
    # Start the scheduler
    scheduler.start()
    logger.info("Scheduler initialized with %d tasks", len(scheduler._tasks))

# This function is called when the application starts
def start_scheduler() -> None:
    """Start the scheduler if it's not already running."""
    if not scheduler._running:
        init_scheduler()

# This function is called when the application shuts down
def stop_scheduler() -> None:
    """Stop the scheduler."""
    if scheduler._running:
        scheduler.stop()
        logger.info("Scheduler stopped")
