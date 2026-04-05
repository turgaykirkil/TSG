import logging
import re
from typing import List, Dict, Any, Tuple, Optional, Set

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.company import Company
from app.models.announcement import Announcement
from app.models.ocr_result import OcrResult
from app.models.person import Person
from app.models.relation import CompanyPersonRelation, RelationType
from app.services import nlp_service
from app.utils.office_normalization import normalize_office_from_header
from app.core.search_tokens import tr_normalize_py
from app.core.search_tokens import tr_normalize_py

logger = logging.getLogger(__name__)

# --- Helpers ---

def _normalize_whitespace(s: Optional[str]) -> str:
    if not s:
        return ""
    return re.sub(r"\s+", " ", s).strip()


def _clean_nexus_string(value: Optional[str]) -> Optional[str]:
    """Unified cleaner for addresses and headers to prevent administrative noise leakage.
    Uses recursive trimming to strip headers/footers containing TC., Müdürlüğü, etc.
    """
    if not value:
        return None
    
    # 2. Identify noise tokens (Unified with NLP layer)
    noise_pat = re.compile(
        r"^([#\*\s\-\:：.,;]+|"
        r"T\.?C\.?(\s|(?=[A-ZÇĞİÖŞÜ]))|"
        r"TiCARET\s+SiCiL[İI](\s+MÜDÜRLÜĞÜ)?\s*[:：.\-]*|"
        r"MERS[İI]S\s*No.*?\:|"
        r"[İI]lan\s*S[ıi]ra\s*No.*?\:|"
        r"S[ıi]ra\s*No.*?\:)"
        r"|([#\*\s\-\:：.,;]+|"
        r"MÜDÜRLÜĞÜ['’]NDEN\.?|"
        r"MÜDÜRLÜĞÜNE\.?|"
        r"(?<!\w)MÜDÜRLÜĞÜ\.?)$",
        re.IGNORECASE
    )
    
    s = value
    iteration = 0
    while iteration < 5:
        prev = s
        s = noise_pat.sub("", s).strip()
        if s == prev: break
        iteration += 1
        
    if not s or len(s.strip()) < 2:
        return None
        
    return _normalize_whitespace(s.strip(":,.- "))

def _clean_company_address(address: Optional[str]) -> Optional[str]:
    cleaned = _clean_nexus_string(address)
    if cleaned and len(cleaned) < 5: # Address usually longer than just a city name
        return None
    return cleaned


def _normalize_sicil_no(s: Optional[str]) -> str:
    if not s:
        return ""
    s = s.strip()
    # Çok agresif olmadan sadeleştir: boşlukları kaldır, büyük harfe çevir
    s = re.sub(r"\s+", "", s)
    return s.upper()


def _canonical_sicil_root(s: Optional[str]) -> str:
    """
    Sicil numarasının kök kısmını çıkarır: yalnızca baştaki rakamları alır.
    Örn: "315543-5" -> "315543", "315543/5" -> "315543".
    """
    if not s:
        return ""
    # Baştaki ardışık rakamları yakala
    m = re.match(r"^(\d+)", s)
    return m.group(1) if m else ""


def _extract_office_from_header(header: Optional[str]) -> str:
    """
    Başlıktan (sicil_office_header) sadece İLK KELİMEYİ döner.
    Örn: "İZMİR TİCARET SİCİLİ MÜDÜRLÜĞÜ'NDEN" -> "İZMİR"

    - Başta "T.C." varsa ayıklar.
    - Mümkünse "... Ticaret Sicil" ifadesinden ÖNCEKİ kısmın ilk kelimesini alır.
    - Aksi halde başlığın ilk anlamlı alfasayısal kelimesini döner.
    """
    h = _normalize_whitespace(header)
    if not h:
        return ""
    # Baş kısımdaki "T.C." ibaresini temizle
    h = re.sub(r"^(?i)T\.?C\.?\s+", "", h)
    # "... Ticaret Sicil" öncesini hedefle
    m = re.search(r"(?i)([A-ZÇĞİÖŞÜ\s\-]{1,60})\s+Ticaret\s+Sicil\b", h)
    cand = None
    if m:
        cand = _normalize_whitespace(m.group(1))
    else:
        cand = h
    # İlk anlamlı kelime
    for tok in re.split(r"\s+", cand):
        # baş/son noktalama ayıkla
        t = re.sub(r"^[^\wÇĞİÖŞÜçğıöşü\-]+|[^\wÇĞİÖŞÜçğıöşü\-]+$", "", tok)
        if not t:
            continue
        # "ticaret", "sicil", "müdürlüğü" gibi kelimeleri ilk kelime kabul etme
        if re.match(r"(?i)ticaret|sicil|müdür|mudur|memurlu|sicili", t):
            continue
        return t.upper()
    return ""


