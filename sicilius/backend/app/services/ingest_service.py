import logging
import re
from typing import List, Dict, Any, Tuple

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.company import Company
from app.models.announcement import Announcement
from app.models.ocr_result import OcrResult
from app.utils.office_normalization import normalize_office_from_header

logger = logging.getLogger(__name__)

# --- Helpers ---

def _normalize_whitespace(s: str | None) -> str:
    if not s:
        return ""
    return re.sub(r"\s+", " ", s).strip()


def _normalize_sicil_no(s: str | None) -> str:
    if not s:
        return ""
    s = s.strip()
    # Çok agresif olmadan sadeleştir: boşlukları kaldır, büyük harfe çevir
    s = re.sub(r"\s+", "", s)
    return s.upper()


def _canonical_sicil_root(s: str | None) -> str:
    """
    Sicil numarasının kök kısmını çıkarır: yalnızca baştaki rakamları alır.
    Örn: "315543-5" -> "315543", "315543/5" -> "315543".
    """
    if not s:
        return ""
    # Baştaki ardışık rakamları yakala
    m = re.match(r"^(\d+)", s)
    return m.group(1) if m else ""


def _extract_office_from_header(header: str | None) -> str:
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


def _pick_address(addresses: List[str] | None) -> str | None:
    if not addresses:
        return None
    # İlk anlamlı adresi seç
    for a in addresses:
        aa = _normalize_whitespace(a)
        if aa:
            return aa
    return None


def _first_word_office(s: str | None) -> str:
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


# --- Core ingest ---

def build_company_payload_from_parsed(item: Dict[str, Any]) -> Tuple[str, str, Dict[str, Any]] | None:
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
            existing: Company | None = db.execute(stmt).scalars().first()
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
                    existing.sicil_mudurluk = sicil_mudurluk
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
            existing: Company | None = db.execute(stmt).scalars().first()

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
                    existing.sicil_mudurluk = sicil_mudurluk
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
                raw_text=raw_text if isinstance(raw_text, str) else None,
                structured_data=item,
                status='completed',
            )
            db.add(ocr)
            ocr_created += 1

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
