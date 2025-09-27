from fastapi import APIRouter, Depends, HTTPException, Query, Request
from supabase import Client
from typing import List, Dict, Any, Optional, Set
from pydantic import BaseModel, Field
import os
import requests
from datetime import datetime
import re
import json
import unicodedata
import logging
import time
import threading
from collections import deque
from app.core.dependencies import get_supabase_client
from app.api.deps import enforce_daily_limit
from app.core.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)

# --- Config helpers ---
def _int_from_settings_or_env(attr_name: str, env_names: list[str], default: int) -> int:
    try:
        start_ts = time.perf_counter()
        val = getattr(settings, attr_name)
        if isinstance(val, (int,)):
            return int(val)
    except Exception:
        pass
    for name in env_names:
        # check both exact and upper-case variant
        for key in {name, name.upper()}:
            raw = os.getenv(key)
            if raw is not None and str(raw).strip() != "":
                try:
                    return int(str(raw).strip())
                except Exception:
                    continue
    return int(default)

def _clamp(v: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, int(v)))

# Arama sonuçlarındaki şirket sayısı sınırı (settings/env ile yönetilebilir)
MAX_COMPANIES = _clamp(
    _int_from_settings_or_env(
        "search_max_companies",
        ["tsg_search_max_companies", "SEARCH_MAX_COMPANIES", "TSG_SEARCH_MAX_COMPANIES"],
        20,
    ),
    1,
    200,
)

# --- Simple in-memory TTL cache (env: SEARCH_CACHE_TTL_SECONDS) ---
class SimpleTTLCache:
    def __init__(self, ttl_seconds: int):
        self.ttl = max(0, ttl_seconds)
        self._store: Dict[str, Any] = {}
        self._lock = threading.Lock()

    def get(self, key: str):
        if self.ttl <= 0:
            return None
        now = time.time()
        with self._lock:
            item = self._store.get(key)
            if not item:
                return None
            exp, val = item
            if exp < now:
                self._store.pop(key, None)
                return None
            return val

    def set(self, key: str, value: Any):
        if self.ttl <= 0:
            return
        exp = time.time() + self.ttl
        with self._lock:
            self._store[key] = (exp, value)

SEARCH_CACHE_TTL_SECONDS = max(0, _int_from_settings_or_env(
    "search_cache_ttl_seconds",
    ["tsg_search_cache_ttl_seconds", "SEARCH_CACHE_TTL_SECONDS", "TSG_SEARCH_CACHE_TTL_SECONDS"],
    30,
))
_cache_all = SimpleTTLCache(SEARCH_CACHE_TTL_SECONDS)
_cache_all_legacy = SimpleTTLCache(SEARCH_CACHE_TTL_SECONDS)


# --- Very simple per-IP rate limiter (env: SEARCH_RATE_LIMIT_RPM) ---
class RateLimiter:
    def __init__(self, rpm: int = 120, window: int = 60):
        self.limit = max(0, rpm)
        self.window = max(1, window)
        self._buckets: Dict[str, deque] = {}
        self._lock = threading.Lock()

    def check(self, ip: str):
        if self.limit == 0:
            return  # disabled
        now = time.time()
        with self._lock:
            dq = self._buckets.get(ip)
            if dq is None:
                dq = deque()
                self._buckets[ip] = dq
            # evict old
            cutoff = now - self.window
            while dq and dq[0] < cutoff:
                dq.popleft()
            if len(dq) >= self.limit:
                raise HTTPException(
                    status_code=429,
                    detail="Arama oran sınırı aşıldı. Lütfen kısa bir süre sonra tekrar deneyin.",
                    headers={"Retry-After": str(int(self.window))},
                )
            dq.append(now)

SEARCH_RATE_LIMIT_RPM = max(0, _int_from_settings_or_env(
    "search_rate_limit_rpm",
    ["tsg_search_rate_limit_rpm", "SEARCH_RATE_LIMIT_RPM", "TSG_SEARCH_RATE_LIMIT_RPM"],
    0,
))
_limiter = RateLimiter(SEARCH_RATE_LIMIT_RPM, 60)

# Proximity thresholds (configurable)
SEARCH_PROXIMITY_STRONG = max(1, _int_from_settings_or_env(
    "search_proximity_strong",
    ["tsg_search_proximity_strong", "SEARCH_PROXIMITY_STRONG", "TSG_SEARCH_PROXIMITY_STRONG"],
    8,
))
SEARCH_PROXIMITY_MEDIUM = max(SEARCH_PROXIMITY_STRONG + 1, _int_from_settings_or_env(
    "search_proximity_medium",
    ["tsg_search_proximity_medium", "SEARCH_PROXIMITY_MEDIUM", "TSG_SEARCH_PROXIMITY_MEDIUM"],
    20,
))
SEARCH_PROXIMITY_WEAK = max(SEARCH_PROXIMITY_MEDIUM + 1, _int_from_settings_or_env(
    "search_proximity_weak",
    ["tsg_search_proximity_weak", "SEARCH_PROXIMITY_WEAK", "TSG_SEARCH_PROXIMITY_WEAK"],
    40,
))

# Simple synonym map (normalized) — 81 il + kısa varyantlar (3 harf kısaltma)
_CITY_SYNONYMS = {
    "adana": {"adana", "adn"},
    "adiyaman": {"adiyaman", "ady"},
    "afyonkarahisar": {"afyonkarahisar", "afyon", "afy"},
    "agri": {"agri", "agr"},
    "amasya": {"amasya", "ams"},
    "ankara": {"ankara", "ank"},
    "antalya": {"antalya", "ant"},
    "artvin": {"artvin", "art"},
    "aydin": {"aydin", "ayd"},
    "balikesir": {"balikesir", "blk"},
    "bilecik": {"bilecik", "blc"},
    "bingol": {"bingol", "bng"},
    "bitlis": {"bitlis", "btl"},
    "bolu": {"bolu", "blu"},
    "burdur": {"burdur", "brd"},
    "bursa": {"bursa", "brs"},
    "canakkale": {"canakkale", "cnk"},
    "cankiri": {"cankiri", "ckr"},
    "corum": {"corum", "crm"},
    "denizli": {"denizli", "dnz"},
    "diyarbakir": {"diyarbakir", "diy"},
    "edirne": {"edirne", "edr"},
    "elazig": {"elazig", "elz"},
    "erzincan": {"erzincan", "erc"},
    "erzurum": {"erzurum", "erz"},
    "eskisehir": {"eskisehir", "esk"},
    "gaziantep": {"gaziantep", "gaz"},
    "giresun": {"giresun", "grs"},
    "gumushane": {"gumushane", "gms"},
    "hakkari": {"hakkari", "hkr"},
    "hatay": {"hatay", "hty"},
    "isparta": {"isparta", "isp"},
    "mersin": {"mersin", "mrs", "icel"},
    "istanbul": {"istanbul", "ist"},
    "izmir": {"izmir", "izm"},
    "kars": {"kars", "krs"},
    "kastamonu": {"kastamonu", "ksm"},
    "kayseri": {"kayseri", "kys"},
    "kirklareli": {"kirklareli", "kkl"},
    "kirsehir": {"kirsehir", "ksh"},
    "kocaeli": {"kocaeli", "kcl"},
    "konya": {"konya", "kny"},
    "kutahya": {"kutahya", "kty"},
    "malatya": {"malatya", "mal"},
    "manisa": {"manisa", "man"},
    "kahramanmaras": {"kahramanmaras", "maras", "kmar"},
    "mardin": {"mardin", "mrn"},
    "mugla": {"mugla", "mgl"},
    "mus": {"mus", "mus"},
    "nevsehir": {"nevsehir", "nvs"},
    "nigde": {"nigde", "ngd"},
    "ordu": {"ordu", "ord"},
    "rize": {"rize", "rze"},
    "sakarya": {"sakarya", "sky"},
    "samsun": {"samsun", "sam"},
    "siirt": {"siirt", "srt"},
    "sinop": {"sinop", "sin"},
    "sivas": {"sivas", "siv"},
    "tekirdag": {"tekirdag", "tgd"},
    "tokat": {"tokat", "tok"},
    "trabzon": {"trabzon", "trb"},
    "tunceli": {"tunceli", "tnc"},
    "sanliurfa": {"sanliurfa", "urfa", "san"},
    "usak": {"usak", "usk"},
    "van": {"van", "van"},
    "yozgat": {"yozgat", "yoz"},
    "zonguldak": {"zonguldak", "zon"},
    "aksaray": {"aksaray", "aks"},
    "bayburt": {"bayburt", "byb"},
    "karaman": {"karaman", "krm"},
    "kirikkale": {"kirikkale", "kkl"},
    "batman": {"batman", "btm"},
    "sirnak": {"sirnak", "srn"},
    "bartin": {"bartin", "brt"},
    "ardahan": {"ardahan", "ard"},
    "igdir": {"igdir", "igd"},
    "yalova": {"yalova", "ylv"},
    "karabuk": {"karabuk", "krb"},
    "kilis": {"kilis", "kls"},
    "osmaniye": {"osmaniye", "osm"},
    "duzce": {"duzce", "dzc"},
}