# Duplicate _pick_address removed


def _split_person_name(full_name: str) -> Optional[Tuple[str, Optional[str], str]]:
    """
    Basit isim bölücü: son kelime soyadı, ilk kelime adı, aradakiler orta ad.
    Person modeli için first_name ve last_name zorunlu.
    Tek kelime ise veya 2'den kısa parça varsa None döner.
    """
    if not isinstance(full_name, str):
        return None
    name = _normalize_whitespace(full_name)
    if not name:
        return None
    parts = name.split(" ")
    if len(parts) < 2:
        return None
    first = parts[0]
    last = parts[-1]
    middle = " ".join(parts[1:-1]) if len(parts) > 2 else None
    if not first or not last:
        return None
    return first, (middle or None), last


def _pick_address(addresses: Optional[List[str]]) -> Optional[str]:
    if not addresses:
        return None
        
    # Pick the longest one that looks like a real address and is clean
    valid_addresses = []
    for a in addresses:
        cleaned = _clean_company_address(a)
        if cleaned and len(cleaned) > 10:
            valid_addresses.append(cleaned)
    
    if not valid_addresses:
        # Fallback to pure normalization if nothing passes the strict filter
        for a in addresses:
            aa = _normalize_whitespace(a)
            if aa and len(aa) > 5:
                return aa
        return None
        
    return max(valid_addresses, key=len)


def _first_word_office(s: Optional[str]) -> str:
    """
    Verilen ofis metninden yalnızca ilk anlamlı kelimeyi (üstteki kuralla) çıkarır.
    """
    if not s:
        return ""
    s = _normalize_whitespace(s)
    # Baş önekleri temizle: T.C., T C, TC., Türkiye Cumhuriyeti vb.
    s = re.sub(r"(?i)^(?:T\s*\.?\s*C\s*\.?\s*)+", "", s)
    s = re.sub(r"(?i)^(?:TÜRKİYE\s+CUMHURİYETİ\s+)", "", s)
    s = re.sub(r"(?i)^(?:TURKIYE\s+CUMHURIYETI\s+)", "", s)
    for tok in re.split(r"\s+", s):
        t = re.sub(r"^[^\wÇĞİÖŞÜçğıöşü\-]+|[^\wÇĞİÖŞÜçğıöşü\-]+$", "", tok)
        if not t:
            continue
        if re.match(r"(?i)ticaret|sicil|müdür|mudur|memurlu|sicili", t):
            continue
        return t.upper()
    return ""


def delete_company_person_relations(db: Session, company_id: Any):
    """Deletes all person relations for a company. Used during entity splits to clear stale data."""
    db.query(CompanyPersonRelation).filter(CompanyPersonRelation.company_id == company_id).delete()
    db.flush()


def _is_placeholder_unvan(unvan: Optional[str]) -> bool:
    """Detects if a company name is a placeholder from previous ingestion errors."""
    if not unvan:
        return True
    v = unvan.upper()
    # Common OCR noise or generic placeholders
    placeholders = [
        "MADDE 3", "TİCARET SİCİL", "SİCİL MÜDÜRLÜĞÜ", "İLAN SIRA NO",
        "SMRA", "SHEM GIDA", "ANKARA", "İSTANBUL", "KEP ADRESİ"
    ]
    # If the unvan is very short or contains major placeholder keywords
    if len(v) < 15:
        return True
    for p in placeholders:
        if p in v and len(v) < 40:
            return True
    return False


