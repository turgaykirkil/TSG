import logging
from datetime import datetime
from fastapi import APIRouter, Body, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, List, Union, Optional

from app.services import nlp_service
from app.services import ingest_service
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_supabase_client
from supabase import Client
from app import crud
from app.models.gazette import Gazette
from app.models.file_upload import FileUploadStatus

logger = logging.getLogger(__name__)

router = APIRouter()

class NlpRequest(BaseModel):
    text: str

@router.post("/parse-announcement", response_model=Dict[str, Any])
async def parse_text(
    request_body: NlpRequest
):
    """
    Receives raw text and uses the NLP service to parse it,
    extracting structured information like company name, address, etc.
    """
    logger.info("Received request for NLP parsing.")
    if not request_body.text or not request_body.text.strip():
        raise HTTPException(status_code=400, detail="Text content cannot be empty.")

    try:
        # Ensure the model is loaded before parsing
        if nlp_service.nlp_model is None:
            nlp_service.load_spacy_model()
            
        parsed_data = nlp_service.parse_announcement_text(request_body.text)
        logger.info("Successfully parsed text.")
        return parsed_data
    except Exception as e:
        logger.error(f"An error occurred during NLP parsing: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to parse text due to an internal server error: {e}")

@router.post("/parse-announcements", response_model=List[Dict[str, Any]])
async def parse_text_multiple(
    request_body: NlpRequest
):
    """
    Splits the incoming OCR text into multiple announcements and parses each segment.
    Returns a list where each item contains the structured fields plus
    `index`, `sicil_office_header`, and `original_text`.
    """
    logger.info("Received request for MULTI NLP parsing. text_len=%s", len(request_body.text or ""))
    if not request_body.text or not request_body.text.strip():
        raise HTTPException(status_code=400, detail="Text content cannot be empty.")

    try:
        if nlp_service.nlp_model is None:
            nlp_service.load_spacy_model()

        parsed_list = nlp_service.parse_multiple_announcements(request_body.text)
        logger.info("Successfully parsed multiple announcements. count=%d", len(parsed_list))
        return parsed_list
    except Exception as e:
        logger.error(f"An error occurred during MULTI NLP parsing: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to parse text due to an internal server error: {e}")


@router.post("/ingest-announcements", response_model=Dict[str, Any])
async def ingest_announcements(
    request_body: NlpRequest,
    db: Session = Depends(get_db)
):
    """
    OCR metnini ilânlara böler ve her bir segment için:
      - (sicil_no, sicil_mudurluk, unvan, address) alanlarını çıkarır ve `companies` tablosuna upsert eder,
      - Eşleşen/oluşan şirketin UUID'si ile bir `Announcement` kaydı oluşturur,
      - Ham ilan metnini ve parse edilmiş JSON'u `OcrResult` içine yazar.

    Zorunlu alanlar: sicil_no, sicil_mudurluk (biri eksikse o kayıt atlanır)
    Opsiyonel alanlar: unvan, address
    """
    logger.info(
        "Received request for INGEST of announcements into companies. text_len=%s preview=%s",
        len(request_body.text or ""), (request_body.text or "").strip().replace("\n", " ")[:120]
    )
    if not request_body.text or not request_body.text.strip():
        raise HTTPException(status_code=400, detail="Text content cannot be empty.")

    try:
        if nlp_service.nlp_model is None:
            nlp_service.load_spacy_model()

        parsed_list = nlp_service.parse_multiple_announcements(request_body.text)
        # Alan mevcutluğu istatistikleri (ön teşhis)
        has_reg = sum(1 for it in parsed_list if (it.get("registration_number") or it.get("sicil_dosya_no")))
        has_header = sum(1 for it in parsed_list if it.get("sicil_office_header"))
        logger.info("Parsed segments=%s with reg_present=%s header_present=%s", len(parsed_list), has_reg, has_header)
        result = ingest_service.ingest_companies_and_announcements(parsed_list, db)
        payload = {
            "parsed_count": len(parsed_list),
            **result,  # inserted/updated/skipped/office_mismatch/errors, plus announcements_created/ocr_results_created/links
        }
        logger.info(
            "Ingest finished. parsed=%d inserted=%d updated=%d skipped=%d announcements=%d ocr=%d",
            len(parsed_list), payload.get("inserted", 0), payload.get("updated", 0), payload.get("skipped", 0),
            payload.get("announcements_created", 0), payload.get("ocr_results_created", 0)
        )
        return payload
    except Exception as e:
        logger.error(f"An error occurred during ingest: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to ingest due to an internal server error: {e}")