def _token_variants(t: str) -> set:
    base = tr_normalize_py(t)
    out = {base}
    # City synonyms
    for canon, variants in _CITY_SYNONYMS.items():
        if base == canon or base in variants:
            out |= {canon} | set(variants)
            break
    # Common suffix handling for province/district phrases
    # e.g., "ankara il", "ankara ilce", "ankara ilçe", "ankara merkez", "ankara sehir/şehir"
    suffixes = [" il", " ilce", " ilçe", " merkez", " sehir", " sehir", " sehir merkezi", " şehir", " şehir merkezi"]
    for sfx in suffixes:
        if base.endswith(sfx.strip()):
            trimmed = base.replace(sfx.strip(), "").strip()
            if trimmed:
                out.add(trimmed)
    return out

class SearchResult(BaseModel):
    companies: List[Dict[str, Any]] = Field(default_factory=list)
    persons: List[Dict[str, Any]] = Field(default_factory=list)
    announcements: List[Dict[str, Any]] = Field(default_factory=list)
    related_companies: List[Dict[str, Any]] = Field(default_factory=list)
    same_address_companies: List[Dict[str, Any]] = Field(default_factory=list)
    related_persons: List[Dict[str, Any]] = Field(default_factory=list)
    ocr_matches: List[Dict[str, Any]] = Field(default_factory=list)
    total_matches: int = 0

