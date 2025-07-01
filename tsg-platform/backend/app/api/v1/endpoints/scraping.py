from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel

from app.scraping_chromium import start_scraping_process

router = APIRouter()

class ScrapingRequest(BaseModel):
    count: int = 100 # Varsayılan olarak 100 firma scrape edilsin

@router.post("/start", status_code=202)
async def start_scraping(request: ScrapingRequest, background_tasks: BackgroundTasks):
    """
    Scraping işlemini arka planda başlatır.

    - **count**: Scrape edilecek maksimum firma sayısı.
    """
    if request.count <= 0:
        raise HTTPException(status_code=400, detail="Count 0'dan büyük olmalı.")

    print(f"Arka plan görevi olarak {request.count} firmanın scraping işlemi başlatılıyor.")
    background_tasks.add_task(start_scraping_process, request.count)
    
    return {"message": f"Scraping işlemi {request.count} firma için başarıyla başlatıldı. İşlem arka planda devam edecek."}