def _find_or_create_company_by_nlp(db: Session, structured_data: Dict[str, Any], current_cid: Any) -> Any:
    """
    Verifies if current_cid is the correct legal entity. 
    If not, finds or creates the correct one.
    """
    trade_name = structured_data.get("trade_name")
    sicil_no = structured_data.get("sicil_no")
    
    if not trade_name and not sicil_no:
        return current_cid

    # 1. Check current company
    current_company = db.query(Company).filter(Company.id == current_cid).first()
    if current_company:
        curr_unvan = (current_company.unvan or "").upper()
        ext_unvan = (trade_name or "").upper()
        
        # If it's a placeholder or a match, keep original CID but update it
        if _is_placeholder_unvan(current_company.unvan):
            return current_cid
        
        # If name matches (partial), keep it
        if ext_unvan and (ext_unvan in curr_unvan or curr_unvan in ext_unvan):
            return current_cid
            
        # If sicil_no matches, keep it
        if sicil_no and current_company.sicil_no == str(sicil_no):
            return current_cid

    # 2. Mismatch detected! Search for the correct entity
    # A. Search by MERSIS (Strongest identifier if present)
    mersis_no = structured_data.get("mersis_no") or structured_data.get("mersis")
    if isinstance(mersis_no, list) and mersis_no:
        mersis_no = mersis_no[0]
    
    if mersis_no:
        mersis_val = _normalize_whitespace(str(mersis_no))
        match = db.query(Company).filter(Company.mersis_number == mersis_val).first()
        if match:
            logger.info(f"Re-anchoring to existing company by MERSIS: {match.id}")
            return match.id

    # B. Search by Sicil No
    s_no = sicil_no
    if isinstance(s_no, list) and s_no:
        s_no = s_no[0]
        
    if s_no:
        match = db.query(Company).filter(Company.sicil_no == str(s_no)).first()
        if match:
            logger.info(f"Re-anchoring to existing company by Sicil No: {match.id}")
            return match.id

    # C. Search by Name (Normalized)
    if trade_name:
        t_name = trade_name
        if isinstance(t_name, list) and t_name:
            t_name = t_name[0]
        norm_name = tr_normalize_py(str(t_name))
        if len(norm_name) > 10:
            match = db.query(Company).filter(Company.unvan_unaccent.ilike(f"%{norm_name}%")).first()
            if match:
                logger.info(f"Re-anchoring to existing company by Name: {match.id}")
                return match.id

    # 3. Create new company entry if we strongly believe it's a different entity
    if trade_name:
        new_comp = Company(
            unvan=_clean_nexus_string(trade_name),
            sicil_no=str(sicil_no) if sicil_no else None,
            mersis_number=_normalize_whitespace(mersis_no) if mersis_no else None,
            address=_clean_nexus_string(_pick_address(structured_data.get("addresses")))
        )
        db.add(new_comp)
        try:
            with db.begin_nested():
                db.flush()
            logger.info(f"Created NEW company for split entity: {new_comp.id} ({trade_name})")
            return new_comp.id
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to create new company entry: {e}")
            # Final fallback: return the original CID if we can't even create a new one
            return current_cid

    return current_cid


# --- Sync Helper for OCR Tasks ---

