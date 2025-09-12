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
from app.nlp import segmenter

logger = logging.getLogger(__name__)

router = APIRouter()

class NlpRequest(BaseModel):
    text: str

def _pair_masked_ids_to_persons(text: str, persons: List[Dict[str, Any]], masked_ids: List[str]) -> List[Dict[str, Any]]:
    """
    Verilen ilân metni içinde, her PER* kişi için en yakın maskeli kimliği (aynı satır veya takip eden 1-3 satır) eşler.
    Eşleşen kişi sözlüklerine 'masked_ids' (string) alanı eklenir. Eşleşme bulunamazsa alan eklenmez.
    """
    try:
        if not text or not persons or not masked_ids:
            return persons
        lines = text.splitlines()
        # Maskeli kimliklerin satır indeksleri
        id_positions: List[tuple[str, int]] = []
        for mi in masked_ids:
            token = (mi or "").strip()
            if not token:
                continue
            for idx, raw in enumerate(lines):
                if token in raw:
                    id_positions.append((token, idx))
                    break
        if not id_positions:
            return persons

        # Kişileri zenginleştir (mevcut masked_ids korunur, sadece eksikler doldurulur)
        enriched: List[Dict[str, Any]] = []
        assigned_person_idxs: set[int] = set()
        # Önce mevcut masked_ids içerenleri doğrudan taşı ve işaretle
        for pi, p in enumerate(persons):
            label = (p.get("label") or "").upper()
            masked_present = bool((p.get("masked_ids") or "").strip())
            if label.startswith("PER") and masked_present:
                enriched.append(dict(p))
                assigned_person_idxs.add(pi)

        # Prefiks varyantlarını oluşturmak için yardımcı
        def _name_variants(n: str) -> List[str]:
            base = (n or "").strip().lower()
            if not base:
                return []
            prefixes = [
                "",
                "t.c. ", "tc ", "t c ",
                "t.a. ", "ta ",
                "sn. ", "sayin ",
                "bay ", "bayan ",
            ]
            return [p + base for p in prefixes]

        for (mid, i) in id_positions:
            # aynı satır ve takip eden 1-3 satır içinde ara
            win_lines = lines[i:i+4]
            window_text = "\n".join(win_lines).lower()
            # en erken geçen ve henüz masked_id set edilmemiş kişi atanır
            for pi, p in enumerate(persons):
                if pi in assigned_person_idxs:
                    continue
                label = (p.get("label") or "").upper()
                if not label.startswith("PER"):
                    continue
                name = (p.get("text") or "").strip()
                if not name:
                    continue
                variants = _name_variants(name)
                if any(v and v in window_text for v in variants):
                    p2 = dict(p)
                    p2.setdefault("masked_ids", mid)
                    enriched.append(p2)
                    assigned_person_idxs.add(pi)
                    break
        # Eşleşmeyenler olduğu gibi eklenir
        for pi, p in enumerate(persons):
            if pi not in assigned_person_idxs:
                enriched.append(p)
        # Basit geri dönüş: tek kişi ve tek id varsa ve atanmamışsa ata
        if len(masked_ids) == 1:
            only_id = masked_ids[0]
            for e in enriched:
                if (e.get("label") or "").upper().startswith("PER") and not (e.get("masked_ids") or "").strip():
                    e["masked_ids"] = only_id
                    break
        return enriched
    except Exception:
        # Herhangi bir hata durumunda orijinal listeyi döndür (dayanıklılık)
        return persons

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


