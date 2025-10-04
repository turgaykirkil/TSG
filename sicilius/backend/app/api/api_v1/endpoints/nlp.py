import logging
import uuid
import hashlib
import re
import time
from datetime import datetime
from fastapi import APIRouter, Body, HTTPException, Depends, Query, BackgroundTasks
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

# Background tasks for ingest/link updates
def _link_companies_for_rpc_task(supabase: Client, items: List[Dict[str, Any]], publication_date: Any, issue_number: Any, page_number: Any) -> None:
    try:
        linked = 0
        for it in items:
            cid = _find_or_create_company(
                supabase,
                it.get("sicil_office_header"),
                it.get("sicil_dosya_no") or it.get("registration_number"),
                it.get("trade_name"),
                it.get("addresses"),
                it.get("mersis_no"),
            )
            if cid:
                idx = it.get("index")
                if idx is not None:
                    supabase.table("ocr_results").update({"company_id": cid}).match({
                        "publication_date": publication_date,
                        "issue_number": int(issue_number),
                        "page_number": int(page_number),
                        "item_index": int(idx),
                    }).execute()
                    linked += 1
        if linked:
            logger.info("parse-announcements company links updated via RPC path (background): %d", linked)
    except Exception:
        logger.warning("parse-announcements company link (RPC path, background) failed", exc_info=True)


def _fallback_sidewrite_task(supabase: Client, parsed_list: List[Dict[str, Any]]) -> None:
    try:
        rows: List[Dict[str, Any]] = []
        link_intents: List[Dict[str, Any]] = []
        errors_local: List[Dict[str, Any]] = []
        for it in parsed_list:
            cid = _find_or_create_company(
                supabase,
                it.get("sicil_office_header"),
                it.get("sicil_dosya_no") or it.get("registration_number"),
                it.get("trade_name"),
                it.get("addresses"),
                it.get("mersis_no"),
            )
            orig_text = it.get("original_text") or ""
            h = hashlib.sha256(orig_text.encode("utf-8")).hexdigest() if isinstance(orig_text, str) else None
            try:
                _len_txt = len(orig_text) if isinstance(orig_text, str) else 0
            except Exception:
                _len_txt = 0
            logger.debug("parse-announcements fallback(bg): item_index=%s len=%s hash=%s", it.get("index"), _len_txt, h)
            rows.append({
                "publication_date": None,
                "issue_number": None,
                "page_number": None,
                "pdf_url": None,
                "pdf_page_count": None,
                "company_id": cid,
                "content_sha256": h,
                "sicil_office_header": it.get("sicil_office_header"),
                "sicil_dosya_no": it.get("sicil_dosya_no"),
                "mersis_no": it.get("mersis_no"),
                "trade_name": it.get("trade_name"),
                "old_trade_name": it.get("old_trade_name"),
                "addresses": it.get("addresses"),
                "old_addresses": it.get("old_addresses"),
                "persons": it.get("persons"),
                "masked_ids": it.get("masked_ids"),
                "hususlar": it.get("hususlar"),
                "belgeler": it.get("belgeler"),
                "type": it.get("type"),
                "item_index": it.get("index"),
                "original_text": it.get("original_text"),
                "start_offset": it.get("start_offset"),
                "end_offset": it.get("end_offset"),
                "is_derived": it.get("is_derived"),
                "derived_from_index": it.get("derived_from_index"),
                "ilan_sira_no": it.get("ilan_sira_no"),
                "status": "completed",
            })
            if h and cid:
                link_intents.append({"content_sha256": h, "company_id": cid})
        if rows:
            def is_transient(em: str) -> bool:
                return ("<!DOCTYPE html>" in em or "Worker threw exception" in em or "JSON could not be generated" in em or "json_invalid" in em or "connection reset by peer" in em or "57014" in em or "1101" in em)
            def _upsert_chunked_local(all_rows: List[Dict[str, Any]], chunk_size: int = 10) -> int:
                def upsert_chunk(chunk: List[Dict[str, Any]]) -> int:
                    if not chunk:
                        return 0
                    try:
                        res = supabase.table("ocr_results").upsert(chunk, on_conflict="content_sha256").execute()
                        return len(getattr(res, "data", None) or [])
                    except Exception as e:
                        if len(chunk) > 1:
                            mid = len(chunk) // 2
                            return upsert_chunk(chunk[:mid]) + upsert_chunk(chunk[mid:])
                        item = chunk[0]
                        em = str(e)
                        for attempt in range(3):
                            try:
                                time.sleep(0.25 * (attempt + 1))
                                res = supabase.table("ocr_results").upsert([item], on_conflict="content_sha256").execute()
                                return len(getattr(res, "data", None) or [])
                            except Exception as e2:
                                em2 = str(e2)
                                if is_transient(em2) and attempt < 2:
                                    continue
                                else:
                                    break
                        try:
                            errors_local.append({"index": item.get("item_index"), "hash": item.get("content_sha256"), "error": em[:200],})
                        except Exception:
                            pass
                        return 0
                total = 0
                for i in range(0, len(all_rows), chunk_size):
                    total += upsert_chunk(all_rows[i:i + chunk_size])
                return total
            inserted = _upsert_chunked_local(rows, chunk_size=10)
            logger.info("parse-announcements side-write (background) completed. inserted=%d errors=%d", inserted, len(errors_local))
            for li in link_intents:
                try:
                    supabase.table("ocr_results").update({"company_id": li["company_id"]}).eq("content_sha256", li["content_sha256"]).is_("company_id", "null").execute()
                except Exception:
                    logger.warning("post-upsert company link by content_sha256 (background) failed", exc_info=True)
    except Exception as e:
        logger.warning("parse-announcements side-write (background) failed: %s", e, exc_info=True)

class NlpRequest(BaseModel):
    text: str

