"""
Example background task implementation.

This module shows how to implement a background task that can be executed
asynchronously through the job system.
"""
import time
from typing import Dict, Any

def run_example(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Example background task that simulates some work.
    
    Args:
        context: Task context containing job information and utilities
        
    Returns:
        A dictionary with the task results
    """
    # Extract useful information from the context
    job_id = context["job_id"]
    job_type = context["job_type"]
    parameters = context["parameters"]
    db = context["db"]
    update_progress = context["update_progress"]
    
    # Log start
    print(f"Starting example task for job {job_id} with parameters: {parameters}")
    
    # Update progress
    update_progress(10, "Starting example task")
    
    # Simulate some work
    time.sleep(2)
    
    # Update progress
    update_progress(30, "Processing items...")
    
    # Simulate more work with progress updates
    total_items = parameters.get("item_count", 10)
    for i in range(total_items):
        # Do some work for each item
        time.sleep(0.5)
        
        # Update progress
        progress = 30 + int((i + 1) * 60 / total_items)
        update_progress(progress, f"Processed item {i+1}/{total_items}")
    
    # Update progress
    update_progress(95, "Finalizing...")
    
    # Simulate some final work
    time.sleep(1)
    
    # Return a result
    result = {
        "status": "completed",
        "items_processed": total_items,
        "message": f"Successfully processed {total_items} items"
    }
    
    return result
