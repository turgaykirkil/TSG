from fastapi import APIRouter, Depends, HTTPException, Query
from supabase import Client
from typing import List, Dict, Any, Optional, Set
from pydantic import BaseModel, Field
from datetime import datetime
import re
import unicodedata
import logging
from app.core.dependencies import get_supabase_client

router = APIRouter()
logger = logging.getLogger(__name__)

class SearchResult(BaseModel):
    companies: List[Dict[str, Any]] = Field(default_factory=list)
    persons: List[Dict[str, Any]] = Field(default_factory=list)
    announcements: List[Dict[str, Any]] = Field(default_factory=list)
    related_companies: List[Dict[str, Any]] = Field(default_factory=list)
    same_address_companies: List[Dict[str, Any]] = Field(default_factory=list)
    related_persons: List[Dict[str, Any]] = Field(default_factory=list)
    ocr_matches: List[Dict[str, Any]] = Field(default_factory=list)
    total_matches: int = 0


def tr_normalize_py(s: Optional[str]) -> str:
    """Türkçe aksan ve noktalı I/ı duyarsız normalize edici.
    - 'İ' -> 'I', 'ı' -> 'i'
    - Unicode accent kaldırma
    - lower()
    """
    if not s:
        return ""
    s = s.replace("İ", "I").replace("ı", "i")
    # NFKD ile ayır ve ASCII dışını temizle (örn. ç->c, ş->s)
    s = unicodedata.normalize("NFKD", s)
    s = s.encode("ascii", "ignore").decode("ascii")
    return s.lower().strip()

def tr_letters_digits(s: Optional[str]) -> str:
    """Normalize et ve harf/rakam dışını çıkar. Maskeli OCR metinleri için faydalı."""
    if not s:
        return ""
    return re.sub(r"[^a-z0-9]+", "", tr_normalize_py(s))