def _to_ascii_upper(s: str) -> str:
    """Türkçe büyük harfleri ASCII üst sürüme yakınsar: İ->I, I->I, Ş->S, Ğ->G, Ü->U, Ö->O, Ç->C.
    OCR toleransı için yeterli. Boşsa boş döner."""
    if not isinstance(s, str):
        return ""
    t = s.upper()
    t = (
        t.replace("İ", "I").replace("I", "I")
        .replace("Ş", "S").replace("Ğ", "G")
        .replace("Ü", "U").replace("Ö", "O").replace("Ç", "C")
    )
    # Bazı OCR çıktılarında tek tırnak benzeri karakterler farklı olabilir; normalize edelim
    t = t.replace("’", "'").replace("`", "'")
    return t

_TC_PREFIX_RE = re.compile(r"^\s*T\s*\.?\s*C\s*\.?\s+", re.IGNORECASE)
_SUFFIX_RE = re.compile(
    #  ...TICARET [SICILI] [MUDURLUGU] ['NDEN]
    r"\s+(TICARET(?:\s+SICIL[Iİ])?(?:\s+M[UÜ]D[UÜ]RL[UÜ][GĞ][UÜ])?(?:'?NDEN)?)\s*$",
    re.IGNORECASE,
)

def _collapse_spaced_letters(prefix_tokens: list[str]) -> str:
    """Öndeki tek harfli tokenları bitişik hale getir (örn. I Z M I R -> IZMIR).
    İlk birden fazla tek-harf gruplaşmasını destekler; karmaşık durumlarda güvenli şekilde geriye döner."""
    buf: list[str] = []
    for tok in prefix_tokens:
        if len(tok) == 1 and tok.isalpha():
            buf.append(tok)
        else:
            break
    if len(buf) >= 2:
        return "".join(buf)
    return ""

def _normalize_office_first(header: Optional[str]) -> Optional[str]:
    """Sicil müdürlüğü başlığından ilk kelimeyi OCR toleranslı çıkar.
    Ör: "T.C. IZMIR TICARET SICILI MUDURLUGU'NDEN" -> "IZMIR"."""
    if not header or not isinstance(header, str):
        return None
    h = _to_ascii_upper(header)
    h = _TC_PREFIX_RE.sub("", h)
    h = _SUFFIX_RE.sub("", h)
    # Noktalama/çoklu boşluk sadeleştirme
    h2 = re.sub(r"[^A-Z0-9ÇĞİÖŞÜ' ]+", " ", h)
    h2 = re.sub(r"\s+", " ", h2).strip()
    if not h2:
        return None
    toks = h2.split(" ")
    if not toks:
        return None
    # Başta tek harfli tokenlar birbirine yapıştırılmış olabilir
    collapsed = _collapse_spaced_letters(toks[:8])  # makul pencere
    if collapsed:
        return collapsed
    return toks[0]

def _normalize_sicil_no_digits(no: Optional[str]) -> Optional[str]:
    if not no or not isinstance(no, str):
        return None
    digits = re.sub(r"[^0-9]", "", no)
    return digits or None

def _canonicalize_sicil_no(no: Optional[str]) -> Optional[str]:
    """Sicil/Dosya no'yu STRING olarak kanonik hale getirir.
    - Harflerin hepsi upper (TR toleranslı _to_ascii_upper ile)
    - Üniversal tire/slash normalizasyonu: – — − -> -, tam genişlikli slash -> /
    - Ayırıcıların etrafındaki boşlukları kaldırır: ' - ' -> '-', ' / ' -> '/'
    - Birden çok boşluğu tek boşluğa indirger
    - Nokta, gereksiz unicode boşlukları sadeleştirilir
    - İçerik (harf/rakam/separatör) korunur; RAKAMLARA indirgeme yapılmaz
    """
    if not no or not isinstance(no, str):
        return None
    t = _to_ascii_upper(no.strip())
    if not t:
        return None
    # Unicode dash/slash varyantlarını normalleştir
    t = t.replace("–", "-").replace("—", "-").replace("−", "-")
    t = t.replace("／", "/")
    # Ayırıcı kenar boşluklarını kaldır
    t = re.sub(r"\s*([\-/])\s*", r"\1", t)
    # Noktalama ve fazla boşluk sadeleştirme (ayırıcılar korunur)
    t = re.sub(r"\s+", " ", t).strip()
    return t or None

def _sicil_ilike_pattern_from_canonical(canon: str) -> str:
    """DB 'ilike' aramasında tolerans için kanonik stringten pattern üretir.
    Ayırıcıları ve boşlukları '%' jokerine çevirerek varyasyonlara tolerans sağlar."""
    p = canon.replace("-", "%").replace("/", "%").replace(" ", "%")
    p = re.sub(r"%+", "%", p)
    return p