def sync_relational_data_from_nlp(db: Session, company_id: Any, structured_data: Dict[str, Any]) -> Any:
    """
    Called by background OCR tasks to sync extracted data back to relational tables.
    Returns the (potentially new/split) company_id.
    """
    # 1. Entity Re-Anchoring: Ensure we are using the correct company UUID
    target_cid = _find_or_create_company_by_nlp(db, structured_data, company_id)
    
    # 2. Update company metadata
    company = db.query(Company).filter(Company.id == target_cid).first()
    if company:
        changed = False
        trade_name = structured_data.get("trade_name")
        current_unvan = company.unvan
        
        # Overwrite if current unvan is empty OR a placeholder
        if trade_name and (_is_placeholder_unvan(current_unvan) or not _normalize_whitespace(current_unvan)):
            company.unvan = _clean_nexus_string(trade_name)
            changed = True
        
        # Address update
        address = _pick_address(structured_data.get("addresses"))
        if address and not company.address:
            # Also clean address before sinking
            company.address = _clean_nexus_string(address)
            changed = True
            
        # Mersis update if missing
        mersis = structured_data.get("mersis_no")
        if mersis and not company.mersis_number:
            company.mersis_number = _normalize_whitespace(mersis)
            changed = True
            
        if changed:
            try:
                # Use a nested transaction (savepoint) to prevent poisoning the whole session on IntegrityError
                with db.begin_nested():
                    db.flush()
                logger.info(f"Updated metadata for company {company_id} from NLP")
            except Exception as exc:
                # If MERSIS is duplicate or other constraint fails, we skip this metadata update
                db.rollback() 
                logger.warning(f"Could not sync NLP metadata for company {company_id}: {exc}")

    # 3. Ingest persons and relations
    ingest_persons_and_relations(
        db, target_cid, 
        structured_data.get("persons"), 
        structured_data.get("publication_date")
    )
    
    return target_cid


# --- Core ingest ---

def ingest_persons_and_relations(
    db: Session, 
    company_id: Any, 
    persons_data: Optional[List[Dict[str, Any]]],
    pub_date: Optional[Any] = None
):
    """
    Normalizes persons and creates CompanyPersonRelation records.
    """
    if not persons_data or not isinstance(persons_data, list):
        return

    seen_relations: Set[Tuple[Any, Any]] = set()
    for person_item in persons_data:
        if not isinstance(person_item, dict):
            continue
        
        full_name = person_item.get("text") or person_item.get("full_name") or person_item.get("name")
        masked_id = person_item.get("masked_ids") or person_item.get("masked_id")
        if isinstance(masked_id, list) and masked_id:
            masked_id = masked_id[0]
        
        address = person_item.get("address")
        
        if not full_name:
            continue
        
        # Split name into first/last
        name_parts = _split_person_name(full_name)
        if not name_parts:
            logger.debug(f"Could not split person name: {full_name}")
            continue
        
        first_name, middle_name, last_name = name_parts
        
        # SEARCH FOR EXISTING PERSON (Disjunctive: Name + [ID OR Address])
        # Find candidates with same name
        candidates = db.query(Person).filter(
            Person.first_name == first_name,
            Person.last_name == last_name
        ).all()
        
        existing_person = None
        for cand in candidates:
            # 1. Match by Masked ID (Strongest)
            if masked_id and cand.masked_id == masked_id:
                existing_person = cand
                break
            
            # 2. Match by Address (Secondary)
            if address and cand.address == address:
                 existing_person = cand
                 break
            
            # 3. Fallback: If both existing and new have NO ID and NO Address, 
            # we assume it's the same person (Standard deduplication)
            if not masked_id and not cand.masked_id and not address and not cand.address:
                existing_person = cand
                break

        if not existing_person:
            # Create new person
            person_obj = Person(
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                masked_id=masked_id,
                address=address
            )
            db.add(person_obj)
            db.flush()
            logger.info(f"Created person: {full_name} (ID: {masked_id}, Address: {address})")
        else:
            person_obj = existing_person
            # Update fields if they were missing
            updated = False
            if not person_obj.masked_id and masked_id:
                person_obj.masked_id = masked_id
                updated = True
            if not person_obj.address and address:
                person_obj.address = address
                updated = True
            
            if updated:
                logger.info(f"Updated person: {full_name} (ID: {person_obj.masked_id}, Address: {person_obj.address})")
            else:
                logger.debug(f"Matched existing person: {full_name}")
        
        # Create or update CompanyPersonRelation
        rel_key = (company_id, person_obj.id)
        if rel_key in seen_relations:
            continue

        existing_relation = db.query(CompanyPersonRelation).filter(
            CompanyPersonRelation.company_id == company_id,
            CompanyPersonRelation.person_id == person_obj.id
        ).first()
        
        if not existing_relation:
            relation = CompanyPersonRelation(
                company_id=company_id,
                person_id=person_obj.id,
                relation_type=RelationType.SHAREHOLDER,
                start_date=pub_date,
                is_current=True,
                source="NLP_EXTRACTION"
            )
            db.add(relation)
            db.flush()
            seen_relations.add(rel_key)
            logger.debug(f"Created relation: {full_name} <-> company:{company_id}")
        else:
            seen_relations.add(rel_key)