@router.post("/parse-announcements-minimal", response_model=List[Dict[str, Any]])
async def parse_text_minimal(
    request_body: NlpRequest
):
    """
    OCR metnini ilânlara böler ve her ilân için SADECE aşağıdaki alanları Türkçe anahtarlarla döner:
      - "müdürlük" (kaynak: sicil_office_header)
      - "ilan Sira No" (kaynak: ilan_sira_no[0] varsa; yoksa sicil_dosya_no)
      - "Mersis No" (kaynak: mersis_no)
      - "Ticaret Sicil/Dosya No" (kaynak: sicil_dosya_no)
      - "Ticaret Unvan" (kaynak: trade_name)
      - "Adres" (kaynak: addresses)
      - "Eski Adres" (opsiyonel; kaynak: old_addresses)
      - "Tescil Edilen Hususlar" (kaynak: hususlar)
      - "Tescile Delil Olan Belgeler" (kaynak: belgeler)
      - "Kişiler" (kaynak: persons)
      - "Maskeli Kimlik Numaraları" (kaynak: masked_ids)
      - "orjinal metin" (kaynak: original_text)

    Swift istemcisi ham JSON olarak bu minimal çıktıyı gösterir.
    """
    logger.info("Received request for MINIMAL NLP parsing (TR). text_len=%s", len(request_body.text or ""))
    if not request_body.text or not request_body.text.strip():
        raise HTTPException(status_code=400, detail="Text content cannot be empty.")

    try:
        if nlp_service.nlp_model is None:
            nlp_service.load_spacy_model()

        items = nlp_service.parse_multiple_announcements(request_body.text)
        minimal_list: List[Dict[str, Any]] = []
        for it in items:
            ilan_sira = None
            val = it.get("ilan_sira_no")
            if isinstance(val, list) and val:
                ilan_sira = val[0]
            elif isinstance(val, str) and val.strip():
                ilan_sira = val.strip()
            else:
                # Yedek: sicil_dosya_no
                sd = it.get("sicil_dosya_no")
                if isinstance(sd, str) and sd.strip():
                    ilan_sira = sd.strip()

            enriched_persons = _pair_masked_ids_to_persons(
                it.get("original_text") or "",
                it.get("persons") or [],
                it.get("masked_ids") or [],
            )

            minimal = {
                "müdürlük": it.get("sicil_office_header"),
                "ilan Sira No": ilan_sira,
                "Mersis No": it.get("mersis_no"),
                "Ticaret Sicil/Dosya No": it.get("sicil_dosya_no"),
                "Ticaret Unvan": it.get("trade_name"),
                "Adres": it.get("addresses") or [],
                "Tescil Edilen Hususlar": it.get("hususlar") or [],
                "Tescile Delil Olan Belgeler": it.get("belgeler"),
                "Kişiler": enriched_persons,
                "Maskeli Kimlik Numaraları": it.get("masked_ids") or [],
                "orjinal metin": it.get("original_text"),
            }
            if it.get("old_addresses"):
                minimal["Eski Adres"] = it.get("old_addresses")
            minimal_list.append(minimal)

        logger.info("Successfully built minimal announcements. count=%d", len(minimal_list))
        return minimal_list
    except Exception as e:
        logger.error(f"An error occurred during MINIMAL NLP parsing: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to build minimal output: {e}")


@router.post("/parse-announcements-minimal-single", response_model=Dict[str, Any])
async def parse_text_minimal_single(
    request_body: NlpRequest,
    index: int = 1,
):
    """
    OCR metnini ilânlara böler ve **tek** bir ilân için SADECE aşağıdaki alanları
    Türkçe anahtarlarla döner (dizi yerine doğrudan sözlük döner):
      - "müdürlük" (kaynak: sicil_office_header)
      - "ilan Sira No" (kaynak: ilan_sira_no[0] varsa; yoksa sicil_dosya_no)
      - "Mersis No" (kaynak: mersis_no)
      - "Ticaret Sicil/Dosya No" (kaynak: sicil_dosya_no)
      - "Ticaret Unvan" (kaynak: trade_name)
      - "Adres" (kaynak: addresses)
      - "Eski Adres" (opsiyonel; kaynak: old_addresses)
      - "Tescil Edilen Hususlar" (kaynak: hususlar)
      - "Tescile Delil Olan Belgeler" (kaynak: belgeler)
      - "Kisiler" (kaynak: persons)
      - "Maskeli Kimlik Numaralari" (kaynak: masked_ids)
      - "orjinal metin" (kaynak: original_text)

    Parametreler:
      - index: 1-tabancı ilan index'i. Varsayılan 1. Aralık dışı ise 404 döner.
    """
    logger.info(
        "Received request for MINIMAL NLP parsing SINGLE (TR). text_len=%s index=%s",
        len(request_body.text or ""), index,
    )
    if not request_body.text or not request_body.text.strip():
        raise HTTPException(status_code=400, detail="Text content cannot be empty.")

    try:
        if nlp_service.nlp_model is None:
            nlp_service.load_spacy_model()

        items = nlp_service.parse_multiple_announcements(request_body.text)
        minimal_list: List[Dict[str, Any]] = []
        for it in items:
            ilan_sira = None
            val = it.get("ilan_sira_no")
            if isinstance(val, list) and val:
                ilan_sira = val[0]
            elif isinstance(val, str) and val.strip():
                ilan_sira = val.strip()
            else:
                sd = it.get("sicil_dosya_no")
                if isinstance(sd, str) and sd.strip():
                    ilan_sira = sd.strip()

            enriched_persons = _pair_masked_ids_to_persons(
                it.get("original_text") or "",
                it.get("persons") or [],
                it.get("masked_ids") or [],
            )

            minimal = {
                "müdürlük": it.get("sicil_office_header"),
                "ilan Sira No": ilan_sira,
                "Mersis No": it.get("mersis_no"),
                "Ticaret Sicil/Dosya No": it.get("sicil_dosya_no"),
                "Ticaret Unvan": it.get("trade_name"),
                "Adres": it.get("addresses") or [],
                "Tescil Edilen Hususlar": it.get("hususlar") or [],
                "Tescile Delil Olan Belgeler": it.get("belgeler"),
                "Kişiler": enriched_persons,
                "Maskeli Kimlik Numaraları": it.get("masked_ids") or [],
                "orjinal metin": it.get("original_text"),
            }
            # "Eski Adres" alanı opsiyoneldir; yalnızca veri varsa ekleyelim (minimal çoklu uç noktası ile uyumlu)
            if it.get("old_addresses"):
                minimal["Eski Adres"] = it.get("old_addresses")
            minimal_list.append(minimal)

        if not minimal_list:
            raise HTTPException(status_code=404, detail="No announcements were parsed from the provided text.")

        # 1-tabanlı index'i 0-tabanlıya çevir
        sel = max(1, int(index)) - 1
        if sel < 0 or sel >= len(minimal_list):
            raise HTTPException(status_code=404, detail=f"Index out of range. Provided index={index}, available=1..{len(minimal_list)}")

        logger.info("Successfully built minimal SINGLE announcement. selected=%d total=%d", sel + 1, len(minimal_list))
        return minimal_list[sel]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"An error occurred during MINIMAL NLP parsing SINGLE: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to build minimal single output: {e}")