def _find_or_create_company(
    supabase: Client,
    office_header: Optional[str],
    sicil_no_raw: Optional[str],
    trade_name: Optional[str],
    addresses: Optional[List[Any]],
    mersis_no: Optional[str] = None,
) -> Optional[str]:
    """Şirketi bulur ya da oluşturur ve id döner.
    EŞLEŞTİRME SADECE: (office_first + sicil_digits) ile yapılır. (Kullanıcı talebi.)
    MERSIS yalnızca insert sırasında saklanır; eşleştirmede KULLANILMAZ.
    Hata/eksikte None döner.
    """
    try:
        # 0) Adres ilk satır
        addr0 = None
        if isinstance(addresses, list) and addresses:
            a0 = addresses[0]
            if isinstance(a0, str):
                addr0 = a0
        # 1) Ofis+sicil (string) ile dene (TEK eşleştirme yöntemi)
        office_first = _normalize_office_first(office_header)
        sicil_canon = _canonicalize_sicil_no(sicil_no_raw)
        if not office_first or not sicil_canon:
            return None
        like_pat = _sicil_ilike_pattern_from_canonical(sicil_canon)
        # Cloudflare/edge kaynaklı arızi HTML/bağlantı hataları için küçük retry
        sel = None
        for attempt in range(3):
            try:
                sel = (
                    supabase
                    .table("companies")
                    .select("id, sicil_mudurluk, sicil_no")
                    .ilike("sicil_no", f"%{like_pat}%")
                    .limit(100)
                    .execute()
                )
                break
            except Exception as e:
                em = str(e)
                transient = (
                    "<!DOCTYPE html>" in em or
                    "Worker threw exception" in em or
                    "JSON could not be generated" in em or
                    "json_invalid" in em or
                    "connection reset by peer" in em
                )
                if transient and attempt < 2:
                    time.sleep(0.2 * (attempt + 1))
                    continue
                raise
        candidates = getattr(sel, "data", None) or []
        for c in candidates:
            cm = _normalize_office_first(c.get("sicil_mudurluk"))
            cc = _canonicalize_sicil_no(c.get("sicil_no"))
            if cm and cc and cm == office_first and cc == sicil_canon:
                return c.get("id")
        # 2) Bulunamadı; oluştur
        insert_obj: Dict[str, Any] = {
            "id": str(uuid.uuid4()),
            "sicil_mudurluk": office_first or None,
            "sicil_no": sicil_no_raw,
            "unvan": trade_name,
            "address": addr0,
        }
        if isinstance(mersis_no, str) and mersis_no.strip():
            insert_obj["mersis_number"] = mersis_no.strip()
        # Insert için de aynı transient hata toleransı
        ins = None
        for attempt in range(3):
            try:
                ins = supabase.table("companies").insert(insert_obj).execute()
                break
            except Exception as e:
                em = str(e)
                transient = (
                    "<!DOCTYPE html>" in em or
                    "Worker threw exception" in em or
                    "JSON could not be generated" in em or
                    "json_invalid" in em or
                    "connection reset by peer" in em
                )
                if transient and attempt < 2:
                    time.sleep(0.2 * (attempt + 1))
                    continue
                raise
        data = getattr(ins, "data", None) or []
        if data and isinstance(data, list):
            rid = data[0].get("id")
            if rid:
                return rid
        # Insert çağrısı istisnasız döndüyse ve data gelmediyse, ürettiğimiz UUID'yi döndür (idempotent bağlama için yeterli)
        return insert_obj["id"]
    except Exception:
        # Gürültüyü azalt: terminale ERROR/stack trace basma; veri kaybı yok, None dönüyoruz
        logger.debug("_find_or_create_company suppressed transient error", exc_info=False)
        return None

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
    request_body: NlpRequest,
    background_tasks: BackgroundTasks,
    supabase: Client = Depends(get_supabase_client),
    announcement_id: Optional[str] = Query(None, description="If provided, results will be ingested for this announcement"),
    pdf_page_count: Optional[int] = Query(None, description="Optional PDF total page count for dedupe"),
    skip_ingest: bool = Query(True, description="If true (default), do not persist here; parse-only response.")
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

        # Eğer sadece parse isteniyorsa (skip_ingest=True) ve announcement_id verilmemişse hızlı dönüş yap
        # Eğer sadece parse isteniyorsa (skip_ingest=True) ve announcement_id verilmemişse hızlı dönüş yap
        if not announcement_id:
            logger.info("parse-announcements: scheduling fallback side-write in background (no announcement_id)")
            background_tasks.add_task(_fallback_sidewrite_task, supabase, parsed_list)
            return parsed_list

        # If client provided announcement_id, resolve meta and do RPC ingest with meta
        if announcement_id:
            try:
                sel = (
                    supabase
                    .table("announcements")
                    .select("id, publication_date, issue_number, page_number, pdf_url")
                    .eq("id", announcement_id)
                    .limit(1)
                    .execute()
                )
                rows_meta = getattr(sel, "data", None) or []
                if rows_meta:
                    meta = rows_meta[0]
                    publication_date = meta.get("publication_date")
                    issue_number = meta.get("issue_number")
                    page_number = meta.get("page_number")
                    pdf_url = meta.get("pdf_url")
                    if publication_date is not None and issue_number is not None and page_number is not None:
                        rpc_params = {
                            "_publication_date": publication_date,
                            "_issue_number": int(issue_number),
                            "_page_number": int(page_number),
                            "_pdf_url": pdf_url,
                            "_raw_text": request_body.text,
                            "_structured": {"items": parsed_list},
                            "_company_id": None,
                            "_status": "completed",
                            "_pdf_page_count": int(pdf_page_count) if pdf_page_count is not None else None,
                        }
                        rpc_res = supabase.rpc("fn_ingest_ocr_by_ann_key", rpc_params).execute()
                        logger.info("parse-announcements RPC ingest done. rows=%s", len(getattr(rpc_res, "data", []) or []))
                        # Schedule background company link updates instead of blocking here
                        background_tasks.add_task(_link_companies_for_rpc_task, supabase, parsed_list, publication_date, issue_number, page_number)
                        logger.info("parse-announcements: scheduled company link updates via RPC path (background)")
                        return parsed_list
                    else:
                        logger.warning("parse-announcements: announcement meta incomplete; falling back to content hash upsert")
                else:
                    logger.warning("parse-announcements: announcement_id not found; falling back to content hash upsert")
            except Exception as e:
                logger.warning("parse-announcements RPC ingest failed: %s", e, exc_info=True)

        # Schedule background fallback side-write instead of blocking here (meta missing or RPC failed)
        background_tasks.add_task(_fallback_sidewrite_task, supabase, parsed_list)
        logger.info("parse-announcements: scheduled fallback side-write (background)")
        return parsed_list

        # Fallback: Side-write to Supabase (content hash upsert). Non-blocking best-effort.
        try:
            rows: List[Dict[str, Any]] = []
            link_intents: List[Dict[str, Any]] = []
            errors_local: List[Dict[str, Any]] = []
            for it in parsed_list:
                cid = _find_or_create_company(
                    supabase,
                    it.get("sicil_office_header"),
                    it.get("sicil_dosya_no") or it.get("registration_number"),
                    it.get("trade_name"),
                    it.get("addresses"),
                    it.get("mersis_no"),
                )
                orig_text = it.get("original_text") or ""
                h = hashlib.sha256(orig_text.encode("utf-8")).hexdigest() if isinstance(orig_text, str) else None
                # Teşhis için DEBUG: index, metin uzunluğu, hash
                try:
                    _len_txt = len(orig_text) if isinstance(orig_text, str) else 0
                except Exception:
                    _len_txt = 0
                logger.debug("parse-announcements fallback: item_index=%s len=%s hash=%s", it.get("index"), _len_txt, h)
                rows.append({
                    "publication_date": None,
                    "issue_number": None,
                    "page_number": None,
                    "pdf_url": None,
                    "pdf_page_count": None,
                    "company_id": cid,
                    "content_sha256": h,
                    "sicil_office_header": it.get("sicil_office_header"),
                    "sicil_dosya_no": it.get("sicil_dosya_no"),
                    "mersis_no": it.get("mersis_no"),
                    "trade_name": it.get("trade_name"),
                    "old_trade_name": it.get("old_trade_name"),
                    "addresses": it.get("addresses"),
                    "old_addresses": it.get("old_addresses"),
                    "persons": it.get("persons"),
                    "masked_ids": it.get("masked_ids"),
                    "hususlar": it.get("hususlar"),
                    "belgeler": it.get("belgeler"),
                    "type": it.get("type"),
                    "item_index": it.get("index"),
                    "original_text": it.get("original_text"),
                    "start_offset": it.get("start_offset"),
                    "end_offset": it.get("end_offset"),
                    "is_derived": it.get("is_derived"),
                    "derived_from_index": it.get("derived_from_index"),
                    "ilan_sira_no": it.get("ilan_sira_no"),
                    "status": "completed",
                })
                if h and cid:
                    link_intents.append({"content_sha256": h, "company_id": cid})
            if rows:
                # Chunk'lı upsert ve tekil retry/backoff
                def is_transient(em: str) -> bool:
                    return (
                        "<!DOCTYPE html>" in em or
                        "Worker threw exception" in em or
                        "JSON could not be generated" in em or
                        "json_invalid" in em or
                        "connection reset by peer" in em or
                        "57014" in em or
                        "1101" in em
                    )

                def _upsert_chunked_local(all_rows: List[Dict[str, Any]], chunk_size: int = 10) -> int:
                    def upsert_chunk(chunk: List[Dict[str, Any]]) -> int:
                        if not chunk:
                            return 0
                        try:
                            res = supabase.table("ocr_results").upsert(chunk, on_conflict="content_sha256").execute()
                            return len(getattr(res, "data", None) or [])
                        except Exception as e:
                            if len(chunk) > 1:
                                mid = len(chunk) // 2
                                return upsert_chunk(chunk[:mid]) + upsert_chunk(chunk[mid:])
                            # Tekil retry/backoff
                            item = chunk[0]
                            em = str(e)
                            for attempt in range(3):
                                try:
                                    time.sleep(0.25 * (attempt + 1))
                                    res = supabase.table("ocr_results").upsert([item], on_conflict="content_sha256").execute()
                                    return len(getattr(res, "data", None) or [])
                                except Exception as e2:
                                    em2 = str(e2)
                                    if is_transient(em2) and attempt < 2:
                                        continue
                                    else:
                                        break
                            # Başarısız tekil kayıt: errors[] topla
                            try:
                                errors_local.append({
                                    "index": item.get("item_index"),
                                    "hash": item.get("content_sha256"),
                                    "error": em[:200],
                                })
                            except Exception:
                                pass
                            return 0

                    total = 0
                    for i in range(0, len(all_rows), chunk_size):
                        total += upsert_chunk(all_rows[i:i + chunk_size])
                    return total

                inserted = _upsert_chunked_local(rows, chunk_size=10)
                logger.info("parse-announcements side-write completed. inserted=%d errors=%d", inserted, len(errors_local))
                # Güvence: company_id boş kalan satırlar için ikinci tur link
                for li in link_intents:
                    try:
                        supabase.table("ocr_results").update({"company_id": li["company_id"]}).eq("content_sha256", li["content_sha256"]).is_("company_id", "null").execute()
                    except Exception:
                        logger.warning("post-upsert company link by content_sha256 failed", exc_info=True)
        except Exception as e:
            logger.warning("parse-announcements side-write failed: %s", e, exc_info=True)

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
        # Supabase'e idempotent ingest (sayfa bazında per-item)
        # Gerekli meta alanları: publication_date, issue_number, page_number (ve opsiyonel pdf_url, pdf_page_count)
        publication_date = None
        issue_number = None
        page_number = None
        pdf_url = None
        pdf_page_count = None

        if isinstance(request_body, dict):
            publication_date = request_body.get("publication_date")
            issue_number = request_body.get("issue_number")
            page_number = request_body.get("page_number")
            pdf_url = request_body.get("pdf_url")
            pdf_page_count = request_body.get("pdf_page_count")

        use_rpc = True
        if not publication_date or issue_number is None or page_number is None:
            # Meta eksikse RPC yerine doğrudan upsert fallback'ini kullanacağız
            use_rpc = False

        # raw_text: varsa üst seviyeden, yoksa item'ların original_text'lerinin birleştirilmiş hali
        raw_text: Optional[str] = None
        if not raw_text:
            try:
                pieces = []
                for it in parsed_list:
                    t = it.get("original_text")
                    if isinstance(t, str) and t.strip():
                        pieces.append(t.strip())
                raw_text = "\n\n".join(pieces) if pieces else None
            except Exception:
                raw_text = None

        inserted = 0
        updated = 0
        rpc_data = None
        if use_rpc:
            structured_payload = {"items": parsed_list}
            rpc_params = {
                "_publication_date": publication_date,
                "_issue_number": int(issue_number),
                "_page_number": int(page_number),
                "_pdf_url": pdf_url,
                "_raw_text": raw_text or "",
                "_structured": structured_payload,
                "_company_id": None,
                "_status": "completed",
                "_pdf_page_count": int(pdf_page_count) if pdf_page_count is not None else None,
            }
            rpc_res = supabase.rpc("fn_ingest_ocr_by_ann_key", rpc_params).execute()
            rpc_data = getattr(rpc_res, "data", None)
            if isinstance(rpc_data, list):
                for row in rpc_data:
                    try:
                        if bool(row.get("inserted", True)):
                            inserted += 1
                        else:
                            updated += 1
                    except Exception:
                        inserted += 1
            # RPC sonrası company_id bağlama (per-item)
            try:
                linked = 0
                for it in parsed_list:
                    cid = _find_or_create_company(
                        supabase,
                        it.get("sicil_office_header"),
                        it.get("sicil_dosya_no") or it.get("registration_number"),
                        it.get("trade_name"),
                        it.get("addresses"),
                        it.get("mersis_no"),
                    )
                    if cid:
                        idx = it.get("index")
                        if idx is not None:
                            supabase.table("ocr_results").update({"company_id": cid}).match({
                                "publication_date": publication_date,
                                "issue_number": int(issue_number),
                                "page_number": int(page_number),
                                "item_index": int(idx),
                            }).execute()
                            linked += 1
                if linked:
                    logger.info("ingest-announcements company links updated via RPC path: %d", linked)
            except Exception:
                logger.warning("ingest-announcements company link (RPC path) failed", exc_info=True)
        else:
            # Fallback: Meta yoksa content_sha256 üzerinden idempotent upsert
            rows: list[dict] = []
            link_intents: List[Dict[str, Any]] = []
            for it in parsed_list:
                cid = _find_or_create_company(
                    supabase,
                    it.get("sicil_office_header"),
                    it.get("sicil_dosya_no") or it.get("registration_number"),
                    it.get("trade_name"),
                    it.get("addresses"),
                    it.get("mersis_no"),
                )
                orig_text = it.get("original_text") or ""
                h = hashlib.sha256(orig_text.encode("utf-8")).hexdigest() if isinstance(orig_text, str) else None
                row = {
                    "publication_date": publication_date,
                    "issue_number": issue_number,
                    "page_number": page_number,
                    "pdf_url": pdf_url,
                    "pdf_page_count": pdf_page_count,
                    "company_id": cid,
                    "content_sha256": h,
                    "sicil_office_header": it.get("sicil_office_header"),
                    "sicil_dosya_no": it.get("sicil_dosya_no"),
                    "mersis_no": it.get("mersis_no"),
                    "trade_name": it.get("trade_name"),
                    "old_trade_name": it.get("old_trade_name"),
                    "addresses": it.get("addresses"),
                    "old_addresses": it.get("old_addresses"),
                    "persons": it.get("persons"),
                    "masked_ids": it.get("masked_ids"),
                    "hususlar": it.get("hususlar"),
                    "belgeler": it.get("belgeler"),
                    "type": it.get("type"),
                    "item_index": it.get("index"),
                    "original_text": it.get("original_text"),
                    "start_offset": it.get("start_offset"),
                    "end_offset": it.get("end_offset"),
                    "is_derived": it.get("is_derived"),
                    "derived_from_index": it.get("derived_from_index"),
                    "ilan_sira_no": it.get("ilan_sira_no"),
                    "status": "completed",
                }
                rows.append(row)
                if h and cid:
                    link_intents.append({"content_sha256": h, "company_id": cid})
            up = supabase.table("ocr_results").upsert(rows, on_conflict="content_sha256").execute()
            data = getattr(up, "data", None) or []
            # PostgREST upsert dönen satır sayısına göre sayım
            inserted = len(data)
            # Güvence: company_id boş kalan satırlar için ikinci tur link
            for li in link_intents:
                try:
                    supabase.table("ocr_results").update({"company_id": li["company_id"]}).eq("content_sha256", li["content_sha256"]).is_("company_id", "null").execute()
                except Exception:
                    logger.warning("ingest-announcements post-upsert company link by content_sha256 failed", exc_info=True)
        result = {
            "inserted": inserted,
            "updated": updated,
            "skipped": 0,
            "office_mismatch": 0,
            "errors": [],
            "announcements_created": 0,
            "ocr_results_created": inserted + updated,
            "links": [],
            "rpc": rpc_data,
        }
        payload = {
            "parsed_count": len(parsed_list),
            **result,
        }
        logger.info("Ingest completed. parsed=%d inserted=%d updated=%d", len(parsed_list), inserted, updated)
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

        # Supabase'e idempotent ingest (sayfa bazında per-item)
        publication_date = None
        issue_number = None
        page_number = None
        pdf_url = None
        pdf_page_count = None

        if isinstance(request_body, dict):
            publication_date = request_body.get("publication_date")
            issue_number = request_body.get("issue_number")
            page_number = request_body.get("page_number")
            pdf_url = request_body.get("pdf_url")
            pdf_page_count = request_body.get("pdf_page_count")

        # raw_text: varsa üst seviyeden, yoksa item'ların original_text'lerinin birleştirilmiş hali
        if not raw_text:
            try:
                pieces = []
                for it in parsed_list:
                    t = it.get("original_text")
                    if isinstance(t, str) and t.strip():
                        pieces.append(t.strip())
                raw_text = "\n\n".join(pieces) if pieces else None
            except Exception:
                raw_text = None

        inserted = 0
        updated = 0
        rpc_data = None
        use_rpc = bool(publication_date and issue_number is not None and page_number is not None)
        if use_rpc:
            structured_payload = {"items": parsed_list}
            rpc_params = {
                "_publication_date": publication_date,
                "_issue_number": int(issue_number),
                "_page_number": int(page_number),
                "_pdf_url": pdf_url,
                "_raw_text": raw_text or "",
                "_structured": structured_payload,
                "_company_id": None,
                "_status": "completed",
                "_pdf_page_count": int(pdf_page_count) if pdf_page_count is not None else None,
            }
            rpc_res = supabase.rpc("fn_ingest_ocr_by_ann_key", rpc_params).execute()
            rpc_data = getattr(rpc_res, "data", None)
            if isinstance(rpc_data, list):
                for row in rpc_data:
                    try:
                        if bool(row.get("inserted", True)):
                            inserted += 1
                        else:
                            updated += 1
                    except Exception:
                        inserted += 1
            # RPC sonrası company_id bağlama (meta varsa)
            try:
                if publication_date is not None and issue_number is not None and page_number is not None:
                    linked = 0
                    for it in parsed_list:
                        cid = _find_or_create_company(
                            supabase,
                            it.get("sicil_office_header"),
                            it.get("sicil_dosya_no") or it.get("registration_number"),
                            it.get("trade_name"),
                            it.get("addresses"),
                            it.get("mersis_no"),
                        )
                        if cid:
                            idx = it.get("index")
                            if idx is not None:
                                supabase.table("ocr_results").update({"company_id": cid}).match({
                                    "publication_date": publication_date,
                                    "issue_number": int(issue_number),
                                    "page_number": int(page_number),
                                    "item_index": int(idx),
                                }).execute()
                                linked += 1
                    if linked:
                        logger.info("ingest-structured company links updated via RPC path: %d", linked)
                else:
                    logger.info("ingest-structured RPC: meta keys missing for per-item link; skipping link step")
            except Exception:
                logger.warning("ingest-structured company link (RPC path) failed", exc_info=True)
        else:
            # Fallback: Meta yoksa content_sha256 üzerinden idempotent upsert
            rows: list[dict] = []
            link_intents: List[Dict[str, Any]] = []
            for it in parsed_list:
                cid = _find_or_create_company(
                    supabase,
                    it.get("sicil_office_header"),
                    it.get("sicil_dosya_no") or it.get("registration_number"),
                    it.get("trade_name"),
                    it.get("addresses"),
                    it.get("mersis_no"),
                )
                orig_text = it.get("original_text") or ""
                h = hashlib.sha256(orig_text.encode("utf-8")).hexdigest() if isinstance(orig_text, str) else None
                # Teşhis için DEBUG: index, metin uzunluğu, hash
                try:
                    _len_txt = len(orig_text) if isinstance(orig_text, str) else 0
                except Exception:
                    _len_txt = 0
                logger.debug("ingest-structured fallback: item_index=%s len=%s hash=%s", it.get("index"), _len_txt, h)

                row = {
                    "publication_date": publication_date,
                    "issue_number": issue_number,
                    "page_number": page_number,
                    "pdf_url": pdf_url,
                    "pdf_page_count": pdf_page_count,
                    "company_id": cid,
                    "content_sha256": h,
                    "sicil_office_header": it.get("sicil_office_header"),
                    "sicil_dosya_no": it.get("sicil_dosya_no"),
                    "mersis_no": it.get("mersis_no"),
                    "trade_name": it.get("trade_name"),
                    "old_trade_name": it.get("old_trade_name"),
                    "addresses": it.get("addresses"),
                    "old_addresses": it.get("old_addresses"),
                    "persons": it.get("persons"),
                    "masked_ids": it.get("masked_ids"),
                    "hususlar": it.get("hususlar"),
                    "belgeler": it.get("belgeler"),
                    "type": it.get("type"),
                    "item_index": it.get("index"),
                    "original_text": it.get("original_text"),
                    "start_offset": it.get("start_offset"),
                    "end_offset": it.get("end_offset"),
                    "is_derived": it.get("is_derived"),
                    "derived_from_index": it.get("derived_from_index"),
                    "ilan_sira_no": it.get("ilan_sira_no"),
                    "status": "completed",
                }
                rows.append(row)
                if h and cid:
                    link_intents.append({"content_sha256": h, "company_id": cid})
            # Küçük chunk'larla upsert ve tekil kayıt hatalarında retry/backoff; transient hataları yumuşat
            errors_local: List[Dict[str, Any]] = []
            def _upsert_chunked_local(all_rows: List[Dict[str, Any]], chunk_size: int = 10) -> int:
                def is_transient(em: str) -> bool:
                    return (
                        "<!DOCTYPE html>" in em or
                        "Worker threw exception" in em or
                        "JSON could not be generated" in em or
                        "json_invalid" in em or
                        "connection reset by peer" in em or
                        "57014" in em or  # statement timeout
                        "1101" in em
                    )

                def upsert_chunk(chunk: List[Dict[str, Any]]) -> int:
                    if not chunk:
                        return 0
                    try:
                        res = supabase.table("ocr_results").upsert(chunk, on_conflict="content_sha256").execute()
                        return len(getattr(res, "data", None) or [])
                    except Exception as e:
                        if len(chunk) > 1:
                            mid = len(chunk) // 2
                            return upsert_chunk(chunk[:mid]) + upsert_chunk(chunk[mid:])
                        # Tekil kayıt: retry/backoff uygula
                        item = chunk[0]
                        em = str(e)
                        for attempt in range(3):
                            try:
                                time.sleep(0.25 * (attempt + 1))
                                res = supabase.table("ocr_results").upsert([item], on_conflict="content_sha256").execute()
                                return len(getattr(res, "data", None) or [])
                            except Exception as e2:
                                em2 = str(e2)
                                if is_transient(em2) and attempt < 2:
                                    continue
                                else:
                                    break
                        # Başarısız tekil kayıt: errors[]'e ekle (veri izi kaybolmasın)
                        try:
                            errors_local.append({
                                "index": item.get("item_index"),
                                "hash": item.get("content_sha256"),
                                "error": em[:200],
                            })
                        except Exception:
                            pass
                        return 0

                total = 0
                for i in range(0, len(all_rows), chunk_size):
                    total += upsert_chunk(all_rows[i:i + chunk_size])
                return total

            inserted = _upsert_chunked_local(rows, chunk_size=10)
            # Güvence: company_id boş kalan satırlar için ikinci tur link
            for li in link_intents:
                try:
                    supabase.table("ocr_results").update({"company_id": li["company_id"]}).eq("content_sha256", li["content_sha256"]).is_("company_id", "null").execute()
                except Exception:
                    logger.warning("ingest-structured post-upsert company link by content_sha256 failed", exc_info=True)

        result = {
            "inserted": inserted,
            "updated": updated,
            "skipped": 0,
            "office_mismatch": 0,
            "errors": [],
            "announcements_created": 0,
            "ocr_results_created": inserted + updated,
            "links": [],
            "rpc": rpc_data,
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
            "Ingest-structured finished. parsed=%d inserted=%d updated=%d",
            len(parsed_list), result.get("inserted", 0), result.get("updated", 0)
        )
        return payload
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"An error occurred during ingest-structured: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to ingest structured data: {e}")


