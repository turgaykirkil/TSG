from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps
from app.models.company_scrape import CompanyScrape
from app.schemas.company_scrape import CompanyScrapeCreate, CompanyScrapeUpdate, CompanyScrapeInDB

router = APIRouter(prefix="/company-scrapes", tags=["Company Scrapes"])

@router.post("/batch", response_model=List[schemas.CompanyScrape], status_code=201)
def batch_create_companies(
    *,
    db: Session = Depends(deps.get_db),
    companies_in: List[schemas.CompanyScrapeCreate],
) -> List[CompanyScrape]:
    """
    Toplu olarak şirket kayıtları oluştur.
    Aynı sicil no'ya sahip kayıtlar güncellenir.
    """
    result = []
    for company_in in companies_in:
        # Mevcut kaydı kontrol et
        company = crud.company_scrape.get_by_sicil_no(db, sicil_no=company_in.sicil_no)
        
        if company:
            # Eğer kayıt varsa ve son scraping üzerinden 3 ay geçmediyse güncelleme yapma
            if not company.needs_scraping:
                result.append(company)
                continue
                
            # Güncelleme verilerini hazırla
            update_data = {
                "firma_unvani": company_in.firma_unvani,
                "is_scraped": company_in.is_scraped if company_in.is_scraped is not None else company.is_scraped,
                "last_scraped_at": datetime.utcnow() if company_in.is_scraped else company.last_scraped_at,
            }
            
            # Kaydı güncelle
            updated_company = crud.company_scrape.update(db, db_obj=company, obj_in=update_data)
            result.append(updated_company)
        else:
            # Yeni kayıt oluştur
            new_company = crud.company_scrape.create(db, obj_in=company_in)
            result.append(new_company)
    
    return result

@router.post("/", response_model=schemas.CompanyScrape, status_code=201)
def create_company_scrape(
    *,
    db: Session = Depends(deps.get_db),
    company_in: schemas.CompanyScrapeCreate,
) -> CompanyScrape:
    """
    Yeni bir şirket kaydı oluştur.
    Aynı sicil no'ya sahip kayıt varsa günceller.
    """
    # Mevcut kaydı kontrol et
    company = crud.company_scrape.get_by_sicil_no(db, sicil_no=company_in.sicil_no)
    
    if company:
        # Eğer kayıt varsa ve son scraping üzerinden 3 ay geçmediyse güncelleme yapma
        if not company.needs_scraping:
            return company
            
        # Güncelleme verilerini hazırla
        update_data = {
            "firma_unvani": company_in.firma_unvani,
            "is_scraped": company_in.is_scraped if company_in.is_scraped is not None else company.is_scraped,
            "last_scraped_at": datetime.utcnow() if company_in.is_scraped else company.last_scraped_at,
        }
        
        # Kaydı güncelle
        company = crud.company_scrape.update(db, db_obj=company, obj_in=update_data)
        return company
    
    # Yeni kayıt oluştur
    return crud.company_scrape.create(db, obj_in=company_in)

@router.get("/{sicil_no}", response_model=schemas.CompanyScrape, status_code=200)
def read_company(
    *,
    db: Session = Depends(deps.get_db),
    sicil_no: str,
) -> CompanyScrape:
    """
    Sicil numarasına göre şirket bilgilerini getir.
    """
    company = crud.company_scrape.get_by_sicil_no(db, sicil_no=sicil_no)
    if not company:
        raise HTTPException(status_code=404, detail="Şirket bulunamadı")
    return company

@router.get("/needs-scraping/", response_model=List[schemas.CompanyScrape], status_code=200)
def get_companies_needing_scraping(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> List[CompanyScrape]:
    """
    Scraping yapılması gereken şirketleri getir.
    """
    return crud.company_scrape.get_multi_needing_scraping(db, skip=skip, limit=limit)

@router.put("/{company_id}/mark-scraped", response_model=schemas.CompanyScrape, status_code=200)
def mark_as_scraped(
    *,
    db: Session = Depends(deps.get_db),
    company_id: int,
) -> CompanyScrape:
    """
    Şirketin scraping işleminin tamamlandığını işaretle.
    """
    company = crud.company_scrape.get(db, id=company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Şirket bulunamadı")
    
    update_data = {
        "is_scraped": True,
        "last_scraped_at": datetime.utcnow()
    }
    
    return crud.company_scrape.update(db, db_obj=company, obj_in=update_data)