# Config visibility
logger.info(
    f"[Search Config] MAX_COMPANIES={MAX_COMPANIES}, CACHE_TTL={SEARCH_CACHE_TTL_SECONDS}s, RATE_LIMIT_RPM={SEARCH_RATE_LIMIT_RPM}"
)


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
    total_companies_pre_count: Optional[int] = None  # dilimlemeden önce toplam şirket sayısı
    q_raw = (query or "").strip()
    q_norm = tr_normalize_py(q_raw)
    tokens = [t for t in re.split(r"\s+", q_norm) if t]
    tokens_letters = [tr_letters_digits(t) for t in tokens if tr_letters_digits(t)]
    # Sayı odaklı aramalar için rakamları soy: MERSİS alt-dize aramasını hızlandırmak için
    q_digits = re.sub(r"\D+", "", (query or ""))

    # Hızlı yol: Saf sayısal ve yeterince uzun sorgu ise doğrudan OCR (mersis_no, original_text) ve kimlik numarası taraması
    try:
        # Tüm sorgu sadece rakamlardan oluşuyorsa ve uzunluğu >=6 ise hızlı yol devreye girsin.
        pure_digits = bool(re.fullmatch(r"\d{6,}", q_raw))
        if pure_digits:
            # Skor tabloları ve kaynak bayrakları
            score_map: Dict[str, int] = {}
            def bump(cid: str, val: int):
                prev = score_map.get(cid, 0)
                if val > prev:
                    score_map[cid] = val

            # 0) Companies: mersis_number ve sicil_no içinde alt-dize
            comp_hits_ids: Set[str] = set()
            try:
                c_mersis = (
                    supabase.table("companies").select("id, unvan, mersis_number")
                    .like("mersis_number", f"%{q_digits}%").limit(500).execute()
                ).data or []
                for r in c_mersis:
                    cid = r.get("id")
                    if cid:
                        comp_hits_ids.add(cid)
                        bump(cid, 90)  # companies.mersis_number eşleşmesi: güçlü
            except Exception:
                pass
            try:
                c_sicil = (
                    supabase.table("companies").select("id, unvan, sicil_no")
                    .like("sicil_no", f"%{q_digits}%").limit(500).execute()
                ).data or []
                for r in c_sicil:
                    cid = r.get("id")
                    if cid:
                        comp_hits_ids.add(cid)
                        bump(cid, max(score_map.get(cid, 0), 70))  # sicil_no: orta-güçlü
            except Exception:
                pass

            # 1) OCR'da mersis_no ve original_text
            ocr_company_ids: Set[str] = set()
            ocr_mersis_map: Dict[str, str] = {}
            ocr_trade_map: Dict[str, str] = {}
            try:
                ocr_rows = (
                    supabase
                    .table("ocr_results")
                    .select("id, company_id, mersis_no, trade_name")
                    .or_(f"mersis_no.like.%{q_digits}%,original_text.like.%{q_digits}%")
                    .limit(2000)
                    .execute()
                ).data or []
            except Exception:
                ocr_rows = []

            if not ocr_rows:
                # Python tarafı fallback — Supabase'in varsayılan 1000 satır limitini aşmak için sayfalama
                try:
                    batch = 1000
                    max_pages = 20  # en fazla 20k satır tarar
                    page = 0
                    while page < max_pages:
                        start = page * batch
                        end = start + batch - 1
                        q = (
                            supabase
                            .table("ocr_results")
                            .select("id, company_id, mersis_no, trade_name, original_text")
                            .order("id", desc=True)
                            .range(start, end)
                            .execute()
                        )
                        rows = q.data or []
                        if not rows:
                            break
                        for r in rows:
                            cid = r.get("company_id")
                            if not cid:
                                continue
                            text = r.get("original_text") or ""
                            mers = r.get("mersis_no") or ""
                            if (q_digits in text) or (q_digits in mers):
                                ocr_company_ids.add(cid)
                                if r.get("mersis_no") and not ocr_mersis_map.get(cid):
                                    ocr_mersis_map[cid] = r["mersis_no"]
                                    bump(cid, max(score_map.get(cid, 0), 80))
                                if q_digits in text:
                                    bump(cid, max(score_map.get(cid, 0), 60))
                                if r.get("trade_name") and not ocr_trade_map.get(cid):
                                    ocr_trade_map[cid] = r["trade_name"]
                        if len(rows) < batch:
                            break
                        page += 1
                except Exception:
                    pass
            else:
                for r in ocr_rows:
                    cid = r.get("company_id")
                    if cid:
                        ocr_company_ids.add(cid)
                        if r.get("mersis_no") and not ocr_mersis_map.get(cid):
                            ocr_mersis_map[cid] = r["mersis_no"]
                            bump(cid, max(score_map.get(cid, 0), 80))  # OCR.mersis_no
                        # original_text içinde sayısal alt-dize eşleşmesini doğrudan tespit edemiyoruz;
                        # ancak bu sorgu zaten OR ile geldiği için en az orta skor veriyoruz.
                        bump(cid, max(score_map.get(cid, 0), 60))  # OCR.original_text
                        if r.get("trade_name") and not ocr_trade_map.get(cid):
                            ocr_trade_map[cid] = r.get("trade_name")

            # Şirketleri getir: tüm kaynaklardan toplanan adaylar üzerinden (skor map anahtarlarının birliği)
            companies_fast: List[Dict[str, Any]] = []

            # Kişiler: kimlik numarası alt-dize
            persons_fast: List[Dict[str, Any]] = []
            try:
                persons_fast = (
                    supabase.table("persons").select("*").like("nationality_id", f"%{q_digits}%").limit(500).execute()
                ).data or []
            except Exception:
                pass

            # 2.5) Kişiler -> ilişkili şirketlere düşük-orta skor ver
            try:
                if persons_fast:
                    pids = [p.get("id") for p in persons_fast if p.get("id")]
                    if pids:
                        rels = (
                            supabase
                            .table("company_person_relations")
                            .select("company_id, person_id")
                            .in_("person_id", pids)
                            .limit(5000)
                            .execute()
                        ).data or []
                        for r in rels:
                            cid = r.get("company_id")
                            if cid:
                                bump(cid, max(score_map.get(cid, 0), 50))
            except Exception:
                pass

            # 2.6) 11 haneli kimlik için OCR masked_ids üzerinden aday şirketleri bul (maskeleri türet)
            try:
                if len(q_digits) == 11:
                    def gen_masks(tckn: str) -> List[str]:
                        out = []
                        n = len(tckn)
                        for pre in range(1, 5):
                            for suf in range(1, 4):
                                if pre + suf < n:
                                    stars = n - (pre + suf)
                                    out.append(tckn[:pre] + ("*" * stars) + tckn[-suf:])
                        # tipik maske öne al
                        pref = tckn[:3] + ("*" * 6) + tckn[-2:]
                        if pref not in out:
                            out.insert(0, pref)
                        return out[:8]  # ilk 8 varyant ile sınırla
                    masks = gen_masks(q_digits)
                    ocr_mask_ids: Set[str] = set()
                    for msk in masks:
                        try:
                            r1 = (
                                supabase
                                .table("ocr_results")
                                .select("company_id, masked_ids")
                                .filter("masked_ids", "cs", json.dumps([msk]))
                                .limit(500)
                                .execute()
                            ).data or []
                            for r in r1:
                                cid = r.get("company_id")
                                if cid:
                                    ocr_mask_ids.add(cid)
                            r2 = (
                                supabase
                                .table("ocr_results")
                                .select("company_id, persons")
                                .filter("persons", "cs", json.dumps([{"masked_ids": msk}]))
                                .limit(500)
                                .execute()
                            ).data or []
                            for r in r2:
                                cid = r.get("company_id")
                                if cid:
                                    ocr_mask_ids.add(cid)
                        except Exception:
                            continue
                    for cid in ocr_mask_ids:
                        bump(cid, max(score_map.get(cid, 0), 70))  # OCR.masked_ids: güçlü-orta
            except Exception:
                pass

            # Sonucu topla ve dön
            # 2.7) Aday şirketleri birleştir ve getir
            try:
                candidate_ids: Set[str] = set(score_map.keys())
                # Eğer yalnız OCR company_id'leri varsa ve skor yazılmadıysa yine de ekle
                candidate_ids.update(ocr_company_ids)
                if candidate_ids:
                    comp_resp2 = (
                        supabase
                        .table("companies")
                        .select("*")
                        .in_("id", list(candidate_ids))
                        .limit(min(2000, len(candidate_ids)))
                        .execute()
                    )
                    fetched2 = comp_resp2.data or []
                else:
                    fetched2 = []
            except Exception:
                fetched2 = []

            fetched2_map = {c.get("id"): c for c in fetched2 if isinstance(c, dict) and c.get("id")}
            for cid in (candidate_ids if 'candidate_ids' in locals() else set()):
                if cid in fetched2_map:
                    companies_fast.append(dict(fetched2_map[cid]))
                else:
                    # Minimal obje (nadiren companies'de yoksa)
                    companies_fast.append({
                        "id": cid,
                        "unvan": ocr_trade_map.get(cid),
                        "unvan_ocr": ocr_trade_map.get(cid),
                        "mersis_number_ocr": ocr_mersis_map.get(cid),
                    })

            # 3) match_strength alanını set et ve sırala
            for obj in companies_fast:
                cid = obj.get("id")
                if cid:
                    obj["match_strength"] = score_map.get(cid, obj.get("match_strength", 0))
            companies_fast.sort(key=lambda x: x.get("match_strength", 0), reverse=True)
            total_companies_pre = len(companies_fast)
            companies_fast = companies_fast[:MAX_COMPANIES]

            result.companies = companies_fast
            result.persons = persons_fast
            result.ocr_matches = []
            result.related_companies = []
            result.same_address_companies = []
            result.total_matches = total_companies_pre + len(persons_fast)
            logger.info(f"[Search Fast Numeric] companies={len(companies_fast)} persons={len(persons_fast)} for q={q_digits}")
            return result
    except Exception:
        pass

    # Hızlı yol: Maskeli arama (en az 3 yıldız içeriyorsa)
    try:
        has_mask = q_raw.count("*") >= 3
        if has_mask:
            # KURAL: asla '*' ibaresi üzerinden OCR araması yapılmaz.
            # Sadece maskeden çıkan sayısal prefix/suffix ile kişilerde arama yapılır ve ilişkili şirketler bulunur.
            ocr_company_ids: Set[str] = set()  # bu hızlı yolda OCR kullanılmıyor
            ocr_trade_map: Dict[str, str] = {}
            ocr_mersis_map: Dict[str, str] = {}

            # 1) Persons: maskeden prefix/suffix çıkar ve nationality_id LIKE uygula
            persons_ids: Set[str] = set()
            try:
                import re as _re
                parts = _re.split(r"\*+", q_raw)
                pre = (parts[0] if parts else "")
                suf = (parts[-1] if parts else "")
                pre_d = _re.sub(r"\D+", "", pre)
                suf_d = _re.sub(r"\D+", "", suf)
                pattern = None
                if pre_d and suf_d:
                    pattern = f"%{pre_d}%{suf_d}%"
                elif pre_d:
                    pattern = f"%{pre_d}%"
                elif suf_d:
                    pattern = f"%{suf_d}%"
                if pattern:
                    persons_rows = (
                        supabase
                        .table("persons")
                        .select("id")
                        .like("nationality_id", pattern)
                        .limit(1000)
                        .execute()
                    ).data or []
                    for p in persons_rows:
                        if p.get("id"):
                            persons_ids.add(p["id"])
            except Exception:
                pass

            # 2) Persons -> relations -> company_ids
            rel_company_ids: Set[str] = set()
            try:
                if persons_ids:
                    rels = (
                        supabase
                        .table("company_person_relations")
                        .select("company_id, person_id")
                        .in_("person_id", list(persons_ids))
                        .limit(5000)
                        .execute()
                    ).data or []
                    for r in rels:
                        cid = r.get("company_id")
                        if cid:
                            rel_company_ids.add(cid)
            except Exception:
                pass

            # 2.1) OCR masked_ids: doğrudan input maskesi ile eşleşen şirketleri bul (original_text taraması yapmadan)
            ocr_mask_company_ids: Set[str] = set()
            try:
                # masked_ids dizisi doğrudan bu maskeyi içeriyor mu?
                m1 = (
                    supabase
                    .table("ocr_results")
                    .select("company_id, masked_ids")
                    .filter("masked_ids", "cs", json.dumps([q_raw]))
                    .limit(2000)
                    .execute()
                ).data or []
                for r in m1:
                    cid = r.get("company_id")
                    if cid:
                        ocr_mask_company_ids.add(cid)
                # persons JSON'i içinde masked_ids alanında bu maske geçiyor mu?
                m2 = (
                    supabase
                    .table("ocr_results")
                    .select("company_id, persons")
                    .filter("persons", "cs", json.dumps([{"masked_ids": q_raw}]))
                    .limit(2000)
                    .execute()
                ).data or []
                for r in m2:
                    cid = r.get("company_id")
                    if cid:
                        ocr_mask_company_ids.add(cid)
            except Exception:
                pass

            # 3) Topla ve tekilleştir
            all_cids = set()
            all_cids.update(ocr_company_ids)
            all_cids.update(rel_company_ids)
            all_cids.update(ocr_mask_company_ids)

            companies_fast: List[Dict[str, Any]] = []
            if all_cids:
                try:
                    comp_resp = (
                        supabase
                        .table("companies")
                        .select("*")
                        .in_("id", list(all_cids))
                        .limit(1000)
                        .execute()
                    )
                    fetched = comp_resp.data or []
                except Exception:
                    fetched = []
                fetched_map = {c.get("id"): c for c in fetched if isinstance(c, dict) and c.get("id")}
                for cid in all_cids:
                    if cid in fetched_map:
                        obj = dict(fetched_map[cid])
                        # OCR masked_ids ile eşleştiyse daha yüksek skor ver; aksi halde kişi maskesi skoru
                        obj["match_strength"] = 70 if cid in ocr_mask_company_ids else 40
                        companies_fast.append(obj)
                    else:
                        companies_fast.append({
                            "id": cid,
                            "unvan": ocr_trade_map.get(cid),
                            "unvan_ocr": ocr_trade_map.get(cid),
                            "mersis_number_ocr": ocr_mersis_map.get(cid),
                            "match_strength": 70 if cid in ocr_mask_company_ids else 40,
                        })

            # 4) Skora göre sırala (yüksekten düşüğe)
            companies_fast.sort(key=lambda x: x.get("match_strength", 0), reverse=True)
            total_companies_pre = len(companies_fast)
            companies_fast = companies_fast[:MAX_COMPANIES]

            result.companies = companies_fast
            result.persons = []  # maskeli aramada ek kişi detayı döndürmüyoruz; istenirse genişletilir
            result.ocr_matches = []
            result.related_companies = []
            result.same_address_companies = []
            result.total_matches = total_companies_pre
            logger.info(f"[Search Fast Mask] companies={len(companies_fast)} for q='{q_raw}'")
            return result
    except Exception:
        pass

    # Akıllı karma arama: hem rakam hem metin tokenları varsa, aynı kayıtta ikisinin de bulunmasını şart koş
    try:
        has_digits = bool(q_digits)
        has_text_tokens = len(tokens) > 0
        if has_digits and has_text_tokens:
            # Supabase tarafında geniş OR ile adayları getir, Python tarafında AND filtresi uygula
            try:
                conds = [
                    f"sicil_no.ilike.%{q_digits}%",
                ]
                # opsiyonel kolon olabilir
                conds.append(f"mersis_number.ilike.%{q_digits}%")
                for t in tokens:
                    vars_t = list(_token_variants(t))[:3]
                    for v in vars_t:
                        pat = f"%{v}%"
                        conds.extend([
                            f"unvan_unaccent.ilike.{pat}",
                            f"firma_unvani_unaccent.ilike.{pat}",
                            f"address_unaccent.ilike.{pat}",
                            f"adres_unaccent.ilike.{pat}",
                        ])
                or_expr = ",".join(conds)
                coarse = (
                    supabase
                    .table("companies")
                    .select("*")
                    .or_(or_expr)
                    .limit(500)
                    .execute()
                ).data or []
            except Exception:
                # Unaccent kolonları yoksa orijinal kolonlarla dene
                try:
                    conds = [f"sicil_no.ilike.%{q_digits}%", f"mersis_number.ilike.%{q_digits}%"]
                    for t in tokens:
                        vars_t = list(_token_variants(t))[:3]
                        for v in vars_t:
                            pat = f"%{v}%"
                            conds.extend([
                                f"unvan.ilike.{pat}",
                                f"address.ilike.{pat}",
                            ])
                    or_expr = ",".join(conds)
                    coarse = (
                        supabase.table("companies").select("*").or_(or_expr).limit(500).execute()
                    ).data or []
                except Exception:
                    coarse = []

            def _norm_all(c: Dict[str, Any]) -> str:
                return tr_normalize_py(
                    " ".join([
                        str(c.get("unvan", "")),
                        str(c.get("address", "") or c.get("adres", "")),
                        str(c.get("adres", "")),
                        str(c.get("city", "")),
                        str(c.get("district", "")),
                        str(c.get("sicil_mudurluk", "")),
                    ])
                )

            filtered: List[Dict[str, Any]] = []

            def _find_all(hay: str, needle: str) -> List[int]:
                out = []
                if not hay or not needle:
                    return out
                start = 0
                while True:
                    idx = hay.find(needle, start)
                    if idx == -1:
                        break
                    out.append(idx)
                    start = idx + max(1, len(needle))
                return out
            for c in coarse:
                try:
                    num_ok = False
                    if q_digits:
                        s_no = str(c.get("sicil_no", ""))
                        m_no = str(c.get("mersis_number", ""))
                        num_ok = (q_digits in s_no) or (q_digits in m_no)
                    s_all_norm = _norm_all(c) + " " + tr_normalize_py(str(c.get("sicil_no", ""))) + " " + tr_normalize_py(str(c.get("mersis_number", "")))
                    # token eşleşmesi (sinonim varyantları dahil)
                    text_ok = True
                    for t in tokens:
                        vars_t = _token_variants(t)
                        if not any(v in s_all_norm for v in vars_t):
                            text_ok = False
                            break
                    if num_ok and text_ok:
                        # Yakınlık skorunu hesapla
                        c = dict(c)
                        base = int(c.get("match_strength", 0) or 0)
                        score = max(base, 92)
                        # Sayı pozisyonları
                        digit_pos = _find_all(s_all_norm, tr_normalize_py(q_digits))
                        if digit_pos:
                            # Metin tokenları için en yakın mesafe
                            min_gap = 1_000_000
                            for t in tokens:
                                tpos_all: list[int] = []
                                for v in _token_variants(t):
                                    tpos_all.extend(_find_all(s_all_norm, v))
                                tpos = tpos_all
                                if not tpos:
                                    continue
                                for dp in digit_pos:
                                    for tp in tpos:
                                        gap = abs(dp - tp)
                                        if gap < min_gap:
                                            min_gap = gap
                            if min_gap <= SEARCH_PROXIMITY_STRONG:
                                score = max(score, 99)
                            elif min_gap <= SEARCH_PROXIMITY_MEDIUM:
                                score = max(score, 96)
                            elif min_gap <= SEARCH_PROXIMITY_WEAK:
                                score = max(score, 94)
                        # Alan bazlı bonus: sicil müdürlüğünde şehir geçiyorsa
                        sm = tr_normalize_py(str(c.get("sicil_mudurluk", "")))
                        if sm:
                            for t in tokens:
                                if any(v in sm for v in _token_variants(t)):
                                    score = max(score, 98)
                                    break
                        c["match_strength"] = score
                        filtered.append(c)
                except Exception:
                    continue

            if filtered:
                # Skora göre sırala ve erken dön
                filtered.sort(key=lambda x: x.get("match_strength", 0), reverse=True)
                result.companies = filtered[:MAX_COMPANIES]
                result.persons = []
                result.ocr_matches = []
                result.related_companies = []
                result.same_address_companies = []
                result.total_matches = len(filtered)
                logger.info(f"[Search Mixed] companies={len(filtered)} for q='{q_raw}'")
                return result
    except Exception:
        pass

    # 1) Şirketler: önce unaccent kolonları dene, hata olursa orijinal kolonlar ve Python filtresi
    companies_data: List[Dict[str, Any]] = []
    try:
        filter_expr = (
            f"unvan_unaccent.ilike.%{q_norm}%",
            f"sicil_no_unaccent.ilike.%{q_norm}%",
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
            or q_norm in tr_normalize_py(c.get("firma_unvani", ""))
            or q_norm in tr_normalize_py(c.get("sicil_no", ""))
            or q_norm in tr_normalize_py(c.get("address", ""))
            or q_norm in tr_normalize_py(c.get("adres", ""))
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
                    t in tr_normalize_py(" ".join([
                        c.get("unvan", ""),
                        c.get("sicil_no", ""),
                        c.get("address", ""),
                        c.get("adres", ""),
                        c.get("city", ""),
                        c.get("district", ""),
                    ]))
                    for t in tokens
                )
            ]
        except Exception:
            # Fallback: orijinal kolonlarla geniş arama yap ve Python tarafında AND ile filtrele
            try:
                conds = []
                for t in tokens:
                    pat = f"%{t}%"
                    conds.extend([
                        f"unvan.ilike.{pat}",
                        f"sicil_no.ilike.{pat}",
                        f"address.ilike.{pat}",
                    ])
                or_expr = ",".join(conds)
                coarse_multi = (
                    supabase.table("companies").select("*").or_(or_expr).limit(300).execute()
                ).data or []
                companies_data = [
                    c for c in coarse_multi
                    if all(
                        t in tr_normalize_py(" ".join([
                            c.get("unvan", ""),
                            c.get("sicil_no", ""),
                            c.get("address", ""),
                            c.get("adres", ""),
                            c.get("city", ""),
                            c.get("district", ""),
                        ]))
                        for t in tokens
                    )
                ]
            except Exception:
                pass

    # Ek: MERSİS alt-dize araması (örn. 7221127826)
    try:
        if q_digits and len(q_digits) >= 6:
            # 1) companies.mersis_number (opsiyonel kolon olabilir)
            try:
                mersis_hits = (
                    supabase
                    .table("companies")
                    .select("*")
                    .like("mersis_number", f"%{q_digits}%")
                    .limit(100)
                    .execute()
                ).data or []
                companies_data.extend(mersis_hits)
            except Exception:
                # Kolon yoksa veya hata olursa devam et
                pass

            # 2) companies.sicil_no
            try:
                sicil_hits = (
                    supabase
                    .table("companies")
                    .select("*")
                    .like("sicil_no", f"%{q_digits}%")
                    .limit(100)
                    .execute()
                ).data or []
                companies_data.extend(sicil_hits)
            except Exception:
                pass

            # 3) OCR üzerinden MERSİS/Original Text alt-dize araması -> company_id ile şirketleri ekle
            try:
                # 1) OCR'da mersis_no alanında alt-dize araması
                ocr_mersis_rows = (
                    supabase
                    .table("ocr_results")
                    .select("id, company_id, mersis_no, trade_name")
                    .like("mersis_no", f"%{q_digits}%")
                    .limit(1000)
                    .execute()
                ).data or []

                # 2) OCR'da original_text içinde alt-dize araması
                ocr_text_rows = (
                    supabase
                    .table("ocr_results")
                    .select("id, company_id")
                    .like("original_text", f"%{q_digits}%")
                    .limit(1000)
                    .execute()
                ).data or []

                logger.info(f"[Search] OCR numeric: mersis_hits={len(ocr_mersis_rows)} text_hits={len(ocr_text_rows)} for q_digits={q_digits}")

                # company_id bazında tekilleştir ve OCR alanlarını hazırla
                ocr_company_ids: Set[str] = set()
                ocr_mersis_map: Dict[str, str] = {}
                ocr_trade_map: Dict[str, str] = {}
                for row in (ocr_mersis_rows + ocr_text_rows):
                    cid = row.get("company_id")
                    if cid:
                        ocr_company_ids.add(cid)
                        if not ocr_mersis_map.get(cid):
                            val = row.get("mersis_no")
                            if val:
                                ocr_mersis_map[cid] = val
                        if not ocr_trade_map.get(cid):
                            tname = row.get("trade_name")
                            if tname:
                                ocr_trade_map[cid] = tname

                # Fallback: LIKE/ILIKE hatası veya boş sonuç varsa Python tarafı substring filtrelemesi
                if not ocr_company_ids:
                    try:
                        coarse_rows = (
                            supabase
                            .table("ocr_results")
                            .select("id, company_id, mersis_no, trade_name, original_text")
                            .limit(5000)
                            .execute()
                        ).data or []
                        for r in coarse_rows:
                            cid = r.get("company_id")
                            if not cid:
                                continue
                            mers = (r.get("mersis_no") or "")
                            txt = (r.get("original_text") or "")
                            if (q_digits in mers) or (q_digits in txt):
                                ocr_company_ids.add(cid)
                                if not ocr_mersis_map.get(cid) and mers:
                                    ocr_mersis_map[cid] = mers
                                if not ocr_trade_map.get(cid) and r.get("trade_name"):
                                    ocr_trade_map[cid] = r.get("trade_name")
                        logger.info(f"[Search] OCR numeric fallback matched companies={len(ocr_company_ids)}")
                    except Exception as _e_ocr_fb:
                        logger.warning(f"[Search] OCR numeric fallback failed: {_e_ocr_fb}")

                # Şirket tablosundan detayları çek; olmayanlar için minimal obje ekle
                if ocr_company_ids:
                    # Mevcut companies_data içindekileri çık; gereksiz çağrıyı azalt
                    existing_ids = {c.get("id") for c in companies_data if isinstance(c, dict)}
                    fetch_ids = sorted(list(ocr_company_ids - existing_ids))
                    fetched_map: Dict[str, Dict[str, Any]] = {}
                    if fetch_ids:
                        comp_resp = (
                            supabase
                            .table("companies")
                            .select("*")
                            .in_("id", fetch_ids)
                            .limit(min(1000, len(fetch_ids)))
                            .execute()
                        )
                        for c in (comp_resp.data or []):
                            if isinstance(c, dict) and c.get("id"):
                                fetched_map[c["id"]] = c
                        logger.info(f"[Search] OCR numeric: fetched {len(fetched_map)} companies by id")

                    # companies_data listesine ekle
                    for cid in ocr_company_ids:
                        if cid in fetched_map:
                            companies_data.append(fetched_map[cid])
                        else:
                            companies_data.append({
                                "id": cid,
                                # OCR'dan olası yardımcı alanlar
                                "mersis_number_ocr": ocr_mersis_map.get(cid),
                                "unvan_ocr": ocr_trade_map.get(cid),
                                # UI'da daha iyi gösterim için unvan yoksa OCR'dan geleni kullan
                                "unvan": ocr_trade_map.get(cid),
                            })
                    logger.info(f"[Search] OCR numeric: added {len(ocr_company_ids)} companies to results")
            except Exception as _e_ocr_numeric:
                # OCR aramasında hata olsa bile ana arama akışını bozma
                logger.warning(f"[Search] OCR numeric search failed: {_e_ocr_numeric}")
                
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

    # Metin araması için eşleşme skoru: prefix > sıralı tokenlar > serbest tokenlar > adres
    try:
        # Bu blok, hızlı sayısal/maskeli yollardan geçilmediyse devrededir
        if companies:
            for c in companies:
                try:
                    base_score = int(c.get("match_strength", 0) or 0)
                except Exception:
                    base_score = 0
                score = base_score
                unv = (c.get("unvan") or "").strip()
                s_unv = tr_normalize_py(unv)
                # 1) Tam ifade prefix eşleşmesi
                if q_norm and s_unv.startswith(q_norm):
                    score = max(score, 95)
                else:
                    # 2) İlk token prefix eşleşmesi veya ifade başa çok yakın
                    if tokens:
                        if s_unv.startswith(tokens[0]):
                            score = max(score, 88)
                    if q_norm:
                        idx = s_unv.find(q_norm)
                        if idx != -1 and idx <= 5:
                            score = max(score, 88)
                    # 3) Tokenlar sırayla geçiyor mu?
                    if tokens:
                        pos = 0
                        ok = True
                        for t in tokens:
                            p = s_unv.find(t, pos)
                            if p == -1:
                                ok = False
                                break
                            pos = p + len(t)
                        if ok:
                            score = max(score, 80)
                    # 4) Tüm tokenlar bir yerlerde mevcut mu?
                    if tokens and all(t in s_unv for t in tokens):
                        score = max(score, 72)
                    # 5) Adres fallback
                    if score == base_score:
                        addr = tr_normalize_py((c.get("address") or c.get("adres") or "").strip())
                        if addr and tokens and all(t in addr for t in tokens):
                            score = max(score, 50)
                c["match_strength"] = score

            # Skora göre sırala
            companies.sort(key=lambda x: x.get("match_strength", 0), reverse=True)
            total_companies_pre_count = len(companies)
            companies = companies[:MAX_COMPANIES]
    except Exception:
        pass

    result.companies = companies
    # Yükü azaltmak için aşağıdaki sorgularda yalnızca en iyi şirketlerin id'lerini kullan
    company_ids = [c.get("id") for c in companies if isinstance(c, dict) and c.get("id")]

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
    # Ek: Sayı odaklı aramalar için kimlik numarası (nationality_id) üzerinden hızlı arama
    try:
        if q_digits and len(q_digits) >= 6:
            pnat_resp = (
                supabase
                .table("persons")
                .select("*")
                .ilike("nationality_id", f"%{q_digits}%")
                .limit(200)
                .execute()
            )
            persons_match.extend(pnat_resp.data or [])
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
        # Sayısal sorgularda PostgREST ilike ile 500 hatası alabildiği için LIKE kullan
        all_digits = bool(q_digits) and (q_digits == tr_letters_digits(q_raw))
        if tokens:
            for t in tokens:
                if all_digits and t.isdigit():
                    ocr_q = ocr_q.like("original_text", f"%{t}%")
                else:
                    ocr_q = ocr_q.ilike("original_text", f"%{t}%")
        else:
            if all_digits:
                ocr_q = ocr_q.like("original_text", f"%{q_norm}%")
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
    # OCR eklemelerinden sonra da üst sınırı koru
    if len(result.companies) > MAX_COMPANIES:
        result.companies = result.companies[:MAX_COMPANIES]

    # 6) Toplam eşleşme sayısı
    pre_companies = total_companies_pre_count if total_companies_pre_count is not None else len(result.companies)
    result.total_matches = (
        pre_companies
        + len(result.related_companies)
        + len(result.same_address_companies)
        + len(result.persons)
        + len(result.ocr_matches)
    )

    logger.info(
        f"[Search] totals companies={len(result.companies)} related={len(result.related_companies)} same_addr={len(result.same_address_companies)} persons={len(result.persons)} ocr_matches={len(result.ocr_matches)} total={result.total_matches} for query='{query}'"
    )

    return result

