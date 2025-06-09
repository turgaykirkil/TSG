"""Background tasks for the application.

This package contains background tasks that can be executed asynchronously.
Each task type should be defined in its own module in this package.

The task module should define a function named `run_<task_type>` that takes
a context dictionary as its only parameter and returns a result.

The context dictionary contains:
- job_id: The ID of the job
- job_type: The type of the job
- parameters: The job parameters
- db: A database session
- update_progress: A function to update the job progress

Example task module (app/tasks/example.py):

```python
def run_example(context):
    \"\"\"Example task that does some work.\"\"\"
    params = context.get(\"parameters\")
    db = context.get(\"db\")
    update_progress = context.get(\"update_progress\")
    
    # Update progress
    if update_progress:
        update_progress(10, \"Starting work\")
    
    # Do some work...
    
    # Return a result
    return {\"status\": \"success\"}
```
"""

# Import task modules here to register them
# from . import example  # noqa