@router.post("/ingest-structured", response_model=Dict[str, Any])
async def ingest_structured(
    request_body: Union[List[Dict[str, Any]], Dict[str, Any]] = Body(...),
    db: Session = Depends(get_db),
    supabase: Client = Depends(get_supabase_client),
):
    """
    Swift uygulamasının veya harici bir istemcinin ürettiği parse edilmiş ilanları doğrudan ingest eder.

    Beklenen giriş biçimleri:
      - Doğrudan liste: `[ { ...parsed_announcement... }, ... ]`
      - Sözlük: `{ "items": [...]} | {"parsed": [...]} | {"data": [...] }`

    Her öğe ideal olarak `original_text`, `sicil_office_header`, `registration_number` (veya `sicil_dosya_no`) alanlarını içermelidir.
    NLP yeniden çalıştırılmaz; gelen veri `ingest_service.ingest_companies_and_announcements()`'a iletilir.
    """
    try:
        # Giriş payload'ını normalize et
        parsed_list: List[Dict[str, Any]]
        raw_text: Optional[str] = None
        source_file: Optional[Dict[str, Any]] = None
        delete_after_ingest: bool = False

        if isinstance(request_body, list):
            parsed_list = request_body
        elif isinstance(request_body, dict):
            # Esnek alan isimleri
            for key in ("items", "parsed", "data"):
                if isinstance(request_body.get(key), list):
                    parsed_list = request_body[key]  # type: ignore[index]
                    break
            else:
                raise HTTPException(status_code=400, detail="Payload must be a list or contain an array under 'items' | 'parsed' | 'data'.")
            # Üst seviye ham metin alanı (opsiyonel)
            for tkey in ("raw_text", "text", "full_text"):
                if isinstance(request_body.get(tkey), str):
                    raw_text = request_body[tkey]  # type: ignore[index]
                    break
            # Opsiyonel silme ve kaynak dosya bilgisi
            if isinstance(request_body.get("source_file"), dict):
                source_file = request_body["source_file"]  # type: ignore[index]
            if isinstance(request_body.get("delete_after_ingest"), bool):
                delete_after_ingest = bool(request_body.get("delete_after_ingest"))
        else:
            raise HTTPException(status_code=400, detail="Unsupported payload type.")

        # Boş kontrolü
        if not parsed_list:
            raise HTTPException(status_code=400, detail="Parsed list is empty.")

        # Hızlı alan mevcutluğu istatistikleri
        # original_text'i offsets ile doldurma (varsa)
        filled_from_offsets = 0
        if raw_text:
            for it in parsed_list:
                if not it.get("original_text"):
                    start = it.get("start_offset")
                    end = it.get("end_offset")
                    if isinstance(start, int) and isinstance(end, int) and 0 <= start <= end <= len(raw_text):
                        it["original_text"] = raw_text[start:end]
                        filled_from_offsets += 1

        has_reg = sum(1 for it in parsed_list if (it.get("registration_number") or it.get("sicil_dosya_no")))
        has_header = sum(1 for it in parsed_list if it.get("sicil_office_header"))
        has_text = sum(1 for it in parsed_list if it.get("original_text"))
        logger.info(
            "Received request for INGEST-STRUCTURED. items=%s reg_present=%s header_present=%s original_text_present=%s filled_from_offsets=%s raw_text_provided=%s",
            len(parsed_list), has_reg, has_header, has_text, filled_from_offsets, bool(raw_text)
        )

        result = ingest_service.ingest_companies_and_announcements(parsed_list, db)

        # Ingest başarıysa ve istek silme istiyorsa, Supabase Storage'dan dosyayı sil ve DB'yi güncelle
        storage_deleted = False
        delete_error: Optional[str] = None
        if source_file and delete_after_ingest:
            bucket = source_file.get("bucket")
            path = source_file.get("path")
            gazette_id = source_file.get("gazette_id")
            file_upload_id = source_file.get("file_upload_id")

            if not bucket or not path:
                logger.warning("delete_after_ingest=true ancak source_file.bucket veya source_file.path eksik")
            else:
                try:
                    # Supabase Storage: dosyayı sil
                    supabase.storage.from_(bucket).remove([path])
                    storage_deleted = True
                    logger.info("Storage deletion succeeded for %s/%s", bucket, path)
                except Exception as e:
                    delete_error = f"Storage deletion failed: {e}"
                    logger.error(delete_error, exc_info=True)

                # DB işaretleme (best effort)
                try:
                    if gazette_id:
                        gaz = db.query(Gazette).filter(Gazette.id == gazette_id).first()
                        if gaz:
                            gaz.is_processed = True
                            gaz.processed_at = datetime.utcnow()
                            db.add(gaz)
                            db.commit()
                            db.refresh(gaz)
                    if file_upload_id:
                        fu = crud.file_upload.get(db, id=file_upload_id)
                        if fu:
                            meta = fu.file_metadata or {}
                            if isinstance(meta, dict):
                                meta["deleted_from_storage"] = storage_deleted
                                meta["deleted_path"] = path
                                meta["deleted_bucket"] = bucket
                                if storage_deleted:
                                    meta["deleted_at"] = datetime.utcnow().isoformat()
                            update_data: Dict[str, Any] = {
                                "status": FileUploadStatus.COMPLETED,
                                "processed_at": datetime.utcnow(),
                                "file_metadata": meta,
                            }
                            crud.file_upload.update(db, db_obj=fu, obj_in=update_data)
                except Exception as e:
                    logger.error(f"Post-delete DB update failed: {e}", exc_info=True)

        payload = {
            "parsed_count": len(parsed_list),
            **result,
        }
        if source_file is not None:
            payload.update({
                "delete_after_ingest": delete_after_ingest,
                "storage_deleted": storage_deleted,
            })
            if delete_error:
                payload["delete_error"] = delete_error
        logger.info(
            "Ingest-structured finished. parsed=%d inserted=%d updated=%d skipped=%d announcements=%d ocr=%d",
            len(parsed_list), payload.get("inserted", 0), payload.get("updated", 0), payload.get("skipped", 0),
            payload.get("announcements_created", 0), payload.get("ocr_results_created", 0)
        )
        return payload
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"An error occurred during ingest-structured: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to ingest structured data: {e}")