@router.post("/parse-structured", response_model=Dict[str, Any])
async def parse_structured(
    request_body: NlpRequest
):
    """
    Regex tabanlı segmenter ile tek bir metni ayrıştırır ve ayrıntılı JSON döner.
    Swift gibi istemcilerin UI'da doğrudan gösterebileceği yapıdadır.
    """
    logger.info("Received request for SEGMENTER parsing.")
    if not request_body.text or not request_body.text.strip():
        raise HTTPException(status_code=400, detail="Text content cannot be empty.")

    try:
        result = segmenter.parse_document(request_body.text)
        logger.info("Successfully parsed with segmenter.")
        return result
    except Exception as e:
        logger.error(f"An error occurred during SEGMENTER parsing: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to parse with segmenter: {e}")


@router.post("/parse-structured-announcements", response_model=List[Dict[str, Any]])
async def parse_structured_multiple(
    request_body: NlpRequest
):
    """
    OCR metnini ilânlara böler ve her ilânı regex tabanlı segmenter ile ayrıştırır.
    Her ilân için: index, offsets, original_text, sicil_office_header ve parsed alanları döner.
    """
    logger.info("Received request for SEGMENTER MULTI parsing. text_len=%s", len(request_body.text or ""))
    if not request_body.text or not request_body.text.strip():
        raise HTTPException(status_code=400, detail="Text content cannot be empty.")

    try:
        segments = nlp_service.split_announcements_with_offsets(request_body.text)
        out: List[Dict[str, Any]] = []
        for idx, segobj in enumerate(segments, start=1):
            seg_text = segobj.get("text") or ""
            seg_raw = segobj.get("raw_text") or seg_text
            parsed = segmenter.parse_document(seg_text)
            # Başlık satır(lar)ını pratikçe oluştur (ilk 3 dolu satır)
            header_lines: List[str] = []
            for ln in seg_text.splitlines():
                s = ln.strip()
                if not s:
                    continue
                header_lines.append(s)
                if len(header_lines) >= 3:
                    break
            header = " ".join(header_lines).strip()

            out.append({
                "index": idx,
                "sicil_office_header": header,
                "original_text": seg_raw,
                "start_offset": segobj.get("start"),
                "end_offset": segobj.get("end"),
                "parsed": parsed,
            })
        logger.info("Successfully parsed structured announcements. count=%d", len(out))
        return out
    except Exception as e:
        logger.error(f"An error occurred during SEGMENTER MULTI parsing: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to parse structured announcements: {e}")

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
        # result = ingest_service.ingest_companies_and_announcements(parsed_list, db)  # TEMP: disabled
        result = {
            "inserted": 0,
            "updated": 0,
            "skipped": 0,
            "office_mismatch": 0,
            "errors": [],
            "announcements_created": 0,
            "ocr_results_created": 0,
            "links": [],
        }
        payload = {
            "parsed_count": len(parsed_list),
            **result,
        }
        logger.info("Ingest disabled. parsed=%d", len(parsed_list))
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

        # result = ingest_service.ingest_companies_and_announcements(parsed_list, db)  # TEMP: disabled
        result = {
            "inserted": 0,
            "updated": 0,
            "skipped": 0,
            "office_mismatch": 0,
            "errors": [],
            "announcements_created": 0,
            "ocr_results_created": 0,
            "links": [],
        }

        # Ingest başarıysa ve istek silme istiyorsa, Supabase Storage'dan dosyayı sil ve DB'yi güncelle (TEMP disabled)
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