def search_all_related(query: str, supabase: Client) -> SearchResult:
    """
    Kapsamlı ve Türkçe aksan duyarsız arama.
    1) Şirketleri, kişileri ve OCR/duyuru/gazete metinlerini tarar.
    2) İlişki geçişleri: kişi->şirket ve şirket->kişi, aynı adres vs.
    3) Unaccent generated kolonları varsa onları kullanır; yoksa Python tarafında normalize ederek filtreler.
    """
    result = SearchResult()
    q_raw = (query or "").strip()
    q_norm = tr_normalize_py(q_raw)
    tokens = [t for t in re.split(r"\s+", q_norm) if t]
    tokens_letters = [tr_letters_digits(t) for t in tokens if tr_letters_digits(t)]

    # 1) Şirketler: önce unaccent kolonları dene, hata olursa orijinal kolonlar ve Python filtresi
    companies_data: List[Dict[str, Any]] = []
    try:
        filter_expr = (
            f"unvan_unaccent.ilike.%{q_norm}%,"
            f"sicil_no_unaccent.ilike.%{q_norm}%,"
            f"address_unaccent.ilike.%{q_norm}%"
        )
        companies_data = (
            supabase.table("companies")
            .select("*")
            .or_(filter_expr)
            .limit(100)
            .execute()
        ).data or []
    except Exception:
        # Fallback: orijinal kolonlarla geniş arama, sonra Python normalize ile filtre
        coarse = (
            supabase.table("companies")
            .select("*")
            .or_(f"unvan.ilike.%{q_raw}%,sicil_no.ilike.%{q_raw}%,address.ilike.%{q_raw}%")
            .limit(200)
            .execute()
        ).data or []
        companies_data = [
            c for c in coarse
            if q_norm in tr_normalize_py(c.get("unvan", ""))
            or q_norm in tr_normalize_py(c.get("sicil_no", ""))
            or q_norm in tr_normalize_py(c.get("address", ""))
        ]

    # Çok kelimeli sorgu: ilk sorgu sonuç vermediyse, token bazlı geniş OR + Python AND filtresi
    if not companies_data and len(tokens) > 1:
        try:
            conds = []
            for t in tokens:
                pat = f"%{t}%"
                conds.extend([
                    f"unvan_unaccent.ilike.{pat}",
                    f"sicil_no_unaccent.ilike.{pat}",
                    f"address_unaccent.ilike.{pat}",
                ])
            or_expr = ",".join(conds)
            coarse_multi = (
                supabase.table("companies").select("*").or_(or_expr).limit(300).execute()
            ).data or []
            companies_data = [
                c for c in coarse_multi
                if all(
                    t in tr_normalize_py(" ".join([c.get("unvan", ""), c.get("sicil_no", ""), c.get("address", "")]))
                    for t in tokens
                )
            ]
        except Exception:
            pass

    # Dedup by id
    seen_company_ids: Set[str] = set()
    companies: List[Dict[str, Any]] = []
    for c in companies_data:
        cid = c.get("id")
        if cid and cid not in seen_company_ids:
            seen_company_ids.add(cid)
            companies.append(c)

    result.companies = companies
    company_ids = list(seen_company_ids)

    # 1b) Bulunan şirketlere ait duyuruları getir
    try:
        if company_ids:
            ann_resp = (
                supabase
                .table("announcements")
                .select("id, company_id, title, announcement_type, publication_date, issue_number, page_number, newspaper_name, pdf_url, ocr_status, created_at")
                .in_("company_id", company_ids)
                .order("publication_date", desc=True)
                .limit(300)
                .execute()
            )
            result.announcements = ann_resp.data or []
    except Exception:
        result.announcements = []

    # 1c) Bulunan şirketlerden ilişkili kişiler
    related_persons: List[Dict[str, Any]] = []
    try:
        if company_ids:
            rels_cp = (
                supabase
                .table("company_person_relations")
                .select("company_id, person_id, relation_type, position, is_current, start_date, end_date")
                .in_("company_id", company_ids)
                .limit(2000)
                .execute()
            ).data or []

            person_ids_for_companies = sorted({r.get("person_id") for r in rels_cp if r.get("person_id")})
            persons_map_cp: Dict[str, Dict[str, Any]] = {}
            if person_ids_for_companies:
                persons_resp_cp = (
                    supabase
                    .table("persons")
                    .select("id, full_name, first_name, last_name, email, nationality_id, birth_date, is_active, updated_at")
                    .in_("id", person_ids_for_companies)
                    .limit(2000)
                    .execute()
                )
                persons_map_cp = {p["id"]: p for p in (persons_resp_cp.data or [])}

            dedup_rel_keys: Set[str] = set()
            for r in rels_cp:
                pid = r.get("person_id")
                cid = r.get("company_id")
                if not pid or not cid:
                    continue
                key = f"{cid}:{pid}"
                if key in dedup_rel_keys:
                    continue
                dedup_rel_keys.add(key)
                base_person = persons_map_cp.get(pid, {"id": pid})
                merged = {
                    **base_person,
                    "company_id": cid,
                    "relation_type": r.get("relation_type"),
                    "position": r.get("position"),
                    "is_current": r.get("is_current"),
                    "start_date": r.get("start_date"),
                    "end_date": r.get("end_date"),
                }
                related_persons.append(merged)
    except Exception:
        related_persons = []
    result.related_persons = related_persons

    # 2) Aynı adresteki şirketler
    same_address_companies: List[Dict[str, Any]] = []
    same_seen: Set[str] = set()
    for company in companies:
        addr = company.get("address")
        if not addr:
            continue
        try:
            same_addr = (
                supabase.table("companies")
                .select("*")
                .eq("address", addr)
                .neq("id", company.get("id"))
                .limit(50)
                .execute()
            ).data or []
        except Exception:
            same_addr = []
        for sc in same_addr:
            scid = sc.get("id")
            if scid and scid not in same_seen and scid not in seen_company_ids:
                same_seen.add(scid)
                same_address_companies.append(sc)
    result.same_address_companies = same_address_companies

    # 3) Kişiler: isimle eşleşen kişiler (aksansız) + şirket ilişkileri
    persons_match: List[Dict[str, Any]] = []
    try:
        persons_filter = (
            f"full_name_unaccent.ilike.%{q_norm}%,"
            f"first_name_unaccent.ilike.%{q_norm}%,"
            f"last_name_unaccent.ilike.%{q_norm}%"
        )
        persons_match = (
            supabase.table("persons")
            .select("*")
            .or_(persons_filter)
            .limit(100)
            .execute()
        ).data or []
    except Exception:
        coarse_p = (
            supabase.table("persons")
            .select("*")
            .or_(f"full_name.ilike.%{q_raw}%,first_name.ilike.%{q_raw}%,last_name.ilike.%{q_raw}%")
            .limit(200)
            .execute()
        ).data or []
        persons_match = [
            p for p in coarse_p
            if q_norm in tr_normalize_py(p.get("full_name", ""))
            or q_norm in tr_normalize_py(p.get("first_name", ""))
            or q_norm in tr_normalize_py(p.get("last_name", ""))
        ]

    # Çok kelimeli sorgu için ek yaklaşım: geniş OR + Python AND filtresi
    if not persons_match and len(tokens) > 1:
        try:
            conds = []
            for t in tokens:
                pat = f"%{t}%"
                conds.extend([
                    f"full_name_unaccent.ilike.{pat}",
                    f"first_name_unaccent.ilike.{pat}",
                    f"last_name_unaccent.ilike.{pat}",
                ])
            or_expr = ",".join(conds)
            coarse_pt = (
                supabase.table("persons").select("*").or_(or_expr).limit(400).execute()
            ).data or []
            persons_match = [
                p for p in coarse_pt
                if all(
                    t in tr_normalize_py(" ".join([p.get("full_name", ""), p.get("first_name", ""), p.get("last_name", "")]))
                    for t in tokens
                )
            ]
        except Exception:
            pass
    # Dedup persons by id
    seen_person_ids: Set[str] = set()
    persons: List[Dict[str, Any]] = []
    for p in persons_match:
        pid = p.get("id")
        if pid and pid not in seen_person_ids:
            seen_person_ids.add(pid)
            persons.append(p)
    result.persons = persons

    # 4) Kişilerden ilişkili şirketleri bul
    related_companies: List[Dict[str, Any]] = []
    related_seen: Set[str] = set()
    if seen_person_ids:
        rels = (
            supabase.table("company_person_relations")
            .select("company_id, person_id, relation_type, position, is_current, start_date, end_date")
            .in_("person_id", list(seen_person_ids))
            .limit(1000)
            .execute()
        ).data or []
        rel_company_ids = sorted({r.get("company_id") for r in rels if r.get("company_id")})
        if rel_company_ids:
            comp2 = (
                supabase.table("companies")
                .select("*")
                .in_("id", rel_company_ids)
                .limit(1000)
                .execute()
            ).data or []
            for c in comp2:
                cid = c.get("id")
                if cid and cid not in related_seen and cid not in seen_company_ids:
                    related_seen.add(cid)
                    related_companies.append(c)
    result.related_companies = related_companies

    # 5) OCR ve duyurular (aksansız): mümkünse *_unaccent kolonları, değilse Python filtresi
    ocr_matches: List[Dict[str, Any]] = []
    try:
        ocr_q = (
            supabase.table("ocr_results")
            .select("id, announcement_id, company_id, original_text, companies(*)")
            .limit(200)
        )
        if tokens:
            # Her token için AND olacak şekilde birden çok ilike uygula (unaccent kolonu yok)
            for t in tokens:
                ocr_q = ocr_q.ilike("original_text", f"%{t}%")
        else:
            ocr_q = ocr_q.ilike("original_text", f"%{q_norm}%")
        ocr_matches = (ocr_q.execute()).data or []

        # Yıldız/punktuasyon maskeleri için ek Python filtresi (boş dönerse)
        if not ocr_matches and tokens_letters:
            coarse_ocr = (
                supabase.table("ocr_results")
                .select("id, announcement_id, company_id, original_text, companies(*)")
                .limit(500)
                .execute()
            ).data or []
            ocr_matches = [
                o for o in coarse_ocr
                if all(tl in tr_letters_digits(o.get("original_text", "")) for tl in tokens_letters)
            ]
    except Exception:
        coarse_ocr = (
            supabase.table("ocr_results")
            .select("id, announcement_id, company_id, original_text, companies(*)")
            .limit(300)
            .execute()
        ).data or []
        if tokens_letters:
            ocr_matches = [
                o for o in coarse_ocr
                if all(tl in tr_letters_digits(o.get("original_text", "")) for tl in tokens_letters)
            ]
        else:
            ocr_matches = [o for o in coarse_ocr if q_norm in tr_normalize_py(o.get("original_text", ""))]

    # OCR'dan gelen şirketleri ana listeye ekle (dedup)
    for o in ocr_matches:
        comp_obj = o.get("companies")
        cid = comp_obj.get("id") if isinstance(comp_obj, dict) else o.get("company_id")
        if cid and cid not in seen_company_ids and cid not in related_seen and cid not in same_seen:
            # şirket objesi yoksa minimal bir obje oluştur
            to_add = comp_obj if isinstance(comp_obj, dict) and comp_obj else {"id": cid}
            result.companies.append(to_add)
            seen_company_ids.add(cid)

    result.ocr_matches = ocr_matches

    # 6) Toplam eşleşme sayısı
    result.total_matches = (
        len(result.companies)
        + len(result.related_companies)
        + len(result.same_address_companies)
        + len(result.persons)
        + len(result.ocr_matches)
    )

    return result