# --- Core ingest ---

def build_company_payload_from_parsed(item: Dict[str, Any]) -> Optional[Tuple[str, str, Dict[str, Any]]]:
    """
    Parse edilmiş tek ilan kaydından (nlp_service.parse_multiple_announcements çıktısı)
    Company için gerekli alanları üretir.

    Zorunlu: sicil_no, sicil_mudurluk
    Opsiyonel: unvan, address

    Returns tuple: (sicil_no, sicil_mudurluk, payload_dict)
    """
    reg = _normalize_sicil_no(item.get("registration_number") or item.get("sicil_dosya_no"))
    header = item.get("sicil_office_header")
    office_full = normalize_office_from_header(header) or None
    # Gereksinim: Ofis eşitliği ve yeni kayıtlar İLK KELİME bazında olacak
    office_first = _first_word_office(office_full or header)
    try:
        logger.debug(
            "normalize flow idx=%s reg=%s header=%s -> office_full=%s office_first=%s",
            item.get("index"), reg, _normalize_whitespace(header), office_full, office_first,
        )
    except Exception:
        pass

    if not reg or not office_first:
        try:
            logger.warning(
                "Company payload skipped due to missing fields: index=%s, reg=%s, office_first=%s, header=%s",
                item.get("index"), reg, office_first, _normalize_whitespace(item.get("sicil_office_header"))
            )
        except Exception:
            pass
        return None

    trade_name = _normalize_whitespace(item.get("trade_name")) or None
    address = _pick_address(item.get("addresses"))

    payload = {
        "sicil_no": reg,
        # Yeni kayıtlarda sadece ilk kelime saklanacak
        "sicil_mudurluk": office_first,
        "sicil_office_code": office_first,
    }
    if trade_name:
        payload["unvan"] = trade_name
    if address:
        payload["address"] = address

    logger.debug(
        "Built company payload idx=%s sicil_no=%s office_first=%s trade=%s addr_len=%s",
        item.get("index"), reg, office_first, bool(trade_name), len(address or "")
    )
    return reg, office_first, payload


