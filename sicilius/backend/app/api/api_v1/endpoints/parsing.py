import io
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import re

import pdfplumber
from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from app.db.session import get_db
from app.models.company import Company
from app.utils.office_normalization import normalize_office_freeform

# --- Pydantic Models ---

class ParsedTable(BaseModel):
    table_name: str
    headers: List[str]
    rows: List[Dict[str, Any]]

# Frontend'den gelen veri için Pydantic modeli
class CompanyUploadData(BaseModel):
    sicil_no: str
    firma_unvani: Optional[str] = None # 'unvan' -> 'firma_unvani' olarak güncellendi
    adres: Optional[str] = None
    sicil_mudurluk: Optional[str] = None # sicil_mudurluk eklendi

# Veritabanı şeması için Pydantic modeli
class CompanyDBData(BaseModel):
    sicil_no: str
    unvan: Optional[str] = None
    address: Optional[str] = None
    sicil_mudurluk: Optional[str] = None
    sicil_office_code: Optional[str] = None

class SaveCompaniesRequest(BaseModel):
    companies: List[CompanyUploadData]

class SaveResponse(BaseModel):
    status: str = "success"
    message: str
    processed_rows: int

# --- Router Definition ---
router = APIRouter()

logger = logging.getLogger(__name__)

# --- Helper Functions ---
def clean_text(text: Any) -> str:
    if text is None:
        return ""
    return str(text).strip()

def normalize_sicil_no(value: Optional[str]) -> Optional[str]:
    """
    Sicil numarasını normalize eder: None için None döner, boşlukları temizler.
    Gelecekte gerekirse rakam dışı karakterleri de ayıklayacak şekilde genişletilebilir.
    """
    if value is None:
        return None
    # Tüm boşlukları kaldır ve kırp
    return re.sub(r"\s+", "", str(value)).strip()

def normalize_office(value: Optional[str]) -> Optional[str]:
    """Merkezi ofis normalizasyonunu kullan."""
    return normalize_office_freeform(value)



# --- API Endpoints ---

@router.post("/parse-pdf", response_model=List[ParsedTable], tags=["Parsing"])
async def parse_pdf_file(files: List[UploadFile] = File(...)):
    """
    Parses multiple PDF files, merges all tables from all pages,
    and returns a single merged table for user review.
    """
    logger.info("parse-pdf called files=%s", len(files) if files else 0)
    master_header = None
    all_data_rows_as_lists = []
    first_file_processed = False

    for file in files:
        if not file.filename.lower().endswith('.pdf'):
            logging.warning(f"Skipping non-PDF file: {file.filename}")
            continue

        try:
            file_content = await file.read()
            with pdfplumber.open(io.BytesIO(file_content)) as pdf:
                if not pdf.pages:
                    logging.warning(f"PDF is empty and has no pages: {file.filename}")
                    continue

                current_file_rows = []
                for page in pdf.pages:
                    tables = page.extract_tables()
                    for table in tables:
                        if table:
                            cleaned_table = [[clean_text(cell) for cell in row] for row in table]
                            current_file_rows.extend(cleaned_table)

                if not current_file_rows:
                    logging.warning(f"No tables found in PDF: {file.filename}")
                    continue

                if not first_file_processed:
                    master_header = current_file_rows[0]
                    all_data_rows_as_lists.extend(current_file_rows[1:])
                    first_file_processed = True
                else:
                    all_data_rows_as_lists.extend(current_file_rows[1:])

        except Exception as e:
            logging.error(f"Error processing PDF file {file.filename}: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"An error occurred while processing {file.filename}: {e}")

    if not master_header:
        logger.warning("parse-pdf no header extracted")
        raise HTTPException(status_code=400, detail="No valid tables with headers found in any of the uploaded PDF files.")

    all_data_rows_as_lists = [row for row in all_data_rows_as_lists if any(row)]
    logger.info("parse-pdf merged rows=%s header_len=%s", len(all_data_rows_as_lists), len(master_header or []))

    all_data_rows_as_dicts = []
    for row in all_data_rows_as_lists:
        padded_row = row + [''] * (len(master_header) - len(row))
        all_data_rows_as_dicts.append(dict(zip(master_header, padded_row)))

    final_merged_table = ParsedTable(
        table_name="Merged PDF Data",
        headers=master_header,
        rows=all_data_rows_as_dicts
    )

    logger.info("parse-pdf returning rows=%s", len(all_data_rows_as_dicts))

    return [final_merged_table]


@router.post("/companies/save", response_model=SaveResponse, tags=["Parsing"])
async def save_companies_data(payload: SaveCompaniesRequest, db: Session = Depends(get_db)):
    """
    Receives structured company data and upserts it into the 'companies' table.
    """
    # Yinelenen kayıtları sicil numarasına göre filtrele (sadece sonuncuyu tut)
    logger.info("companies/save called incoming=%s", len(payload.companies) if payload and payload.companies else 0)
    unique_companies: Dict[str, CompanyUploadData] = {}
    skipped_missing_sicil = 0
    skipped_missing_office = 0
    for company_data in payload.companies:
        # Normalize alanlar
        company_data.sicil_no = normalize_sicil_no(company_data.sicil_no)
        company_data.sicil_mudurluk = normalize_office(company_data.sicil_mudurluk)
        if not company_data.sicil_no:
            skipped_missing_sicil += 1
            continue
        if not company_data.sicil_mudurluk:
            skipped_missing_office += 1
            continue
        unique_companies[company_data.sicil_no] = company_data

    logger.info(
        "companies/save normalized unique=%s skipped_sicil=%s skipped_office=%s",
        len(unique_companies), skipped_missing_sicil, skipped_missing_office
    )

    records_to_upsert = []
    for company_data in unique_companies.values():
        db_data = CompanyDBData(
            sicil_no=company_data.sicil_no,
            unvan=company_data.firma_unvani,
            address=company_data.adres,
            sicil_mudurluk=company_data.sicil_mudurluk,
            sicil_office_code=company_data.sicil_mudurluk,
        )
        records_to_upsert.append(db_data.dict(exclude_none=True))

    if not records_to_upsert:
        logger.warning("companies/save nothing to upsert")
        raise HTTPException(status_code=400, detail="No company data provided to save.")

    try:
        logger.info(
            "Upserting %s records to 'companies' table. skipped_sicil=%s skipped_office=%s",
            len(records_to_upsert), skipped_missing_sicil, skipped_missing_office
        )
        
        # SQLAlchemy ile bulk upsert işlemi
        stmt = insert(Company).values(records_to_upsert)
        update_stmt = stmt.on_conflict_do_update(
            index_elements=['sicil_no', 'sicil_office_code'],
            set_={
                'unvan': stmt.excluded.unvan,
                'address': stmt.excluded.address,
                # Mevcut kayıtlarda sicil_mudurluk / office_code formatını koru (Altın Kural)
                # 'sicil_mudurluk' ve 'sicil_office_code' ÇAKIŞMADA güncellenmez.
            }
        )
        db.execute(update_stmt)
        db.commit()
        logger.info("companies/save committed upserted=%s", len(records_to_upsert))

        return SaveResponse(
            message=(
                f"Successfully saved {len(records_to_upsert)} company records. "
                f"Skipped (missing sicil_no): {skipped_missing_sicil}; "
                f"Skipped (missing office): {skipped_missing_office}"
            ),
            processed_rows=len(records_to_upsert)
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Error saving company data with SQLAlchemy: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An error occurred while saving data: {str(e)}")