@router.get("/companies")
def search_companies(
    q: str = Query(..., min_length=2, description="Search term for companies"),
    supabase: Client = Depends(get_supabase_client)
):
    """
    Searches for companies in the database based on a query term.
    The search is performed on company name, registration number, and address.
    """
    try:
        # Use the new comprehensive search
        result = search_all_related(q, supabase)
        return {
            "companies": result.companies,
            "related_companies": result.related_companies,
            "same_address_companies": result.same_address_companies,
            "total_matches": result.total_matches
        }
    except Exception as e:
        logger.error(f"Error searching companies: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/cross-company-persons", summary="Persons across multiple companies and starred OCR persons")
def cross_company_persons(
    min_companies: int = Query(2, ge=2, le=50, description="Minimum distinct companies per person/name"),
    limit: int = Query(200, ge=1, le=1000, description="Max items to return for each category"),
    supabase: Client = Depends(get_supabase_client),
):
    """
    Döndürür:
    - persons_multi_company: İlişkilere göre birden fazla şirkette yer alan kişiler
    - starred_persons: OCR'da *** maskeleme içeren isim benzeri ibareler ve göründükleri farklı şirketler
    """
    try:
        # --- 1) İlişkilere göre çok şirketli kişiler ---
        rels_resp = (
            supabase
            .table("company_person_relations")
            .select("person_id, company_id")
            .limit(5000)
            .execute()
        )
        rels = rels_resp.data or []
        person_companies: Dict[str, Set[str]] = {}
        for r in rels:
            pid = r.get("person_id")
            cid = r.get("company_id")
            if not pid or not cid:
                continue
            person_companies.setdefault(pid, set()).add(cid)
        multi_person_ids = [pid for pid, cset in person_companies.items() if len(cset) >= min_companies]

        persons_multi_company = []
        if multi_person_ids:
            # Kısıtla
            multi_person_ids = multi_person_ids[:min(limit, 1000)]
            persons_resp = (
                supabase
                .table("persons")
                .select("id, full_name, first_name, last_name, email, nationality_id")
                .in_("id", multi_person_ids)
                .limit(min(len(multi_person_ids), 1000))
                .execute()
            )
            persons_map = {p["id"]: p for p in (persons_resp.data or [])}
            for pid in multi_person_ids:
                companies_for_person = sorted(list(person_companies.get(pid, set())))
                persons_multi_company.append({
                    **persons_map.get(pid, {"id": pid}),
                    "company_ids": companies_for_person,
                    "company_count": len(companies_for_person),
                })
            # company_count'a göre sırala
            persons_multi_company.sort(key=lambda x: x.get("company_count", 0), reverse=True)
            persons_multi_company = persons_multi_company[:limit]

        # --- 2) OCR'da yıldızlı isimler ---
        starred_map: Dict[str, Set[str]] = {}
        try:
            ocr_q = (
                supabase
                .table("ocr_results")
                .select("company_id, raw_text")
                .like("raw_text_unaccent", "%***%")
                .limit(5000)
            )
            ocr_resp = ocr_q.execute()
            ocr_rows = ocr_resp.data or []
        except Exception:
            # unaccent kolonu yoksa fallback
            ocr_rows = (
                supabase
                .table("ocr_results")
                .select("company_id, raw_text")
                .like("raw_text", "%***%")
                .limit(5000)
                .execute()
            ).data or []

        import re as _re
        for row in ocr_rows:
            cid = row.get("company_id")
            if not cid:
                continue
            text = row.get("raw_text", "") or ""
            # Basit bir pattern: BÜYÜK HARF + yıldızlar
            matches = _re.findall(r"([A-ZĞÜŞİÖÇ]+\*+)", text)
            for m in matches:
                clean = _re.sub(r"\*+", " ", m).strip()
                if clean and len(clean) > 2:
                    key = clean
                    starred_map.setdefault(key, set()).add(cid)

        starred_persons = [
            {"name": name, "company_ids": sorted(list(cids)), "company_count": len(cids)}
            for name, cids in starred_map.items()
            if len(cids) >= min_companies
        ]
        starred_persons.sort(key=lambda x: x.get("company_count", 0), reverse=True)
        starred_persons = starred_persons[:limit]

        return {
            "persons_multi_company": persons_multi_company,
            "starred_persons": starred_persons,
            "min_companies": min_companies,
            "limit": limit,
        }
    except Exception as e:
        logger.error(f"[Cross Company Persons] Error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An error occurred while fetching cross-company persons.")