def upsert_companies(parsed_list: List[Dict[str, Any]], db: Session) -> Dict[str, Any]:
    """
    Verilen parse edilmiş ilan listesi üzerinden companies tablosunu günceller.
    - sicil_no ve sicil_mudurluk zorunlu; eksikse atlanır.
    - Kayıt varsa: unvan/adres dolu ise güncellenir.
    - Kayıt yoksa: eklenir.
    """
    inserted = 0
    updated = 0
    skipped = 0
    office_mismatch = 0
    errors: List[str] = []

    logger.info("upsert_companies started count=%s", len(parsed_list))
    for item in parsed_list:
        try:
            built = build_company_payload_from_parsed(item)
            if not built:
                skipped += 1
                continue
            sicil_no, sicil_mudurluk, payload = built
            try:
                logger.debug(
                    "upsert flow idx=%s sicil_no=%s office_first=%s title=%s",
                    item.get("index"), sicil_no, sicil_mudurluk, _normalize_whitespace(payload.get("unvan")) if payload.get("unvan") else None,
                )
            except Exception:
                pass

            # Mevcut kayıt var mı? (sicil_no + ofis İLK KELİME)
            stmt = select(Company).where(
                Company.sicil_no == sicil_no,
                Company.sicil_office_code == sicil_mudurluk,
            )
            existing: Optional[Company] = db.execute(stmt).scalars().first()
            logger.debug("lookup primary key match sicil_no=%s office=%s found=%s", sicil_no, sicil_mudurluk, bool(existing))

            # Geçmişte TAM resmi ad ile kayıt edilmiş olma olasılığına karşı ikinci deneme
            if not existing:
                office_full = normalize_office_from_header(item.get("sicil_office_header")) or None
                if office_full and office_full != sicil_mudurluk:
                    stmt2 = select(Company).where(
                        Company.sicil_no == sicil_no,
                        Company.sicil_office_code == office_full,
                    )
                    existing = db.execute(stmt2).scalars().first()
                    logger.debug("lookup fallback full office sicil_no=%s office_full=%s found=%s", sicil_no, office_full, bool(existing))

            if existing:
                # Eğer sicil_mudurluk boş ve payload dolu ise set et
                changed = False
                if not existing.sicil_mudurluk and sicil_mudurluk:
                    existing.sicil_mudurluk = _clean_nexus_string(sicil_mudurluk)
                    changed = True
                # sicil_office_code eksikse doldur
                if (not getattr(existing, "sicil_office_code", None)) and sicil_mudurluk:
                    existing.sicil_office_code = sicil_mudurluk
                    changed = True
                elif existing.sicil_mudurluk and sicil_mudurluk:
                    # İlk kelimeler eşit ise eşdeğer say (resmi isim çok kelimeli olabilir)
                    ex_first = _first_word_office(existing.sicil_mudurluk)
                    in_first = _first_word_office(sicil_mudurluk)
                    if ex_first and in_first and ex_first == in_first:
                        pass
                    else:
                        # Mevcut ofis ile gelen ofis farklıysa değiştirmiyoruz, raporla
                        office_mismatch += 1
                        logger.info(
                            "office mismatch idx=%s sicil_no=%s existing_first=%s incoming_first=%s existing_raw=%s incoming_raw=%s",
                            item.get("index"), sicil_no, ex_first, in_first, _normalize_whitespace(existing.sicil_mudurluk), sicil_mudurluk,
                        )
                # Unvan/adres güncelle (varsa)
                incoming_unvan = payload.get("unvan")
                if incoming_unvan:
                    # TAVSİYE POLİTİKASI: Sadece mevcut unvan BOŞSA doldur; doluysa overwrite etme
                    if not _normalize_whitespace(existing.unvan):
                        existing.unvan = incoming_unvan
                        changed = True
                if payload.get("address") and payload.get("address") != existing.address:
                    existing.address = payload.get("address")
                    changed = True
                if changed:
                    logger.debug("company updated sicil_no=%s office=%s", sicil_no, sicil_mudurluk)
                    updated += 1
            else:
                company_obj = Company(**payload)
                db.add(company_obj)
                logger.debug("company inserted sicil_no=%s office=%s", sicil_no, sicil_mudurluk)
                inserted += 1
        except Exception as e:
            logger.error("Ingest error: %s", e, exc_info=True)
            errors.append(str(e))
            skipped += 1

    # Toplu commit
    try:
        logger.info("Committing changes...")
        db.commit()
        logger.info("upsert_companies committed inserted=%s updated=%s skipped=%s office_mismatch=%s", inserted, updated, skipped, office_mismatch)
    except Exception as e:
        logger.error("upsert_companies commit failed: %s", e, exc_info=True)
        db.rollback()
        logger.info("Rolled back changes...")
        raise

    return {
        "inserted": inserted,
        "updated": updated,
        "skipped": skipped,
        "office_mismatch": office_mismatch,
        "errors": errors[:5],
    }


