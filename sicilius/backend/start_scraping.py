import sys
from app.tasks.scraping_tasks import run_scraping_task
print("Enqueueing scraping task for İstanbul...")
try:
    task = run_scraping_task.delay(count=50, mode="city_fill", city="İSTANBUL")
    print(f"Task enqueued! ID: {task.id}")
except Exception as e:
    print(f"Failed: {e}")