@router.get("/all", response_model=Dict[str, Any])
def search_all(
    q: str = Query(..., min_length=2, description="Search across companies, persons, OCR and history (SPA payload)"),
    supabase: Client = Depends(get_supabase_client),
):
    """
    SPA dostu birleşik arama sonucu döner.
    Dönüş yapısı frontend `useUnifiedSearch` beklentisiyle uyumludur:
    {
      companies: [...],
      persons: [...],
      history: [...],
      // ekstra alanlar (isteğe bağlı):
      related_companies, same_address_companies, related_persons, ocr_matches, total_matches
    }
    """
    try:
        # Geniş arama (şirket, kişi, OCR, ilişkiler)
        result = search_all_related(q, supabase)

        # History (gazette_entries) — legacy mantığa benzer basit metin araması
        # Not: Supabase tarafında unaccent kolonları yoksa normal ilike kullanılır.
        history_data: List[Dict[str, Any]] = []
        try:
            search_term = q.strip()
            search_query = f"%{search_term.replace(' ', '%')}%"
            history_filter = f"entry_type.ilike.{search_query},processed_text.ilike.{search_query}"
            history_data = (
                supabase
                .table("gazette_entries")
                .select("id, entry_type, entry_date, company_id, processed_text")
                .or_(history_filter)
                .limit(50)
                .execute()
            ).data or []
        except Exception as he:
            logger.warning(f"[Unified Search] Gazette entries query failed: {he}")
            history_data = []

        payload = {
            "companies": result.companies,
            "persons": result.persons,
            "history": history_data,
            # Ekstra zengin alanlar (SPA şu an zorunlu tutmuyor ama advance kullanım için sağlıyoruz)
            "related_companies": result.related_companies,
            "same_address_companies": result.same_address_companies,
            "related_persons": result.related_persons,
            "ocr_matches": result.ocr_matches,
            "total_matches": result.total_matches,
        }
        return payload
    except Exception as e:
        logger.error(f"Error in unified search: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/all-legacy", summary="Unified search: companies, persons, history")
def search_all_legacy(
    q: str = Query(..., min_length=2, description="Search term for companies, persons and history"),
    supabase: Client = Depends(get_supabase_client),
):
    """
    Perform a unified search across multiple entities and return a combined payload:
    {
      "companies": [...],
      "persons": [...],
      "history": [...]
    }
    """
    try:
        search_term = q.strip()
        search_query = f"%{search_term.replace(' ', '%')}%"
        logger.info(f"[Unified Search] Executing search for: {search_query}")

        # --- Companies ---
        companies_data = []
        try:
            companies_filter = f"unvan.ilike.{search_query},sicil_no.ilike.{search_query},address.ilike.{search_query}"
            companies_data = (
                supabase
                .table("companies")
                .select("*")
                .or_(companies_filter)
                .limit(50)
                .execute()
            ).data or []
        except Exception as ce:
            logger.warning(f"[Unified Search] Companies query failed: {ce}")

        # --- Persons ---
        # Try to match by full name, nationality_id, email
        persons_data = []
        try:
            persons_filter = (
                f"full_name.ilike.{search_query},"
                f"first_name.ilike.{search_query},"
                f"last_name.ilike.{search_query},"
                f"nationality_id.ilike.{search_query},"
                f"email.ilike.{search_query}"
            )
            persons_data = (
                supabase
                .table("persons")
                .select("*")
                .or_(persons_filter)
                .limit(50)
                .execute()
            ).data or []
        except Exception as pe:
            logger.warning(f"[Unified Search] Persons query failed: {pe}")

        # --- History (Gazette Entries) ---
        # Select minimal fields, including related company title if available.
        # If foreign select aliasing is unsupported, backend will still return entry fields.
        history_data = []
        try:
            history_filter = f"entry_type.ilike.{search_query},processed_text.ilike.{search_query}"
            history_data = (
                supabase
                .table("gazette_entries")
                .select("id, entry_type, entry_date, company_id, processed_text")
                .or_(history_filter)
                .limit(50)
                .execute()
            ).data or []
        except Exception as he:
            logger.warning(f"[Unified Search] Gazette entries query failed: {he}")

        payload = {
            "companies": companies_data,
            "persons": persons_data,
            "history": history_data,
        }

        logger.info(
            f"[Unified Search] Results — companies: {len(companies_data)}, persons: {len(persons_data)}, history: {len(history_data)}"
        )
        return payload

    except Exception as e:
        logger.error(f"[Unified Search] Error for query '{q}': {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An error occurred while performing unified search.")