@router.get("/companies")
def search_companies(
    q: str = Query(..., min_length=2, description="Search term for companies"),
    supabase: Client = Depends(get_supabase_client),
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
    request: Request,
    q: str = Query(..., min_length=2, description="Search across companies, persons, OCR and history (SPA payload)"),
    cursor: Optional[int] = Query(None, ge=0, description="Sayfalama için opak imleç (cursor)."),
    offset: Optional[int] = Query(0, ge=0, description="Şirketler için başlangıç ofseti (sayfalama)"),
    limit: Optional[int] = Query(None, ge=1, le=200, description="Maksimum şirket sayısı (<= MAX_COMPANIES)."),
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
        # Başlangıç zamanı + oran sınırı + önbellek anahtarı
        start_ts = time.perf_counter()
        try:
            ip = (request.headers.get("x-forwarded-for", "").split(",")[0].strip()) or (request.client.host if request.client else "unknown")
        except Exception:
            ip = "unknown"
        _limiter.check(ip)
        cache_key = f"all:{(q or '').strip().lower()}:{cursor if cursor is not None else (offset or 0)}:{limit or ''}"
        cached = _cache_all.get(cache_key)
        if cached is not None:
            return cached

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

        # Final safety cap at response time as well
        eff_limit = _clamp(limit if limit is not None else MAX_COMPANIES, 1, MAX_COMPANIES)
        start = int(cursor if cursor is not None else (offset or 0))
        end = start + eff_limit
        total_companies_pre = len(result.companies) if isinstance(result.companies, list) else 0
        capped_companies = result.companies[start:end]
        payload = {
            "companies": capped_companies,
            "persons": result.persons,
            "history": history_data,
            # Ekstra zengin alanlar (SPA şu an zorunlu tutmuyor ama advance kullanım için sağlıyoruz)
            "related_companies": result.related_companies,
            "same_address_companies": result.same_address_companies,
            "related_persons": result.related_persons,
            "ocr_matches": result.ocr_matches,
            "total_matches": result.total_matches,
            "limit": eff_limit,
            # Sayfalama sadece companies için; o yüzden next_* hesaplarını şirket toplamına göre yap
            "next_offset": (end if (isinstance(total_companies_pre, int) and total_companies_pre > end) else None),
            "next_cursor": (end if (isinstance(total_companies_pre, int) and total_companies_pre > end) else None),
        }
        dur_ms = int((time.perf_counter() - start_ts) * 1000)
        logger.info(
            f"[Unified Search /all] q='{q}' companies={len(capped_companies)} persons={len(result.persons)} history={len(history_data)} duration_ms={dur_ms} limit={eff_limit}"
        )
        _cache_all.set(cache_key, payload)
        return payload
    except Exception as e:
        logger.error(f"Error in unified search: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/all-legacy", summary="Unified search: companies, persons, history")
def search_all_legacy(
    request: Request,
    q: str = Query(..., min_length=2, description="Search term for companies, persons and history"),
    cursor: Optional[int] = Query(None, ge=0, description="Sayfalama için opak imleç (cursor)."),
    offset: Optional[int] = Query(0, ge=0, description="Şirketler için başlangıç ofseti (sayfalama)"),
    limit: Optional[int] = Query(None, ge=1, le=200, description="Maksimum şirket sayısı (<= MAX_COMPANIES)."),
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
        # Başlangıç zamanı + oran sınırı + önbellek anahtarı
        start_ts = time.perf_counter()
        try:
            ip = (request.headers.get("x-forwarded-for", "").split(",")[0].strip()) or (request.client.host if request.client else "unknown")
        except Exception:
            ip = "unknown"
        _limiter.check(ip)
        cache_key = f"all-legacy:{(q or '').strip().lower()}:{cursor if cursor is not None else (offset or 0)}:{limit or ''}"
        cached = _cache_all_legacy.get(cache_key)
        if cached is not None:
            return cached

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
            total_companies_pre_legacy = len(companies_data)
            # Legacy uçta skorlanmış sıralama yok; yine de yükü azaltmak için ilk N ile sınırla
            eff_limit = _clamp(limit if limit is not None else MAX_COMPANIES, 1, MAX_COMPANIES)
            start = int(cursor if cursor is not None else (offset or 0))
            end = start + eff_limit
            companies_data = companies_data[start:end]
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
            # Bilgilendirme amaçlı toplam (legacy): sadece uzunlukların toplamı
            "total_matches": total_companies_pre_legacy + len(persons_data) + len(history_data) if 'total_companies_pre_legacy' in locals() else len(companies_data) + len(persons_data) + len(history_data),
            "limit": eff_limit if 'eff_limit' in locals() else MAX_COMPANIES,
            "next_offset": (end if ('total_companies_pre_legacy' in locals() and isinstance(total_companies_pre_legacy, int) and total_companies_pre_legacy > end) else None),
            "next_cursor": (end if ('total_companies_pre_legacy' in locals() and isinstance(total_companies_pre_legacy, int) and total_companies_pre_legacy > end) else None),
        }
        _cache_all_legacy.set(cache_key, payload)
        dur_ms = int((time.perf_counter() - start_ts) * 1000)
        logger.info(
            f"[Unified Search /all-legacy] q='{q}' companies: {len(companies_data)}, persons: {len(persons_data)}, history: {len(history_data)}, duration_ms={dur_ms}, limit={payload.get('limit')}"
        )
        return payload

    except Exception as e:
        logger.error(f"[Unified Search] Error for query '{q}': {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An error occurred while performing unified search.")


@router.get("/company-detail", summary="Company detail with related persons and announcements")
def company_detail(
    company_id: str = Query(..., description="UUID of the company"),
    supabase: Client = Depends(get_supabase_client),
    _: None = Depends(enforce_daily_limit),
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
        # Attach koordinat {lat, lon} if present as GeoJSON; otherwise try LocationIQ geocoding (if configured)
        def _ensure_company_coords(c: dict):
            try:
                geo = c.get("koordinat")
                if isinstance(geo, dict):
                    coords = geo.get("coordinates")
                    if isinstance(coords, (list, tuple)) and len(coords) >= 2:
                        lon, lat = coords[0], coords[1]
                        if isinstance(lat, (int, float)) and isinstance(lon, (int, float)):
                            c["koordinat"] = {"lat": float(lat), "lon": float(lon)}
                            return
            except Exception:
                pass

            # Fallback to LocationIQ (optional)
            try:
                api_key = (
                    os.getenv("LOCATIONIQ_API_KEY")
                    or os.getenv("TSG_LOCATIONIQ_TOKEN")
                    or os.getenv("LOCATIONIQ_TOKEN")
                )
                if not api_key:
                    return
                base_url = os.getenv("LOCATIONIQ_BASE_URL", "https://us1.locationiq.com/v1")
                q_parts = [str(c.get("address") or c.get("adres") or "").strip()]
                # enrich with city/district if available
                for k in ("district", "city", "sicil_mudurluk"):
                    v = c.get(k)
                    if isinstance(v, str) and v.strip():
                        q_parts.append(v.strip())
                q = ", ".join([p for p in q_parts if p])
                if not q:
                    return
                params = {"key": api_key, "q": q, "format": "json", "limit": 1}
                r = requests.get(f"{base_url}/search", params=params, timeout=6)
                if r.ok:
                    arr = r.json() if r.headers.get("content-type", "").startswith("application/json") else None
                    if isinstance(arr, list) and arr:
                        top = arr[0]
                        lat = float(top.get("lat")) if top.get("lat") is not None else None
                        lon = float(top.get("lon")) if top.get("lon") is not None else None
                        if isinstance(lat, float) and isinstance(lon, float):
                            c["koordinat"] = {"lat": lat, "lon": lon}
            except Exception:
                # do not fail company detail for geocoding errors
                pass

        _ensure_company_coords(company)

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

        # --- Announcements: enrich with OCR original_text ---
        try:
            if data := result.__dict__.get('announcements'):
                pass  # placeholder; we haven't set announcements yet in this function
        except Exception:
            pass

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
            # Aynı adresteki şirketlerde MERSIS yoksa OCR'dan aday türet
            try:
                if same_address_companies:
                    pat_mersis = re.compile(r"(?:mers(?:i|ı)s\D{0,50}?)([0-9]{10,20})", re.IGNORECASE)
                    for sc in same_address_companies[:20]:  # performans: ilk 20
                        try:
                            if not isinstance(sc, dict) or sc.get('mersis_number'):
                                continue
                            scid = sc.get('id')
                            if not scid:
                                continue
                            ocr2 = (
                                supabase
                                .table('ocr_results')
                                .select('id, original_text')
                                .eq('company_id', scid)
                                .limit(20)
                                .execute()
                            )
                            candidates = []
                            for row in (ocr2.data or []):
                                txt = (row.get('original_text') or '')
                                for m in pat_mersis.finditer(txt):
                                    val = m.group(1)
                                    if val and val not in candidates:
                                        candidates.append(val)
                            if candidates:
                                sc['mersis_number_ocr'] = candidates[0]
                        except Exception:
                            continue
            except Exception as _e_mersis_same:
                logger.warning(f"[Company Detail] Same-address MERSIS extraction failed: {_e_mersis_same}")

        # --- Related companies via shared persons ---
        related_companies = []
        existing_related_ids: Set[str] = set()
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
        except Exception as ex:
            logger.warning(f"[Company Detail] Related companies resolution failed: {ex}")

        # --- Announcements --- (fallback'lı)
        announcements = []
        try:
            # '*' seçerek tabloda varsa original_text gibi ek alanları da alalım.
            ann_resp = (
                supabase
                .table("announcements")
                .select("*")
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
                        .select("*")
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

        # Enrichment: announcements -> original_text & hususlar (from ocr_results by announcement_id)
        try:
            ann_ids = [a.get("id") for a in announcements if isinstance(a, dict) and a.get("id")]
            if ann_ids:
                ocr_by_ann = (
                    supabase
                    .table("ocr_results")
                    .select("announcement_id, original_text, hususlar")
                    .in_("announcement_id", ann_ids)
                    .limit(min(2000, len(ann_ids) * 5))
                    .execute()
                ).data or []
                # Son ilanın metnini tercih et (aynı announcement_id için birden fazla satır olabilir)
                ocr_text_map: Dict[Any, str] = {}
                ocr_husus_map: Dict[Any, str] = {}
                for row in ocr_by_ann:
                    aid = row.get("announcement_id")
                    if aid:
                        if not ocr_text_map.get(aid):
                            ocr_text_map[aid] = row.get("original_text") or ""
                        if not ocr_husus_map.get(aid):
                            hus = row.get("hususlar")
                            hus_text = ""
                            try:
                                if isinstance(hus, str):
                                    hus_text = hus.strip()
                                elif isinstance(hus, list):
                                    # Join list items into a single line
                                    hus_text = ", ".join([str(x).strip() for x in hus if str(x).strip()])[:300]
                                elif isinstance(hus, dict):
                                    # Prefer common keys if present
                                    pref = hus.get("text") or hus.get("value") or ""
                                    if isinstance(pref, str):
                                        hus_text = pref.strip()
                                    else:
                                        hus_text = str(hus)
                                elif hus is not None:
                                    hus_text = str(hus)
                            except Exception:
                                hus_text = ""
                            ocr_husus_map[aid] = hus_text
                for a in announcements:
                    aid = a.get("id")
                    if aid and aid in ocr_text_map:
                        a["original_text"] = ocr_text_map[aid]
                    if aid and aid in ocr_husus_map and ocr_husus_map[aid]:
                        a["hususlar"] = ocr_husus_map[aid]
                # Fallback: Hala metni olmayan ilanlar için şirketin en yeni OCR kayıtlarından sırayla doldur
                missing = [a for a in announcements if isinstance(a, dict) and not a.get("original_text")]
                if missing:
                    try:
                        ocr_recent = (
                            supabase
                            .table("ocr_results")
                            .select("id, original_text, created_at")
                            .eq("company_id", cid)
                            .order("created_at", desc=True)
                            .limit(50)
                            .execute()
                        ).data or []
                        # Tüm eksiklere sırayla doldur, yetmezse ilk metni yay
                        if ocr_recent:
                            for i, a in enumerate(missing):
                                src = ocr_recent[i] if i < len(ocr_recent) else ocr_recent[0]
                                a["original_text"] = (src.get("original_text") or a.get("original_text") or "")
                    except Exception:
                        pass
        except Exception as _e_enrich:
            logger.warning(f"[Company Detail] enrich announcements with original_text failed: {_e_enrich}")

                # --- OCR Results: persons JSON, masked_ids ve yıldızlı örüntüler ---
        try:
            ocr_resp = (
                supabase
                .table("ocr_results")
                .select("id, original_text, persons, masked_ids, created_at, old_trade_name")
                .eq("company_id", cid)
                .order("created_at", desc=True)
                .limit(100)
                .execute()
            )
            try:
                logger.info(f"[Company Detail] OCR results fetched: count={len(ocr_resp.data or [])}")
            except Exception:
                pass

            # using module-level imports for re/json
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

            # MERSIS çıkarımı (mevcut şirkette yoksa OCR'dan türet)
            try:
                if not company.get('mersis_number'):
                    mersis_candidates = []
                    pat = re.compile(r"(?:mers(?:i|ı)s\D{0,50}?)([0-9]{10,20})", re.IGNORECASE)
                    for ocr in (ocr_resp.data or []):
                        txt = (ocr.get('original_text') or '')
                        for m in pat.finditer(txt):
                            val = m.group(1)
                            if val and val not in mersis_candidates:
                                mersis_candidates.append(val)
                    if mersis_candidates:
                        company['mersis_number_ocr'] = mersis_candidates[0]
            except Exception as ex_mersis:
                logger.warning(f"[Company Detail] MERSIS extraction failed: {ex_mersis}")

            # candidate_pairs metrik logu kaldırıldı (tanımsız değişken hatası önlendi)

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

        # Derivations from OCR results
        # 1) Eski unvanlar listesi
        try:
            ocr_rows = (ocr_resp.data or []) if 'ocr_resp' in locals() and hasattr(ocr_resp, 'data') else []
            old_names: list[str] = []

            # Prefer materialized view (fast path)
            try:
                mv = (
                    supabase
                    .table('company_old_trade_names_mv')
                    .select('old_trade_names')
                    .eq('company_id', cid)
                    .limit(1)
                    .execute()
                )
                mv_list = (mv.data[0] or {}).get('old_trade_names') if (mv and mv.data) else []
                if isinstance(mv_list, list):
                    for item in mv_list:
                        if isinstance(item, str):
                            v = item.strip()
                            if v and v not in old_names:
                                old_names.append(v)
            except Exception:
                pass
            for r in ocr_rows:
                name = (r.get('old_trade_name') or '').strip()
                if name and name not in old_names:
                    old_names.append(name)
            # Fallback: company_id üzerinden bulunamadıysa, mersis_no ile direkt tara
            if not old_names:
                try:
                    mersis_vals_fb: list[str] = []
                    for k in ("mersis_number", "mersis_number_ocr"):
                        v = company.get(k)
                        if isinstance(v, str) and v.strip():
                            vv = v.strip()
                            if vv not in mersis_vals_fb:
                                mersis_vals_fb.append(vv)
                    if mersis_vals_fb:
                        fb_rows = (
                            supabase
                            .table('ocr_results')
                            .select('old_trade_name, mersis_no, created_at')
                            .in_('mersis_no', mersis_vals_fb)
                            .order('created_at', desc=True)
                            .limit(200)
                            .execute()
                        ).data or []
                        for r in fb_rows:
                            nm = (r.get('old_trade_name') or '').strip()
                            if nm and nm not in old_names:
                                old_names.append(nm)
                except Exception:
                    pass
            # Second fallback: derive mersis_no directly from this company's OCR rows
            if not old_names:
                try:
                    mers_set: Set[str] = set()
                    for r in ocr_rows:
                        mv = r.get('mersis_no')
                        if isinstance(mv, str) and mv.strip():
                            mers_set.add(mv.strip())
                    if mers_set:
                        fb_rows2 = (
                            supabase
                            .table('ocr_results')
                            .select('old_trade_name, mersis_no, created_at')
                            .in_('mersis_no', list(mers_set))
                            .order('created_at', desc=True)
                            .limit(200)
                            .execute()
                        ).data or []
                        for r in fb_rows2:
                            nm = (r.get('old_trade_name') or '').strip()
                            if nm and nm not in old_names:
                                old_names.append(nm)
                except Exception:
                    pass
            # Final fallback: RPC function (SQL) — get_company_old_trade_names(uuid)
            if not old_names:
                try:
                    rpc_resp = supabase.rpc('get_company_old_trade_names', { 'p_company_id': cid }).execute()
                    arr = []
                    try:
                        arr = rpc_resp.data or []
                    except Exception:
                        arr = []
                    if isinstance(arr, list):
                        for item in arr:
                            if isinstance(item, str):
                                v = item.strip()
                                if v and v not in old_names:
                                    old_names.append(v)
                except Exception:
                    pass
        except Exception:
            old_names = []

        # 2) Announcements boşsa, OCR snippet'larından pseudo-ilan üret
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
                        'title': first_line or 'Metin Özeti',
                        'announcement_type': None,
                        'publication_date': None,
                        'issue_number': None,
                        'page_number': None,
                        'newspaper_name': None,
                        'pdf_url': None,
                        'ocr_status': None,
                        'created_at': None,
                        'trade_registry_number': company.get('sicil_no'),
                        'original_text': txt,
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

        # --- Old addresses: prefer ocr_results.old_addresses, fallback to text heuristics ---
        old_addresses = []
        try:
            curr_addr = (company.get('address') or company.get('adres') or '').strip()
            seen_norm: Set[str] = set()
            candidates: list[str] = []

            # 0) From ocr_results.old_addresses JSONB (preferred)
            try:
                ocr_oa_resp = (
                    supabase
                    .table('ocr_results')
                    .select('old_addresses, created_at')
                    .eq('company_id', cid)
                    .order('created_at', desc=True)
                    .limit(50)
                    .execute()
                )
                for row in (ocr_oa_resp.data or []):
                    oa = row.get('old_addresses')
                    if isinstance(oa, list):
                        for item in oa:
                            if isinstance(item, str):
                                v = item.strip()
                                if v:
                                    candidates.append(v)
                            elif isinstance(item, dict):
                                v = (item.get('address') or item.get('adres') or '').strip()
                                if v:
                                    candidates.append(v)
                            elif isinstance(item, list):
                                for sub in item:
                                    if isinstance(sub, str) and sub.strip():
                                        candidates.append(sub.strip())
                                    elif isinstance(sub, dict):
                                        v = (sub.get('address') or sub.get('adres') or '').strip()
                                        if v:
                                            candidates.append(v)
            except Exception as _e_ocr_oa:
                logger.warning(f"[Company Detail] reading ocr_results.old_addresses failed: {_e_ocr_oa}")

            # Not: OCR old_addresses boş ise heuristik üretim yapılmaz (kullanıcı isteği)

            # Deduplicate and exclude current address (normalized)
            uniq: list[str] = []
            curr_norm = tr_normalize_py(curr_addr)
            for caddr in candidates:
                n = tr_normalize_py(caddr)
                if not n or n == curr_norm:
                    continue
                if n in seen_norm:
                    continue
                seen_norm.add(n)
                uniq.append(caddr)

            # Try to link to existing companies at same address
            for addr in uniq[:20]:  # limit
                linked_company = None
                linked_company_id = None
                try:
                    cands = (
                        supabase
                        .table('companies')
                        .select('id, unvan, address, sicil_no, mersis_number')
                        .eq('address', addr)
                        .limit(1)
                        .execute()
                    ).data or []
                    if cands:
                        linked_company = cands[0]
                        linked_company_id = linked_company.get('id')
                    else:
                        # Fallback 1: address_unaccent ilike normalized pattern
                        try:
                            norm = tr_normalize_py(addr)
                            pat = f"%{norm[:80]}%"
                            cands2 = (
                                supabase
                                .table('companies')
                                .select('id, unvan, address, sicil_no, mersis_number')
                                .ilike('address_unaccent', pat)
                                .limit(1)
                                .execute()
                            ).data or []
                            if cands2:
                                linked_company = cands2[0]
                                linked_company_id = linked_company.get('id')
                        except Exception:
                            pass
                        # Fallback 2: address ilike raw snippet
                        if not linked_company_id:
                            try:
                                pat2 = f"%{addr[:80]}%"
                                cands3 = (
                                    supabase
                                    .table('companies')
                                    .select('id, unvan, address, sicil_no, mersis_number')
                                    .ilike('address', pat2)
                                    .limit(1)
                                    .execute()
                                ).data or []
                                if cands3:
                                    linked_company = cands3[0]
                                    linked_company_id = linked_company.get('id')
                            except Exception:
                                pass
                        # Fallback 3: başka şirketlerin old_addresses (OCR) içinde ara
                        if not linked_company_id:
                            try:
                                occ_data: list[dict] = []
                                # array of strings
                                occ1 = (
                                    supabase
                                    .table('ocr_results')
                                    .select('company_id, companies(*)')
                                    .filter('old_addresses', 'cs', json.dumps([addr]))
                                    .limit(50)
                                    .execute()
                                )
                                occ_data.extend(occ1.data or [])
                                # array of objects with address/adres
                                occ2 = (
                                    supabase
                                    .table('ocr_results')
                                    .select('company_id, companies(*)')
                                    .filter('old_addresses', 'cs', json.dumps([{ 'address': addr }]))
                                    .limit(50)
                                    .execute()
                                )
                                occ_data.extend(occ2.data or [])
                                occ3 = (
                                    supabase
                                    .table('ocr_results')
                                    .select('company_id, companies(*)')
                                    .filter('old_addresses', 'cs', json.dumps([{ 'adres': addr }]))
                                    .limit(50)
                                    .execute()
                                )
                                occ_data.extend(occ3.data or [])
                                # pick first different company
                                for row in occ_data:
                                    rcid = row.get('company_id')
                                    if not rcid or rcid == cid:
                                        continue
                                    comp_obj = row.get('companies') if isinstance(row.get('companies'), dict) else None
                                    if not comp_obj:
                                        try:
                                            comp_f = (
                                                supabase
                                                .table('companies')
                                                .select('id, unvan, address, sicil_no, mersis_number')
                                                .eq('id', rcid)
                                                .limit(1)
                                                .execute()
                                            ).data or []
                                            comp_obj = comp_f[0] if comp_f else None
                                        except Exception:
                                            comp_obj = None
                                    if comp_obj:
                                        linked_company = comp_obj
                                        linked_company_id = comp_obj.get('id') or rcid
                                        break
                            except Exception:
                                pass
                except Exception:
                    pass
                old_addresses.append({
                    'address': addr,
                    'matched_company_id': linked_company_id,
                    'matched_company': linked_company,
                })
        except Exception as e:
            logger.warning(f"[Company Detail] old_addresses derivation failed: {e}")

        # --- Registry-related companies (MERSIS / Sicil) ---
        registry_related_companies = []
        try:
            existing_rr_ids: Set[str] = set()

            # MERSIS match
            mersis_vals: list[str] = []
            try:
                for k in ("mersis_number", "mersis_number_ocr"):
                    v = company.get(k)
                    if isinstance(v, str) and v.strip():
                        vv = v.strip()
                        if vv not in mersis_vals:
                            mersis_vals.append(vv)
            except Exception:
                pass
            if mersis_vals:
                try:
                    mresp = (
                        supabase
                        .table('companies')
                        .select('id, unvan, address, sicil_no, mersis_number, sicil_mudurluk, sicil_office_code')
                        .in_('mersis_number', mersis_vals)
                        .neq('id', cid)
                        .limit(500)
                        .execute()
                    )
                    for row in (mresp.data or []):
                        rid = row.get('id')
                        if not rid or rid in existing_rr_ids:
                            continue
                        registry_related_companies.append({**row, 'match_reason': 'MERSIS_MATCH'})
                        existing_rr_ids.add(rid)
                except Exception as _e_mersis:
                    logger.warning(f"[Company Detail] registry mersis match failed: {_e_mersis}")

            # Sicil match (same sicil_no and same office first token)
            def _office_first_token(s: Any) -> str:
                try:
                    return str(s or '').strip().split()[0].upper()
                except Exception:
                    return ''

            sicil_no = company.get('sicil_no')
            office_norm = _office_first_token(company.get('sicil_mudurluk') or company.get('sicil_office_code'))
            if isinstance(sicil_no, str) and sicil_no.strip():
                try:
                    sresp = (
                        supabase
                        .table('companies')
                        .select('id, unvan, address, sicil_no, mersis_number, sicil_mudurluk, sicil_office_code')
                        .eq('sicil_no', sicil_no.strip())
                        .neq('id', cid)
                        .limit(500)
                        .execute()
                    )
                    for row in (sresp.data or []):
                        rid = row.get('id')
                        if not rid or rid in existing_rr_ids:
                            continue
                        other_off = _office_first_token(row.get('sicil_mudurluk') or row.get('sicil_office_code'))
                        if office_norm and other_off and other_off != office_norm:
                            continue
                        registry_related_companies.append({**row, 'match_reason': 'SICIL_MATCH'})
                        existing_rr_ids.add(rid)
                except Exception as _e_sicil:
                    logger.warning(f"[Company Detail] registry sicil match failed: {_e_sicil}")
        except Exception as _e_rr:
            logger.warning(f"[Company Detail] registry related companies failed: {_e_rr}")

        # --- Final payload ---
        return {
            "company": company,
            "persons": persons,
            "announcements": announcements,
            "history": gazette_entries,
            "related_companies": related_companies,
            "same_address_companies": same_address_companies,
            "registry_related_companies": registry_related_companies,
            "old_addresses": old_addresses,
            "old_trade_names": old_names,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[Company Detail] Error for company_id '{company_id}': {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An error occurred while fetching company detail.")

@router.get("/announcement-detail", summary="Announcement detail with OCR text")
def announcement_detail(
    announcement_id: str = Query(..., description="UUID of the announcement"),
    supabase: Client = Depends(get_supabase_client),
    _: None = Depends(enforce_daily_limit),
):
    try:
        # 1) İlan kaydını getir
        try:
            ann_q = (
                supabase
                .table("announcements")
                .select("*")
                .eq("id", announcement_id)
                .limit(1)
                .execute()
            )
            ann = (ann_q.data or [None])[0]
            if not ann:
                raise HTTPException(status_code=404, detail="İlan bulunamadı")
        except HTTPException:
            raise
        except Exception as ex_ann:
            logger.error(f"[Announcement Detail] Fetch announcement failed: {ex_ann}")
            raise HTTPException(status_code=500, detail="İlan getirilemedi")

        # 2) OCR metni — announcement_id ile
        original_text = None
        try:
            ocr_q = (
                supabase
                .table("ocr_results")
                .select("id, original_text, created_at")
                .eq("announcement_id", announcement_id)
                .order("created_at", desc=True)
                .limit(1)
                .execute()
            )
            if ocr_q.data:
                original_text = (ocr_q.data[0] or {}).get("original_text")
        except Exception as ex_ocr:
            logger.warning(f"[Announcement Detail] OCR by announcement_id failed: {ex_ocr}")

        return {
            "announcement": ann,
            "original_text": original_text,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[Announcement Detail] Error for announcement_id '{announcement_id}': {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An error occurred while fetching announcement detail.")
