"""
Background task configuration.

This module contains configuration for background tasks and job processing.
"""
from pydantic import BaseSettings, Field

class TaskSettings(BaseSettings):
    """Background task settings."""
    
    # Maximum number of background worker threads
    BACKGROUND_TASKS_MAX_WORKERS: int = Field(
        default=10,
        description="Maximum number of background worker threads"
    )
    
    # Maximum time (in seconds) a job can run before being considered stuck
    JOB_TIMEOUT_SECONDS: int = Field(
        default=3600,  # 1 hour
        description="Maximum time (in seconds) a job can run before being considered stuck"
    )
    
    # How often to check for stuck jobs (in seconds)
    STUCK_JOB_CHECK_INTERVAL: int = Field(
        default=300,  # 5 minutes
        description="How often to check for stuck jobs (in seconds)"
    )
    
    # How old a job must be (in seconds) to be considered stuck
    JOB_STUCK_AFTER_SECONDS: int = Field(
        default=1800,  # 30 minutes
        description="How old a job must be (in seconds) to be considered stuck"
    )
    
    # Maximum number of retries for failed jobs
    MAX_JOB_RETRIES: int = Field(
        default=3,
        description="Maximum number of retries for failed jobs"
    )
    
    # Whether to automatically retry failed jobs
    AUTO_RETRY_FAILED_JOBS: bool = Field(
        default=True,
        description="Whether to automatically retry failed jobs"
    )
    
    # Job cleanup settings
    COMPLETED_JOB_RETENTION_DAYS: int = Field(
        default=30,
        description="Number of days to keep completed job records"
    )
    
    FAILED_JOB_RETENTION_DAYS: int = Field(
        default=90,
        description="Number of days to keep failed job records"
    )
    
    class Config:
        env_prefix = "TASK_"
        case_sensitive = False

# Create settings instance
task_settings = TaskSettings()