@router.get("/company-detail", summary="Company detail with related persons and announcements")
def company_detail(
    company_id: str = Query(..., description="UUID of the company"),
    supabase: Client = Depends(get_supabase_client),
):
    """
    Fetch a single company and its related data from Supabase.
    Returns a minimal payload to drive the dashboard modal.

    {
      "company": {...},
      "persons": [{... person ..., relation fields ...}],
      "announcements": [{...}],
      "history": [{...}],  # optional gazette entries
      "related_companies": [...],
      "same_address_companies": [...]
    }
    """
    try:
        cid = company_id.strip()
        if not cid:
            raise HTTPException(status_code=422, detail="company_id is required")

        # --- Company ---
        company_resp = (
            supabase
            .table("companies")
            .select("*")
            .eq("id", cid)
            .limit(1)
            .execute()
        )
        company = (company_resp.data or [None])[0]
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")

        # --- Relations -> Person IDs and relation meta ---
        rel_resp = (
            supabase
            .table("company_person_relations")
            .select("person_id, relation_type, position, is_current, start_date, end_date")
            .eq("company_id", cid)
            .limit(200)
            .execute()
        )
        relations = rel_resp.data or []
        person_ids = [r.get("person_id") for r in relations if r.get("person_id")]

        persons = []
        if person_ids:
            # Fetch persons in batch
            persons_resp = (
                supabase
                .table("persons")
                .select("id, full_name, first_name, last_name, email, nationality_id, birth_date, is_active, updated_at")
                .in_("id", person_ids)
                .limit(500)
                .execute()
            )
            persons_map = {p["id"]: p for p in (persons_resp.data or [])}
            # Merge relation meta onto person objects
            for r in relations:
                pid = r.get("person_id")
                if pid in persons_map:
                    merged = {**persons_map[pid], **{k: v for k, v in r.items() if k != "person_id"}}
                    persons.append(merged)

        # --- Companies at the same address (exclude current company) ---
        same_address_companies = []
        if company.get('address'):
            same_address_resp = (
                supabase
                .table('companies')
                .select('*')
                .eq('address', company['address'])
                .neq('id', cid)  # Exclude current company
                .limit(50)
                .execute()
            )
            same_address_companies = same_address_resp.data or []

        # --- Related companies via shared persons ---
        related_companies = []
        try:
            if person_ids:
                # Get all other company relations for these persons
                rel_others_resp = (
                    supabase
                    .table("company_person_relations")
                    .select("company_id, person_id, relation_type, position, is_current, start_date, end_date")
                    .in_("person_id", person_ids)
                    .neq("company_id", cid)
                    .limit(1000)
                    .execute()
                )
                rel_others = rel_others_resp.data or []

                # Group by related company
                related_company_ids = []
                related_map = {}
                for ro in rel_others:
                    rcid = ro.get("company_id")
                    pid = ro.get("person_id")
                    if not rcid or not pid:
                        continue
                    if rcid not in related_map:
                        related_map[rcid] = {"company": None, "shared_persons": []}
                        related_company_ids.append(rcid)
                    # enrich person info if available
                    person_info = persons_map.get(pid, {"id": pid}) if 'persons_map' in locals() else {"id": pid}
                    related_map[rcid]["shared_persons"].append({
                        **{k: v for k, v in person_info.items() if k in ["id", "full_name", "first_name", "last_name"]},
                        "relation_type": ro.get("relation_type"),
                        "position": ro.get("position"),
                        "is_current": ro.get("is_current"),
                        "start_date": ro.get("start_date"),
                        "end_date": ro.get("end_date"),
                    })

                if related_company_ids:
                    comps_resp = (
                        supabase
                        .table("companies")
                        .select("id, unvan, sicil_no, sicil_mudurluk, address, city, district")
                        .in_("id", related_company_ids)
                        .limit(500)
                        .execute()
                    )
                    comps_map = {c["id"]: c for c in (comps_resp.data or [])}
                    for rcid in related_company_ids:
                        entry = related_map.get(rcid)
                        if entry is None:
                            continue
                        entry["company"] = comps_map.get(rcid)
                        # Flatten to a simpler structure for the API response
                        company_obj = entry["company"] or {"id": rcid}
                        related_companies.append({
                            **company_obj,
                            "shared_persons": entry["shared_persons"],
                        })
        except Exception as re:
            logger.warning(f"[Company Detail] Related companies resolution failed: {re}")

        # --- Announcements --- (fallback'lı)
        announcements = []
        try:
            ann_resp = (
                supabase
                .table("announcements")
                .select("id, title, announcement_type, publication_date, issue_number, page_number, newspaper_name, pdf_url, ocr_status, created_at, trade_registry_number")
                .eq("company_id", cid)
                .order("publication_date", desc=True)
                .limit(100)
                .execute()
            )
            announcements = ann_resp.data or []
        except Exception as _e:
            logger.warning(f"[Company Detail] announcements by company_id failed: {_e}")

        # Fallback 1: trade_registry_number == company.sicil_no
        if not announcements:
            try:
                sicil_no = company.get("sicil_no")
                if sicil_no:
                    ann_by_reg = (
                        supabase
                        .table("announcements")
                        .select("id, title, announcement_type, publication_date, issue_number, page_number, newspaper_name, pdf_url, ocr_status, created_at, trade_registry_number")
                        .eq("trade_registry_number", sicil_no)
                        .order("publication_date", desc=True)
                        .limit(100)
                        .execute()
                    )
                    announcements = ann_by_reg.data or []
                    if announcements:
                        logger.info("[Company Detail] announcements resolved via trade_registry_number fallback")
            except Exception as _e:
                logger.warning(f"[Company Detail] announcements by trade_registry_number failed: {_e}")

        # Fallback 2: title ilike %unvan%
        if not announcements:
            try:
                unvan = (company.get("unvan") or "").strip()
                if unvan:
                    pat = f"%{unvan[:60]}%"
                    ann_by_title = (
                        supabase
                        .table("announcements")
                        .select("id, title, announcement_type, publication_date, issue_number, page_number, newspaper_name, pdf_url, ocr_status, created_at, trade_registry_number")
                        .ilike("title", pat)
                        .order("publication_date", desc=True)
                        .limit(50)
                        .execute()
                    )
                    announcements = ann_by_title.data or []
                    if announcements:
                        logger.info("[Company Detail] announcements resolved via title ilike fallback")
            except Exception as _e:
                logger.warning(f"[Company Detail] announcements by title failed: {_e}")

                # --- OCR Results: persons JSON, masked_ids ve yıldızlı örüntüler ---
        try:
            ocr_resp = (
                supabase
                .table("ocr_results")
                .select("id, original_text, persons, masked_ids, created_at")
                .eq("company_id", cid)
                .order("created_at", desc=True)
                .limit(100)
                .execute()
            )
            try:
                logger.info(f"[Company Detail] OCR results fetched: count={len(ocr_resp.data or [])}")
            except Exception:
                pass

            import re
            import json
            # Tekilleştirme için isim anahtarı üretici
            def _key(n: str) -> str:
                return tr_normalize_py(n or "").strip()

            seen_names = set(_key(p.get('full_name') or f"{p.get('first_name','')} {p.get('last_name','')}") for p in persons if isinstance(p, dict))
            masked_id_set = set()
            attached_mids = set()

            for ocr in (ocr_resp.data or []):
                # 1) persons JSONB içeriği
                plist = ocr.get('persons') or []
                if isinstance(plist, list):
                    for idx, p in enumerate(plist):
                        if not isinstance(p, dict):
                            continue
                        full = (
                            p.get('full_name')
                            or (f"{p.get('first_name','')} {p.get('last_name','')}").strip()
                            or p.get('text')
                            or p.get('label')
                        )
                        if not full:
                            continue
                        # 'OCR' gibi gürültü etiketlerini temizle (bitişik/ayrı), boşlukları normalize et
                        try:
                            full = re.sub(r"(?i)ocr", "", full)
                            full = re.sub(r"\s+", " ", full).strip()
                        except Exception:
                            pass
                        k = _key(full)
                        if k in seen_names:
                            continue
                        seen_names.add(k)
                        # kişiye ait maskeler
                        p_mids = p.get('masked_ids')
                        if isinstance(p_mids, str):
                            p_mids = [p_mids]
                        # kişi maskesi yoksa OCR kaydının masked_ids'lerini kullan
                        if not isinstance(p_mids, list) or len(p_mids) == 0:
                            ocr_mids = ocr.get('masked_ids') or []
                            if isinstance(ocr_mids, list) and ocr_mids:
                                p_mids = [m for m in ocr_mids if isinstance(m, str) and '*' in m]
                        if isinstance(p_mids, list):
                            for mm in p_mids:
                                if isinstance(mm, str):
                                    masked_id_set.add(mm)
                                    attached_mids.add(mm)

                        persons.append({
                            'id': f"ocr_{ocr.get('id')}_{idx}",
                            'full_name': full,
                            'relation_type': p.get('relation_type') or p.get('role') or p.get('position') or 'OCR',
                            'position': p.get('position') or p.get('role') or None,
                            'is_current': True,
                            'source': 'OCR',
                            'masked_ids': p_mids if isinstance(p_mids, list) else [],
                        })
                        try:
                            logger.info(f"[Company Detail] OCR person added: name='{full}', mids={p_mids if isinstance(p_mids, list) else []}")
                        except Exception:
                            pass

                # 2) masked_ids JSONB içeriği
                mids = ocr.get('masked_ids') or []
                if isinstance(mids, list):
                    for midx, mid in enumerate(mids):
                        if not isinstance(mid, (str,)):
                            continue
                        if '*' not in mid:
                            continue
                        masked_id_set.add(mid)
                        # bu masked id zaten bir kişiye bağlandıysa tekrar kişi üretme
                        if mid in attached_mids:
                            continue
                        # isim yoksa masked-only kişi olarak ekle (UI'da isim bulunamadı + kimlik)
                        persons.append({
                            'id': f"ocr_mask_{ocr.get('id')}_{midx}",
                            'full_name': None,
                            'is_starred': True,
                            'relation_type': 'MASKELI_KIMLIK',
                            'is_current': True,
                            'source': 'OCR',
                            'masked_ids': [mid],
                        })
                        try:
                            logger.info(f"[Company Detail] OCR masked-only person added: mid='{mid}'")
                        except Exception:
                            pass

                # 3) original_text içinden yıldızlı örüntü
                text = ocr.get('original_text') or ''
                if text:
                    matches = re.findall(r'([A-ZĞÜŞİÖÇ]+\*+)', text)
                    for m in matches:
                        clean_name = re.sub(r'\*+', ' ', m).strip()
                        if not clean_name or len(clean_name) <= 2:
                            continue
                        k = _key(clean_name)
                        if k in seen_names:
                            continue
                        seen_names.add(k)
                        persons.append({
                            'id': f"ocr_star_{ocr.get('id')}",
                            'full_name': clean_name,
                            'is_starred': True,
                            'relation_type': 'YILDIZLI_KISI',
                            'is_current': True,
                            'source': 'OCR',
                        })

        except Exception as e:
            logger.warning(f"[Company Detail] Error processing OCR results: {e}")

        # Kişi listesinde son temizlik
        try:
            cleaned_persons = []
            for p in (persons or []):
                if not isinstance(p, dict):
                    continue
                nm = p.get('full_name')
                if isinstance(nm, str):
                    try:
                        nm = re.sub(r"(?i)ocr", "", nm)
                        nm = re.sub(r"\s+", " ", nm).strip()
                    except Exception:
                        pass
                    if not nm:
                        nm = 'Ad Bilinmiyor'
                    p['full_name'] = nm
                cleaned_persons.append(p)
            persons = cleaned_persons
            try:
                preview = [{k: v for k, v in p.items() if k in ['full_name', 'masked_ids', 'source']} for p in persons[:5]]
                logger.info(f"[Company Detail] persons after cleanup (preview): {preview}")
            except Exception:
                pass
        except Exception as e:
            logger.warning(f"[Company Detail] persons cleanup failed: {e}")

        # OCR tabanlı ilişkiler: aynı isim + masked_id'yi paylaşan farklı şirketler (öncelik)
        try:
            if 'related_companies' not in locals():
                related_companies = []
            existing_related_ids = {rc.get('id') for rc in related_companies if isinstance(rc, dict)}
            # 1) kişi listesinde OCR kaynaklı {isim + masked_id} çiftlerini çıkar
            candidate_pairs = set()
            for p in (persons or []):
                if not isinstance(p, dict):
                    continue
                if p.get('source') != 'OCR':
                    continue
                nm = (p.get('full_name') or '').strip()
                if not nm or '*' in nm:
                    continue
                mids = p.get('masked_ids') or []
                if isinstance(mids, list):
                    for mm in mids:
                        if isinstance(mm, str) and '*' in mm:
                            candidate_pairs.add((tr_normalize_py(nm), mm))

            logger.info(f"[Company Detail] OCR candidates: masked_id_set={len(masked_id_set)} (sample={list(masked_id_set)[:5]})")
            # 2) Önce isim+maskeye göre ilişkili şirketleri bul
            for (nm_norm, mid) in list(candidate_pairs)[:10]:
                try:
                    occ = (
                        supabase
                        .table("ocr_results")
                        .select("id, company_id, masked_ids, persons, companies(*)")
                        .filter("masked_ids", "cs", json.dumps([mid]))
                        .limit(50)
                        .execute()
                    )
                except Exception as _e:
                    logger.warning(f"[Company Detail] OCR contains query (name+mask) failed for {mid}: {_e}")
                    continue
                for row in (occ.data or []):
                    rcid = row.get('company_id')
                    if not rcid or rcid == cid or rcid in (existing_related_ids or set()):
                        continue
                    # isim doğrulaması: row.persons içinde aynı isim var mı?
                    row_persons = row.get('persons') or []
                    found_same_name = False
                    matched_name = None
                    if isinstance(row_persons, list):
                        for rp in row_persons:
                            if not isinstance(rp, dict):
                                continue
                            rp_full = (
                                rp.get('full_name')
                                or (f"{rp.get('first_name','')} {rp.get('last_name','')}").strip()
                                or rp.get('text')
                                or rp.get('label')
                            )
                            if not rp_full:
                                continue
                            try:
                                rp_full = re.sub(r"(?i)ocr", "", rp_full)
                                rp_full = re.sub(r"\s+", " ", rp_full).strip()
                            except Exception:
                                pass
                            rp_norm = tr_normalize_py(rp_full)
                            # eşleştirme: eşitlik veya içerme veya en az iki ortak token
                            if rp_norm == nm_norm or (rp_norm in nm_norm) or (nm_norm in rp_norm):
                                found_same_name = True
                                matched_name = rp_full
                                break
                            else:
                                rp_toks = [t for t in rp_norm.split() if t]
                                nm_toks = [t for t in nm_norm.split() if t]
                                if len(set(rp_toks).intersection(nm_toks)) >= 2:
                                    found_same_name = True
                                    matched_name = rp_full
                                    break
                    if not found_same_name:
                        continue
                    comp_obj = row.get('companies') if isinstance(row.get('companies'), dict) else None
                    # companies(*) çalışmadıysa Companies tablosundan tekil çekmeye çalış
                    if not comp_obj:
                        try:
                            comp_q = (
                                supabase
                                .table("companies")
                                .select("id, unvan, sicil_no, address, sicil_mudurluk")
                                .eq("id", rcid)
                                .limit(1)
                                .execute()
                            )
                            comp_obj = (comp_q.data or [None])[0]
                        except Exception:
                            comp_obj = None
                    shared = [{'full_name': matched_name if found_same_name else None, 'masked_ids': [mid], 'relation_type': 'OCR_ORTAK', 'is_current': True}]
                    related_companies.append({
                        **(comp_obj or {'id': rcid}),
                        'shared_persons': shared,
                    })
                    existing_related_ids.add(rcid)
                    try:
                        logger.info(f"[Company Detail] related (name+mask): rcid={rcid}, shared={shared}")
                    except Exception:
                        pass

            logger.info(f"[Company Detail] OCR candidate_pairs={len(candidate_pairs)} (sample={list(candidate_pairs)[:5]})")

            # İsim+maskeden isim sözlüğü oluştur (fallback'te kullanmak için)
            name_by_mid: dict[str, str] = {}
            try:
                for p in (persons or []):
                    if not isinstance(p, dict):
                        continue
                    if p.get('source') != 'OCR':
                        continue
                    nm = (p.get('full_name') or '').strip()
                    if not nm or '*' in nm:
                        continue
                    mids = p.get('masked_ids') or []
                    if isinstance(mids, list):
                        for mm in mids:
                            if isinstance(mm, str) and '*' in mm and mm not in name_by_mid:
                                name_by_mid[mm] = nm
            except Exception:
                pass

            # 3) Son olarak yalnızca masked_id ortaklığına göre (fallback)
            for mid in list(masked_id_set)[:20]:  # performans için ilk 20 maske
                try:
                    occ = (
                        supabase
                        .table("ocr_results")
                        .select("id, company_id, masked_ids, persons, companies(*)")
                        .filter("masked_ids", "cs", json.dumps([mid]))
                        .limit(50)
                        .execute()
                    )
                except Exception as _e:
                    logger.warning(f"[Company Detail] OCR contains query failed for {mid}: {_e}")
                    continue
                for row in (occ.data or []):
                    rcid = row.get('company_id')
                    if not rcid or rcid == cid or rcid in (existing_related_ids or set()):
                        continue
                    comp_obj = row.get('companies') if isinstance(row.get('companies'), dict) else None
                    shared_name = name_by_mid.get(mid)
                    shared = [{'full_name': shared_name, 'masked_ids': [mid], 'relation_type': 'MASK_MATCH', 'is_current': True}]
                    related_companies.append({
                        **(comp_obj or {'id': rcid}),
                        'shared_persons': shared,
                    })
                    existing_related_ids.add(rcid)

                # Ek: persons JSON içinde masked_ids içeren kayıtları da ara (string veya liste)
                occ2_data = []
                try:
                    occ2a = (
                        supabase
                        .table("ocr_results")
                        .select("id, company_id, persons, companies(*)")
                        .filter("persons", "cs", json.dumps([{"masked_ids": mid}]))
                        .limit(50)
                        .execute()
                    )
                    occ2_data.extend(occ2a.data or [])
                except Exception as _e2a:
                    logger.warning(f"[Company Detail] OCR persons contains (string) failed for {mid}: {_e2a}")
                try:
                    occ2b = (
                        supabase
                        .table("ocr_results")
                        .select("id, company_id, persons, companies(*)")
                        .filter("persons", "cs", json.dumps([{"masked_ids": [mid]}]))
                        .limit(50)
                        .execute()
                    )
                    occ2_data.extend(occ2b.data or [])
                except Exception as _e2b:
                    logger.warning(f"[Company Detail] OCR persons contains (list) failed for {mid}: {_e2b}")

                seen_rc_in_occ2 = set()
                for row in occ2_data:
                    rcid = row.get('company_id')
                    if not rcid or rcid == cid or rcid in (existing_related_ids or set()) or rcid in seen_rc_in_occ2:
                        continue
                    comp_obj = row.get('companies') if isinstance(row.get('companies'), dict) else None
                    related_companies.append({
                        **(comp_obj or {'id': rcid}),
                        'shared_persons': [{'full_name': None, 'masked_ids': [mid], 'relation_type': 'MASK_IN_PERSONS', 'is_current': True}],
                    })
                    existing_related_ids.add(rcid)
                    seen_rc_in_occ2.add(rcid)
        except Exception as e:
            logger.warning(f"[Company Detail] OCR-based related companies failed: {e}")

        # Announcements boşsa, OCR snippet'larından pseudo-ilan üret
        try:
            if not announcements:
                ann_from_ocr = []
                for ocr in (ocr_resp.data or [])[:5]:
                    txt = (ocr.get('original_text') or '').strip()
                    if not txt:
                        continue
                    first_line = txt.splitlines()[0][:140]
                    ann_from_ocr.append({
                        'id': f"ocr-{ocr.get('id')}",
                        'title': first_line or 'OCR Snippet',
                        'announcement_type': 'OCR_SNIPPET',
                        'publication_date': None,
                        'issue_number': None,
                        'page_number': None,
                        'newspaper_name': 'OCR',
                        'pdf_url': None,
                        'ocr_status': 'extracted',
                        'created_at': None,
                        'trade_registry_number': company.get('sicil_no'),
                    })
                if ann_from_ocr:
                    announcements = ann_from_ocr
        except Exception as e:
            logger.warning(f"[Company Detail] OCR-based announcement fallback failed: {e}")

        # Hala boşsa, gazette_entries'den pseudo-ilan üret
        try:
            if not announcements:
                # gazette_entries henüz yoksa şimdi çek
                if 'gazette_entries' not in locals() or not gazette_entries:
                    try:
                        hist_resp2 = (
                            supabase
                            .table("gazette_entries")
                            .select("id, entry_type, entry_date, processed_text, company_id")
                            .eq("company_id", cid)
                            .order("entry_date", desc=True)
                            .limit(100)
                            .execute()
                        )
                        gazette_entries = hist_resp2.data or []
                    except Exception as _e:
                        logger.warning(f"[Company Detail] Gazette fetch inside fallback failed: {_e}")
                        gazette_entries = []

                ann_from_hist = []
                for ge in (gazette_entries or [])[:5]:
                    pt = (ge.get('processed_text') or '').strip()
                    title = (pt.splitlines()[0] if pt else '')[:140] or 'Gazete Kayıtı'
                    ann_from_hist.append({
                        'id': f"ge-{ge.get('id')}",
                        'title': title,
                        'announcement_type': 'GAZETTE_ENTRY',
                        'publication_date': ge.get('entry_date'),
                        'issue_number': None,
                        'page_number': None,
                        'newspaper_name': 'Gazette',
                        'pdf_url': None,
                        'ocr_status': None,
                        'created_at': None,
                        'trade_registry_number': company.get('sicil_no'),
                    })
                if ann_from_hist:
                    announcements = ann_from_hist
        except Exception as e:
            logger.warning(f"[Company Detail] Gazette-entry announcement fallback failed: {e}")

        # --- History (gazette_entries) --- optional
        gazette_entries = []
        try:
            hist_resp = (
                supabase
                .table("gazette_entries")
                .select("id, entry_type, entry_date, processed_text, company_id")
                .eq("company_id", cid)
                .order("entry_date", desc=True)
                .limit(100)
                .execute()
            )
            gazette_entries = hist_resp.data or []
        except Exception as e:
            logger.warning(f"[Company Detail] Error fetching gazette entries: {e}")
            gazette_entries = []

        return {
            "company": company,
            "persons": persons,
            "announcements": announcements,
            "gazette_entries": gazette_entries,
            "related_companies": related_companies,
            "same_address_companies": same_address_companies,
        }

    except HTTPException as he:
        raise
    except Exception as e:
        logger.error(f"[Company Detail] Error for company_id '{company_id}': {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An error occurred while fetching company detail.")