# -----------------------------
# New: Centralized OCR check & ingest to Supabase
# -----------------------------

class OcrCheckRequest(BaseModel):
    publication_date: str  # ISO date (YYYY-MM-DD)
    issue_number: int
    page_number: int
    pdf_url: Optional[str] = None
    pdf_page_count: Optional[int] = None


@router.post("/check-ocr", response_model=Dict[str, Any])
async def check_ocr_status(
    req: OcrCheckRequest,
    supabase: Client = Depends(get_supabase_client),
):
    """
    Dedupe kontrol noktası: Aynı sayfa için daha önce OCR/parse yapılmış mı?
    - announcements üzerinden announcement_id bulunur.
    - ocr_results içinde announcement_id'ye göre satır aranır.
    - pdf_page_count sağlandıysa mevcut ile kıyaslanır.
    """
    try:
        # 1) İlan id'sini bul
        params = {
            "_publication_date": req.publication_date,
            "_issue_number": req.issue_number,
            "_page_number": req.page_number,
            "_pdf_url": req.pdf_url,
        }
        ann_res = supabase.rpc("fn_find_announcement_id", params).execute()
        ann_id = (ann_res.data if hasattr(ann_res, "data") else None) or None
        if not ann_id:
            return {
                "found": False,
                "already_processed": False,
                "message": "Announcement not found for given keys.",
            }

        # 2) Var olan OCR sonucu var mı?
        sel = (
            supabase
            .table("ocr_results")
            .select("id, announcement_id, publication_date, issue_number, page_number, pdf_url, pdf_page_count, created_at, updated_at")
            .eq("announcement_id", ann_id)
            .limit(1)
            .execute()
        )
        rows = getattr(sel, "data", None) or []
        if not rows:
            return {
                "found": True,
                "announcement_id": ann_id,
                "already_processed": False,
            }

        row = rows[0]
        page_count_match = True
        if req.pdf_page_count is not None:
            try:
                page_count_match = int(row.get("pdf_page_count") or 0) == int(req.pdf_page_count)
            except Exception:
                page_count_match = False
        return {
            "found": True,
            "announcement_id": ann_id,
            "already_processed": True,
            "page_count_match": page_count_match,
            "existing": row,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error("/check-ocr failed: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail=f"check-ocr failed: {e}")


@router.post("/backfill-company-links", response_model=Dict[str, Any])
async def backfill_company_links(
    limit: int = 50,
    supabase: Client = Depends(get_supabase_client),
):
    """
    Son eklenen (company_id IS NULL) OCR sonuçlarını şirketlerle eşleştirir ve `company_id`'yi günceller.
    MERSIS varsa önce onunla, yoksa ofis-ilk-kelime + sicil-digits ile eşleştirir/oluşturur.
    """
    try:
        sel = (
            supabase
            .table("ocr_results")
            .select("id, sicil_office_header, sicil_dosya_no, mersis_no, trade_name, addresses, publication_date, issue_number, page_number, item_index")
            .is_("company_id", "null")
            .order("created_at", desc=True)
            .limit(int(limit))
            .execute()
        )
        rows = getattr(sel, "data", None) or []
        updated = 0
        created = 0
        for r in rows:
            cid = _find_or_create_company(
                supabase,
                r.get("sicil_office_header"),
                r.get("sicil_dosya_no"),
                r.get("trade_name"),
                r.get("addresses"),
                r.get("mersis_no"),
            )
            if cid:
                supabase.table("ocr_results").update({"company_id": cid}).eq("id", r.get("id")).execute()
                updated += 1
        return {"scanned": len(rows), "company_links_updated": updated, "created_candidates": created}
    except Exception as e:
        logger.error("/backfill-company-links failed: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail=f"backfill-company-links failed: {e}")


class ParseAndIngestRequest(BaseModel):
    text: str
    publication_date: str
    issue_number: int
    page_number: int
    pdf_url: Optional[str] = None
    pdf_page_count: Optional[int] = None


@router.post("/parse-and-ingest", response_model=Dict[str, Any])
async def parse_and_ingest(
    req: ParseAndIngestRequest,
    supabase: Client = Depends(get_supabase_client),
):
    """
    - Aynı sayfa için daha önce kayıt varsa parse yapmaz, mevcut sonucu döner.
    - Yoksa NLP parse çalıştırır, tek KAYIT olarak sayfa bazında Supabase ocr_results'a yazar.
      (structured_data: { items: [...] } formatında saklanır.)
    - İdempotent: DB tarafında announcement_id + content_sha256 ile korunur.
    """
    if not req.text or not req.text.strip():
        raise HTTPException(status_code=400, detail="Text content cannot be empty.")

    try:
        # Önce check
        chk = await check_ocr_status(
            OcrCheckRequest(
                publication_date=req.publication_date,
                issue_number=req.issue_number,
                page_number=req.page_number,
                pdf_url=req.pdf_url,
                pdf_page_count=req.pdf_page_count,
            ),
            supabase=supabase,
        )
        if chk.get("found") and chk.get("already_processed") and chk.get("page_count_match", True):
            return {"skipped": True, "reason": "already_processed", **chk}

        # Parse et
        if nlp_service.nlp_model is None:
            nlp_service.load_spacy_model()
        items = nlp_service.parse_multiple_announcements(req.text)

        structured_payload = {"items": items}
        rpc_params = {
            "_publication_date": req.publication_date,
            "_issue_number": req.issue_number,
            "_page_number": req.page_number,
            "_pdf_url": req.pdf_url,
            "_raw_text": req.text,
            "_structured": structured_payload,
            "_company_id": None,
            "_status": "completed",
            "_pdf_page_count": req.pdf_page_count,
        }
        rpc_res = supabase.rpc("fn_ingest_ocr_by_ann_key", rpc_params).execute()
        data = getattr(rpc_res, "data", None)
        # Company bağlama (per-item) – RPC sonrası
        try:
            linked = 0
            for it in items:
                cid = _find_or_create_company(
                    supabase,
                    it.get("sicil_office_header"),
                    it.get("sicil_dosya_no") or it.get("registration_number"),
                    it.get("trade_name"),
                    it.get("addresses"),
                    it.get("mersis_no"),
                )
                if cid:
                    idx = it.get("index")
                    if idx is not None:
                        supabase.table("ocr_results").update({"company_id": cid}).match({
                            "publication_date": req.publication_date,
                            "issue_number": req.issue_number,
                            "page_number": req.page_number,
                            "item_index": int(idx),
                        }).execute()
                        linked += 1
            if linked:
                logger.info("parse-and-ingest company links updated via RPC path: %d", linked)
        except Exception:
            logger.warning("parse-and-ingest company link (RPC path) failed", exc_info=True)
        return {
            "inserted": True,
            "rpc": data,
            "item_count": len(items),
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error("/parse-and-ingest failed: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail=f"parse-and-ingest failed: {e}")


class ParseForAnnouncementRequest(BaseModel):
    text: str
    announcement_id: str
    pdf_page_count: Optional[int] = None


@router.post("/parse-for-announcement", response_model=Dict[str, Any])
async def parse_for_announcement(
    req: ParseForAnnouncementRequest,
    supabase: Client = Depends(get_supabase_client),
):
    """
    Swift'ten gelen ham metni tek çağrıda parse eder ve verilen announcement_id için
    Supabase'e idempotent olarak per-item ingest yapar. Böylece istemcide meta taşıma
    zorunluluğu olmaz; meta DB'den alınır.
    """
    if not req.text or not req.text.strip():
        raise HTTPException(status_code=400, detail="Text content cannot be empty.")
    try:
        # 1) Meta'yı announcements tablosundan al
        sel = (
            supabase
            .table("announcements")
            .select("id, publication_date, issue_number, page_number, pdf_url")
            .eq("id", req.announcement_id)
            .limit(1)
            .execute()
        )
        rows = getattr(sel, "data", None) or []
        if not rows:
            raise HTTPException(status_code=404, detail="Announcement not found")
        meta = rows[0]
        publication_date = meta.get("publication_date")
        issue_number = meta.get("issue_number")
        page_number = meta.get("page_number")
        pdf_url = meta.get("pdf_url")

        if publication_date is None or issue_number is None or page_number is None:
            raise HTTPException(status_code=400, detail="Announcement meta incomplete (date/issue/page)")

        # 2) Parse et
        if nlp_service.nlp_model is None:
            nlp_service.load_spacy_model()
        items = nlp_service.parse_multiple_announcements(req.text)

        # 3) RPC ile ingest
        structured_payload = {"items": items}
        rpc_params = {
            "_publication_date": publication_date,
            "_issue_number": int(issue_number),
            "_page_number": int(page_number),
            "_pdf_url": pdf_url,
            "_raw_text": req.text,
            "_structured": structured_payload,
            "_company_id": None,
            "_status": "completed",
            "_pdf_page_count": int(req.pdf_page_count) if req.pdf_page_count is not None else None,
        }
        rpc_res = supabase.rpc("fn_ingest_ocr_by_ann_key", rpc_params).execute()
        rpc_data = getattr(rpc_res, "data", None)
        inserted = 0
        updated = 0
        if isinstance(rpc_data, list):
            for row in rpc_data:
                try:
                    if bool(row.get("inserted", True)):
                        inserted += 1
                    else:
                        updated += 1
                except Exception:
                    inserted += 1
        # Company bağlama (per-item) – RPC sonrası
        try:
            linked = 0
            for it in items:
                cid = _find_or_create_company(
                    supabase,
                    it.get("sicil_office_header"),
                    it.get("sicil_dosya_no") or it.get("registration_number"),
                    it.get("trade_name"),
                    it.get("addresses"),
                )
                if cid:
                    idx = it.get("index")
                    if idx is not None:
                        supabase.table("ocr_results").update({"company_id": cid}).match({
                            "publication_date": publication_date,
                            "issue_number": int(issue_number),
                            "page_number": int(page_number),
                            "item_index": int(idx),
                        }).execute()
                        linked += 1
            if linked:
                logger.info("parse-for-announcement company links updated via RPC path: %d", linked)
        except Exception:
            logger.warning("parse-for-announcement company link (RPC path) failed", exc_info=True)
        return {
            "inserted": inserted,
            "updated": updated,
            "item_count": len(items),
            "rpc": rpc_data,
            "announcement_id": req.announcement_id,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error("/parse-for-announcement failed: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail=f"parse-for-announcement failed: {e}")


@router.get("/pending-ocr-status", response_model=Dict[str, Any])
async def pending_ocr_status(
    prefix: Optional[str] = Query(None, description="Opsiyonel klasör prefix'i (gazette_pdfs altında)"),
    supabase: Client = Depends(get_supabase_client),
):
    """
    Supabase Storage 'gazette_pdfs' bucket'ında bekleyen PDF var mı?
    - Swift istemcisi bu endpoint'i çağırıp `has_pending` alanını kontrol eder.
    - `has_pending` false ise kullanıcıya "OCR yapılacak PDF yok" mesajı gösterilebilir.
    - `prefix` verilirse yalnızca ilgili alt klasör listelenir.
    """
    try:
        bucket = "gazette_pdfs"
        path = prefix.strip("/") if isinstance(prefix, str) else ""
        # Supabase Storage list: klasör içeriğini döner. Varsayılan list tüm öğeleri getirir.
        # Performans için teorik olarak limit uygulanabilir; basit bir kontrol için tam sayım yerine ilk birkaç öğe yeterli olabilir.
        # Ancak çoğu durumda bucket küçük olacağından doğrudan listeyi alıyoruz.
        objs = supabase.storage.from_(bucket).list(path)
        count = len(objs or [])
        has_pending = count > 0
        msg = "OCR yapılacak PDF yok" if not has_pending else "Bekleyen PDF'ler var"
        return {
            "has_pending": has_pending,
            "count": count,
            "bucket": bucket,
            "prefix": path or None,
            "message": msg,
        }
    except Exception as e:
        logger.warning("/pending-ocr-status failed: %s", e, exc_info=True)
        # Hata durumunda Swift tarafında güvenli bir mesaj gösterebilmek için has_pending=false döneriz
        return {
            "has_pending": False,
            "count": 0,
            "bucket": "gazette_pdfs",
            "prefix": prefix,
            "message": "OCR yapılacak PDF yok",
            "error": str(e),
        }