def ingest_companies_and_announcements(parsed_list: List[Dict[str, Any]], db: Session) -> Dict[str, Any]:
    """
    Parse edilmiş ilan listesi üzerinden şirketleri upsert eder ve her ilan için
    `announcements` + `ocr_results` kayıtları oluşturur.

    - Şirket eşleştirme: `sicil_no` (registration_number/sicil_dosya_no normalize edilmiş) + ofis ilk kelime kuralı
    - Mevcut şirket varsa güncelleme kuralları `upsert_companies` ile aynıdır
    - Her başarılı şirket için bir `Announcement` oluşturulur (company_id FK)
    - Her `Announcement` için bir `OcrResult` oluşturulur:
        - raw_text = item["original_text"]
        - structured_data = tüm `item` sözlüğü (JSON)
        - status = 'completed'

    Dönüş, geriye uyum için company inserted/updated/skipped sayılarını aynı anahtarlarla içerir
    ve ek olarak announcement/ocr sayaçlarını ve UUID eşleştirmelerini döner.
    """
    inserted = 0
    updated = 0
    skipped = 0
    office_mismatch = 0
    ann_created = 0
    ocr_created = 0
    errors: List[str] = []
    links: List[Dict[str, Any]] = []
    seen_relations: Set[Tuple[Any, Any]] = set()

    logger.info("ingest_companies_and_announcements started count=%s", len(parsed_list))
    for item in parsed_list:
        try:
            built = build_company_payload_from_parsed(item)
            if not built:
                skipped += 1
                continue
            sicil_no, sicil_mudurluk, payload = built
            sicil_root = _canonical_sicil_root(sicil_no)

            # 1) Şirketi getir/oluştur (sicil_no + ofis ilk kelime kodu)
            stmt = select(Company).where(
                Company.sicil_no == sicil_no,
                Company.sicil_office_code == sicil_mudurluk,
            )
            existing: Optional[Company] = db.execute(stmt).scalars().first()

            # Tam resmi ad ile geçmiş kayıt olma ihtimaline karşı ikinci deneme
            if not existing:
                office_full = normalize_office_from_header(item.get("sicil_office_header")) or None
                if office_full and office_full != sicil_mudurluk:
                    stmt2 = select(Company).where(
                        Company.sicil_no == sicil_no,
                        Company.sicil_office_code == office_full,
                    )
                    existing = db.execute(stmt2).scalars().first()

            # Tam eşleşme bulunamazsa, köke göre tekil eşleşme ara (315543-5, 315543/5 vb.)
            if not existing and sicil_root:
                try:
                    # Aynı köke sahip olası tekil şirketleri bul
                    candidates = db.execute(
                        select(Company).where(Company.sicil_no.op("~")(rf"^{sicil_root}([\-/].+)?$") )
                    ).scalars().all()
                    if len(candidates) == 1:
                        existing = candidates[0]
                    elif len(candidates) > 1:
                        # Belirsizlik—yanlış eşleşmeden kaçınmak için kayıt atla
                        office_mismatch += 1
                        errors.append(
                            f"Ambiguous sicil root match for {sicil_no}: {len(candidates)} candidates"
                        )
                        skipped += 1
                        logger.warning("ambiguous root match (ingest) sicil_root=%s candidates=%s", sicil_root, len(candidates))
                        continue
                except Exception as _e:
                    logger.warning("Regex fallback for sicil_no failed: %s", _e)

            company_obj: Company
            if existing:
                company_obj = existing
                changed = False
                if not existing.sicil_mudurluk and sicil_mudurluk:
                    existing.sicil_mudurluk = _clean_nexus_string(sicil_mudurluk)
                    changed = True
                if (not getattr(existing, "sicil_office_code", None)) and sicil_mudurluk:
                    existing.sicil_office_code = sicil_mudurluk
                    changed = True
                elif existing.sicil_mudurluk and sicil_mudurluk:
                    ex_first = _first_word_office(existing.sicil_mudurluk)
                    in_first = _first_word_office(sicil_mudurluk)
                    if ex_first and in_first and ex_first == in_first:
                        pass
                    else:
                        office_mismatch += 1
                incoming_unvan = payload.get("unvan")
                if incoming_unvan:
                    # TAVSİYE POLİTİKASI: Sadece mevcut unvan BOŞSA doldur; doluysa overwrite etme
                    if not _normalize_whitespace(existing.unvan):
                        existing.unvan = incoming_unvan
                        changed = True
                if payload.get("address") and payload.get("address") != existing.address:
                    existing.address = payload.get("address")
                    changed = True
                if changed:
                    logger.debug("company updated (ingest) sicil_no=%s office=%s", sicil_no, sicil_mudurluk)
                    updated += 1
            else:
                company_obj = Company(**payload)
                db.add(company_obj)
                logger.debug("company inserted (ingest) sicil_no=%s office=%s", sicil_no, sicil_mudurluk)
                inserted += 1

            # Flush ederek company_obj.id'yi garantile
            db.flush()
            logger.debug("announcement prepare company_id=%s", getattr(company_obj, 'id', None))

            # 2) Announcement oluştur (minimum alanlarla)
            ann = Announcement(
                company_id=company_obj.id,
                trade_registry_name=_normalize_whitespace(item.get("sicil_office_header") or None) or None,
                trade_registry_number=sicil_no,
                title=_normalize_whitespace(payload.get("unvan")) if payload.get("unvan") else None,
                pdf_url=None,
                content=item.get("original_text")
            )
            db.add(ann)
            db.flush()  # ann.id
            logger.debug("announcement created id=%s", getattr(ann, 'id', None))
            ann_created += 1

            # 3) OCR sonucu bağla (company'e doğrudan, announcement opsiyonel)
            raw_text = item.get("original_text")
            ocr = OcrResult(
                company_id=company_obj.id,
                announcement_id=ann.id,
                original_text=raw_text if isinstance(raw_text, str) else None,
                # Map structured data fields to columns
                publication_date=item.get("publication_date"),
                issue_number=item.get("issue_number"),
                page_number=item.get("page_number"),
                pdf_url=item.get("pdf_url"),
                pdf_page_count=item.get("pdf_page_count"),
                sicil_office_header=item.get("sicil_office_header"),
                sicil_dosya_no=item.get("sicil_dosya_no"),
                mersis_no=item.get("mersis_no"),
                trade_name=item.get("trade_name"),
                old_trade_name=item.get("old_trade_name"),
                addresses=item.get("addresses"),
                old_addresses=item.get("old_addresses"),
                persons=item.get("persons"),
                masked_ids=item.get("masked_ids"),
                hususlar=item.get("hususlar"),
                belgeler=item.get("belgeler"),
                type=item.get("type"),
                item_index=item.get("index"),
                start_offset=item.get("start_offset"),
                end_offset=item.get("end_offset"),
                is_derived=item.get("is_derived"),
                derived_from_index=item.get("derived_from_index"),
                ilan_sira_no=item.get("ilan_sira_no"),
                status='completed',
            )
            db.add(ocr)
            ocr_created += 1

            # 4) Normalize persons from OCR JSON to Person and CompanyPersonRelation tables
            ingest_persons_and_relations(
                db, company_obj.id, 
                item.get("persons"), 
                item.get("publication_date")
            )


            links.append({
                "index": item.get("index"),
                "company_id": str(company_obj.id),
                "announcement_id": str(ann.id),
                "sicil_no": sicil_no,
                "sicil_mudurluk": sicil_mudurluk,
            })
        except Exception as e:
            logger.error("Ingest+Link error: %s", e, exc_info=True)
            errors.append(str(e))
            skipped += 1

    # Toplu commit
    try:
        db.commit()
        logger.info(
            "ingest committed inserted=%s updated=%s skipped=%s office_mismatch=%s ann=%s ocr=%s",
            inserted, updated, skipped, office_mismatch, ann_created, ocr_created
        )
        
    except Exception as e:
        logger.error("ingest commit failed: %s", e, exc_info=True)
        db.rollback()
        raise

    return {
        # Backward-compatible company counts
        "inserted": inserted,
        "updated": updated,
        "skipped": skipped,
        "office_mismatch": office_mismatch,
        "errors": errors[:5],
        # New artifacts
        "announcements_created": ann_created,
        "ocr_results_created": ocr_created,
        "links": links,
    }
