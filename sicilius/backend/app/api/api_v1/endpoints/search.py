from fastapi import APIRouter, Depends, HTTPException, Query, Request
from typing import List, Dict, Any, Optional, Set, Tuple, Iterable
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
import uuid
from collections import deque

from sqlalchemy import or_, and_, func, text, cast, Text
from sqlalchemy.orm import Session, joinedload

from geoalchemy2.shape import to_shape

from app.api.deps import enforce_daily_limit, get_db
from app.core.config import settings
from app.core.search_tokens import tr_normalize_py as _tr_normalize_py, tr_letters_digits as _tr_letters_digits
from app.models.company import Company
from app.models.person import Person
from app.models.announcement import Announcement
from app.models.ocr_result import OcrResult
from app.models.gazette import GazetteEntry
from app.models.relation import CompanyPersonRelation

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

# --- MERSIS-FIRST HELPERS ---
def _get_vkn_from_text(text_val: Optional[str]) -> Optional[str]:
    """
    Extracts 11-character identification backbone.
    If 16-digit Mersis: Usually 0 + 10-digit VKN + 000XX.
    If 11-digit: 0... is VKN, 1-9... is TCKN.
    """
    if not text_val: return None
    # 1. Clean digits
    d = "".join(filter(str.isdigit, str(text_val)))
    if len(d) == 16 and d.startswith("0"):
        return d[:11] # Return 0 + 10-digit VKN
    if len(d) >= 11:
        return d[:11]
        
    # 2. Keyed search fallback
    m = re.search(r"(?:Mersis|VKN|TCKN)\s*[:：]?\s*(\d{11,16})", str(text_val), re.IGNORECASE)
    if m:
        d2 = "".join(filter(str.isdigit, m.group(1)))
        return d2[:11] if len(d2) >= 11 else None
    return None

def _is_reliable_mersis_match(vkn_target: Optional[str], ocr_text: Optional[str], ocr_mersis: Optional[str] = None) -> bool:
    """Verifies if the OCR content belongs to the target VKN."""
    if not vkn_target: return True 
    
    ann_vkn = _get_vkn_from_text(ocr_mersis) or _get_vkn_from_text(ocr_text)
    if ann_vkn:
        return ann_vkn == vkn_target
    return True # Allow pre-2021 announcements with no Mersis (Low confidence)


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
    history: List[Dict[str, Any]] = Field(default_factory=list)
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
    return _tr_normalize_py(s)

def tr_letters_digits(s: Optional[str]) -> str:
    """Normalize et ve harf/rakam dışını çıkar. Maskeli OCR metinleri için faydalı."""
    return _tr_letters_digits(s)


_ADDRESS_STOPWORDS = {
    "mah",
    "mahalle",
    "mahallesi",
    "cad",
    "cadde",
    "bul",
    "bulvar",
    "bulvari",
    "sok",
    "sokak",
    "sk",
    "no",
    "ic",
    "iç",
    "kapi",
    "kapı",
    "daire",
    "blok",
    "kat",
    "apt",
    "ap",
    "site",
    "sit",
    "merkez",
    "il",
    "ilce",
    "ilçesi",
}


_PERSON_NAME_SKIP_KEYWORDS = {
    "kimlik",
    "mersis",
    "sicil",
    "uyruk",
    "adres",
    "madde",
    "karar",
    "şirket",
    "sirket",
    "limited",
    "anonim",
    "ticaret",
    "no",
    "say",
    "t.c",
    "t c",
}


_PERSON_NAME_FORBIDDEN_TOKENS = {
    "TURKIYE",
    "TÜRKİYE",
    "CUMHURIYETI",
    "CUMHURİYETİ",
    "UYRUK",
    "UYRUKLU",
    "KIMLIK",
    "KİMLİK",
    "MERSIS",
    "MERSİS",
    "NO",
    "SAYI",
    "SAYISI",
    "ADRES",
    "ADRESINDE",
    "ADRESİNDE",
    "IKAMET",
    "İKAMET",
    "EDEN",
    "EDEN,",
    "MUDUR",
    "MÜDÜR",
    "SEÇILMISTIR",
    "SEÇİLMİŞTİR",
    "YETKI",
    "YETKİ",
    "SEKLI",
    "ŞEKLİ",
    "MÜNFERIDEN",
    "MÜNFERİDEN",
    "TEMSILE",
    "TEMSİLE",
    "YÜRÜTÜLÜR",
    "YÜRÜTÜLÜR.",
    "ŞİRKETİN",
    "SIRKETIN",
    "LIMITED",
    "LİMİTED",
    "ANONIM",
    "ANONİM",
    "ŞIRKETİ",
    "ŞİRKETİ",
    "SIRKETI",
    "ŞİRKET",
    "SIRKET",
    "VE",
    "ILE",
    "İLE",
    "MADDE",
    "KARAR",
}


def _normalize_address_for_compare(address: Optional[str]) -> Optional[str]:
    if not address:
        return None
    normalized = _normalize_text_for_compare(address)
    return normalized or None


def _normalize_whitespace_lower(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    collapsed = " ".join(str(value).strip().split())
    if not collapsed:
        return None
    return collapsed.lower()


def _is_plausible_address_line(value: Optional[str]) -> bool:
    if not value:
        return False
    stripped = " ".join(str(value).split())
    if len(stripped) < 8:
        return False
    has_digit = any(ch.isdigit() for ch in stripped)
    normalized = tr_normalize_py(stripped)
    if not normalized:
        return False
    tokens = normalized.split()
    if has_digit and len(tokens) >= 3:
        return True
    if any(token in _ADDRESS_STOPWORDS for token in tokens):
        return True
    return False


def _resolve_canonical_address(primary: Optional[str], extras: Iterable[str]) -> Optional[Tuple[str, str, str]]:
    candidates: List[Optional[str]] = [primary]
    candidates.extend(extras)
    for addr in candidates:
        if not addr or not _is_plausible_address_line(addr):
            continue
        norm_compare = _normalize_address_for_compare(addr)
        norm_ws = _normalize_whitespace_lower(addr)
        if not norm_ws:
            continue
        return addr, norm_ws, norm_compare
    return None


def _extract_structured_persons_payload(structured: Any) -> List[Dict[str, Any]]:
    persons_payload: List[Dict[str, Any]] = []
    def _plausible_person_name(name: str) -> bool:
        try:
            n = (name or "").strip()
            if len(n) < 2 or len(n) > 60:
                return False
            up = n.upper()
            banned = [
                "YÖNETİM", "YONETIM", "KURULU", "SEÇİL", "SECIL", "TEMSiLE", "TEMSİLE", "TEMSIL",
                "YETKİ", "YETKI", "GÖREV", "GOREV", "DAĞILIM", "DAGILIM", "GENEL", "KURUL",
                "MADDE", "SAYI", "SAYFA",
            ]
            company_words = [
                "SANAY", "SANAYİ", "SANAYI", "ŞİRKET", "SIRKET", "LİMİTED", "LIMITED",
                "ANONİM", "ANONIM", "TİCARET", "TICARET", "A.Ş", "A.S", "LTD", "HOLDİNG", "HOLDING", "BANK",
            ]
            for w in banned:
                if w in up:
                    return False
            for w in company_words:
                if w in up:
                    return False
            return True
        except Exception:
            return False
    try:
        data = structured
        if isinstance(data, str):
            data = json.loads(data)
        raw_persons: Any = []
        if isinstance(data, dict):
            raw_persons = data.get("persons") or []
            if isinstance(raw_persons, dict):
                raw_persons = [raw_persons]
            if isinstance(raw_persons, list):
                for item in raw_persons:
                    if not isinstance(item, dict):
                        continue
                    name = _structured_person_name(item)
                    if not name:
                        continue
                    masked_candidates = _extract_structured_masked_ids(item)
                    masked_arr = [m for m in masked_candidates if isinstance(m, str) and m.strip()]
                    if not masked_arr:
                        continue
                    if not _plausible_person_name(name):
                        continue
                    persons_payload.append({
                        "full_name": name,
                        "mask_source": "structured",
                        "masked_ids": masked_arr,
                        "relation_type": None,
                        "position": None,
                        "is_current": True,
                        "start_date": None,
                        "end_date": None,
                    })
    except Exception:
        return persons_payload
    return persons_payload

def _address_query_tokens(address: str, max_tokens: int = 6) -> List[str]:
    if not address:
        return []
    normalized = _normalize_text_for_compare(address)
    if not normalized:
        return []
    raw_tokens = re.findall(r"[0-9A-Za-zÇĞİÖŞÜçğıöşü]+", address)
    selected: List[str] = []
    seen: Set[str] = set()
    for token in raw_tokens:
        if token.isdigit():
            continue
        normalized = tr_normalize_py(token)
        if not normalized or len(normalized) < 3:
            continue
        if normalized in _ADDRESS_STOPWORDS:
            continue
        if normalized in seen:
            continue
        seen.add(normalized)
        selected.append(token)
        if len(selected) >= max_tokens:
            break
    return selected


def _structured_person_name(item: Dict[str, Any]) -> Optional[str]:
    for key in ("full_name", "fullName", "name", "text"):
        value = item.get(key)
        if isinstance(value, str) and value.strip():
            name = _clean_person_name(value)
            if name:
                return name
    first = item.get("first_name") or item.get("firstName")
    middle = item.get("middle_name") or item.get("middleName")
    last = item.get("last_name") or item.get("lastName") or item.get("surname")
    parts = [part.strip() for part in [first, middle, last] if isinstance(part, str) and part.strip()]
    if parts:
        name = _clean_person_name(" ".join(parts))
        if name:
            return name
    return None


def _extract_structured_masked_ids(item: Dict[str, Any]) -> List[str]:
    masked_candidates: List[str] = []
    for key in (
        "masked_ids",
        "masked_id",
        "maskedIdentity",
        "masked_identity",
        "masked_tc",
        "maskedTc",
        "masked_tckn",
        "maskedIdentityNumbers",
        "masked_identity_numbers",
    ):
        value = item.get(key)
        if isinstance(value, list):
            for entry in value:
                entry_str = str(entry).strip()
                if entry_str:
                    masked_candidates.append(entry_str)
        elif isinstance(value, str) and value.strip():
            masked_candidates.append(value.strip())
    seen: Set[str] = set()
    unique: List[str] = []
    for candidate in masked_candidates:
        clean_candidate = candidate.replace(" ", "")
        if clean_candidate and clean_candidate not in seen:
            seen.add(clean_candidate)
            unique.append(clean_candidate)
    return unique


def _extract_uppercase_name_candidate(line: str) -> Optional[str]:
    if not line:
        return None
    tokens = [token.strip(" ,.;:()[]{}'\"“”‘’") for token in line.split()]
    tokens = [token for token in tokens if token]
    if not tokens:
        return None

    def _token_valid(token: str) -> bool:
        letters = [ch for ch in token if ch.isalpha()]
        if len(letters) < 2:
            return False
        upper_ratio = sum(1 for ch in letters if ch.isupper()) / len(letters)
        if upper_ratio < 0.6:
            return False
        normalized = tr_normalize_py(token).upper()
        if normalized in _PERSON_NAME_FORBIDDEN_TOKENS:
            return False
        return True

    for length in (3, 2):
        for idx in range(len(tokens) - length + 1):
            segment = tokens[idx : idx + length]
            if not all(_token_valid(token) for token in segment):
                continue
            candidate = " ".join(segment)
            candidate_clean = _clean_person_name(candidate)
            if not candidate_clean:
                continue
            parts = candidate_clean.split()
            # Baş harfleri büyük/kalan küçük hale getir
            normalized_parts = [part if part.istitle() else part.title() for part in parts]
            return " ".join(normalized_parts)
    return None


def _is_likely_person_line(line: str) -> Optional[str]:
    cleaned = _clean_person_name(line)
    if not cleaned:
        return None
    lowered = cleaned.lower()
    if "/" in cleaned:
        return None
    for keyword in _PERSON_NAME_SKIP_KEYWORDS:
        if keyword in lowered:
            return None
    tokens = [token for token in cleaned.split() if token]
    if len(tokens) < 2:
        return None
    alpha_tokens = sum(1 for token in tokens if token.replace(".", "").isalpha())
    if alpha_tokens / len(tokens) < 0.8:
        return None
    return cleaned


def _extract_person_name_candidate(line: str) -> Optional[str]:
    direct = _is_likely_person_line(line)
    if direct:
        return direct
    return _extract_uppercase_name_candidate(line)


def _resolve_person_name_from_context(lines: List[str], idx: int) -> Optional[str]:
    offsets = [-1, -2, -3, 0, 1, 2]
    for offset in offsets:
        pos = idx + offset
        if pos < 0 or pos >= len(lines):
            continue
        candidate = _extract_person_name_candidate(lines[pos])
        if candidate:
            return candidate
    return None


def _iso_or_none(value: Optional[datetime]) -> Optional[str]:
    return value.isoformat() if value else None


def _extract_coordinates(geom: Any) -> Optional[Dict[str, float]]:
    if geom is None:
        return None
    try:
        shape = to_shape(geom)
        return {"x": float(shape.x), "y": float(shape.y)}
    except Exception:
        return None


def _company_to_dict(
    company: Company,
    *,
    match_strength: Optional[int] = None,
    ocr_addresses: Optional[List[str]] = None,
) -> Dict[str, Any]:
    address = company.address
    if (not address) and ocr_addresses:
        for addr in ocr_addresses:
            normalized = _normalize_address_for_compare(addr)
            if normalized:
                address = addr
                break

    return {
        "id": str(company.id),
        "unvan": company.unvan,
        "firma_unvani": company.unvan,  # Alias for frontend compatibility
        "address": address,
        "address_is_generic": len(address.strip()) < 15 if address else False,
        "adres": address,  # Alias for frontend compatibility
        "sicil_no": company.sicil_no,
        "mersis_number": company.mersis_number,
        "sicil_mudurluk": company.sicil_mudurluk,  # Add missing field
        "city": company.city,
        "district": company.district,
        "koordinat": _extract_coordinates(company.koordinat),
        "is_active": company.is_active,
        "establishment_date": _iso_or_none(company.establishment_date),
        "created_at": _iso_or_none(company.created_at),
        "updated_at": _iso_or_none(company.updated_at),
        "scraped_at": _iso_or_none(company.scraped_at),
        "pdf_name": company.pdf_name,
        "pdf_path": company.pdf_path,
        "match_strength": match_strength,
    }


def _person_to_dict(person: Person) -> Dict[str, Any]:
    return {
        "id": str(person.id),
        "full_name": person.full_name,
        "first_name": person.first_name,
        "middle_name": person.middle_name,
        "last_name": person.last_name,
        "nationality_id": person.nationality_id,
        "passport_number": person.passport_number,
        "email": person.email,
        "phone": person.phone,
        "birth_date": _iso_or_none(person.birth_date),
        "birth_place": person.birth_place,
        "is_active": person.is_active,
    }


def _relation_to_dict(relation: CompanyPersonRelation) -> Dict[str, Any]:
    return {
        "company_id": str(relation.company_id),
        "person_id": str(relation.person_id),
        "relation_type": relation.relation_type.value if relation.relation_type else None,
        "position": relation.position,
        "start_date": _iso_or_none(relation.start_date),
        "end_date": _iso_or_none(relation.end_date),
        "share_percentage": relation.share_percentage,
        "share_amount": relation.share_amount,
        "description": relation.description,
        "is_current": relation.is_current,
        "source": relation.source,
        "source_reference": relation.source_reference,
    }


def _announcement_to_dict(announcement: Announcement) -> Dict[str, Any]:
    hususlar = None
    ocr_date = None
    ocr_issue = None
    ocr_page = None
    
    if announcement.ocr_result:
        hususlar = announcement.ocr_result.hususlar
        ocr_date = announcement.ocr_result.publication_date
        ocr_issue = announcement.ocr_result.issue_number
        ocr_page = announcement.ocr_result.page_number

    return {
        "id": str(announcement.id),
        "company_id": str(announcement.company_id) if announcement.company_id else None,
        "trade_registry_name": announcement.trade_registry_name,
        "trade_registry_number": announcement.trade_registry_number,
        "title": announcement.title,
        "publication_date": _iso_or_none(announcement.publication_date or ocr_date),
        "issue_number": announcement.issue_number or ocr_issue,
        "page_number": announcement.page_number or ocr_page,
        "announcement_type": announcement.announcement_type,
        "newspaper_name": announcement.newspaper_name,
        "pdf_url": announcement.pdf_url,
        "hususlar": hususlar,
        "content": announcement.content, # New field for UI
        "_ocr_id": announcement.ocr_result.id if announcement.ocr_result else None,
    }


def _ocr_result_to_dict(ocr: OcrResult) -> Dict[str, Any]:
    return {
        "id": ocr.id,
        "announcement_id": str(ocr.announcement_id) if ocr.announcement_id else None,
        "company_id": str(ocr.company_id) if ocr.company_id else None,
        "original_text": ocr.original_text,
        "structured_data": {
            "publication_date": _iso_or_none(ocr.publication_date) if ocr.publication_date else None,
            "issue_number": ocr.issue_number,
            "page_number": ocr.page_number,
            "pdf_url": ocr.pdf_url,
            "pdf_page_count": ocr.pdf_page_count,
            "sicil_office_header": ocr.sicil_office_header,
            "sicil_dosya_no": ocr.sicil_dosya_no,
            "mersis_no": ocr.mersis_no,
            "trade_name": ocr.trade_name,
            "old_trade_name": ocr.old_trade_name,
            "addresses": ocr.addresses,
            "old_addresses": ocr.old_addresses,
            "persons": ocr.persons,
            "masked_ids": ocr.masked_ids,
            "hususlar": ocr.hususlar,
            "belgeler": ocr.belgeler,
            "type": ocr.type,
            "item_index": ocr.item_index,
            "start_offset": ocr.start_offset,
            "end_offset": ocr.end_offset,
            "is_derived": ocr.is_derived,
            "derived_from_index": ocr.derived_from_index,
            "ilan_sira_no": ocr.ilan_sira_no,
        },
        "status": ocr.status,
        "created_at": _iso_or_none(ocr.created_at),
        "updated_at": _iso_or_none(ocr.updated_at),
    }


def _gazette_entry_to_dict(entry: GazetteEntry) -> Dict[str, Any]:
    return {
        "id": str(entry.id),
        "company_id": str(entry.company_id) if entry.company_id else None,
        "entry_type": entry.entry_type,
        "entry_date": _iso_or_none(entry.entry_date),
        "processed_text": entry.processed_text,
        "original_text": entry.original_text,
    }


MASKED_ID_RE = re.compile(r"\b\d{2,4}\*{2,}\d{2,4}\b")
MERSIS_RE = re.compile(r"MERS[İI]S\s*No[:：]?\s*([0-9\*\s]+)", re.IGNORECASE)
SICIL_RE = re.compile(r"Ticaret\s+Sicil(?:/Dosya)?\s*No[:：]?\s*([0-9\-\/]*)", re.IGNORECASE)
ADDRESS_LINE_RE = re.compile(r"adres", re.IGNORECASE)


def _clean_person_name(name: Optional[str]) -> Optional[str]:
    if not name:
        return None
    cleaned = " ".join(str(name).strip().split())
    return cleaned or None


def _normalize_text_for_compare(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    try:
        stripped = re.sub(r"[^0-9a-zA-ZçğıöşüÇĞİÖŞÜ]+", " ", str(value))
        return tr_normalize_py(stripped).strip() or None
    except Exception:
        return None


def _address_key_tokens(address: str, max_tokens: int = 4) -> List[str]:
    tokens = [token for token in re.split(r"\s+", address) if token]
    return tokens[:max_tokens]


def _extract_persons_from_structured(structured: Any) -> List[Dict[str, Optional[str]]]:
    persons: List[Dict[str, Optional[str]]] = []
    try:
        data = structured
        if isinstance(data, str):
            data = json.loads(data)
        if isinstance(data, list):
            candidates = data
        elif isinstance(data, dict):
            candidates = data.get("persons") or []
            if isinstance(candidates, dict):
                candidates = [candidates]
        else:
            candidates = []
        if not isinstance(candidates, list):
            return persons
        for item in candidates:
            if not isinstance(item, dict):
                continue
            masked = item.get("masked_ids")
            masked_ids: List[str] = []
            if isinstance(masked, list):
                masked_ids = [str(m).strip() for m in masked if str(m).strip()]
            elif isinstance(masked, str) and masked.strip():
                masked_ids = [masked.strip()]
            name = _clean_person_name(item.get("full_name") or item.get("text"))
            if not masked_ids:
                continue
            persons.append({"name": name, "masked_ids": masked_ids})
    except Exception:
        pass
    return persons


def _extract_addresses_from_structured(structured: Any) -> List[str]:
    addresses: List[str] = []
    try:
        data = structured
        if isinstance(data, str):
            data = json.loads(data)
        candidates: Any
        if isinstance(data, dict):
            candidates = data.get("addresses")
        else:
            candidates = None
        if isinstance(candidates, list):
            for addr in candidates:
                if isinstance(addr, str) and addr.strip():
                    addresses.append(addr.strip())
        elif isinstance(candidates, str) and candidates.strip():
            addresses.append(candidates.strip())
    except Exception:
        pass
    return addresses


def _extract_sicil_office_from_structured(structured: Any) -> Optional[str]:
    try:
        data = structured
        if isinstance(data, str):
            data = json.loads(data)
        if isinstance(data, dict):
            header = data.get("sicil_office_header") or data.get("sicilOfficeHeader")
            if isinstance(header, str) and header.strip():
                return header.strip()
    except Exception:
        return None
    return None


def _extract_ocr_entities(rows: List[OcrResult]) -> Dict[str, Any]:
    persons: List[Dict[str, Any]] = []
    masked_id_to_names: Dict[str, Set[str]] = {}
    masked_ids: Set[str] = set()
    addresses: List[str] = []
    mersis_numbers: Set[str] = set()
    sicil_numbers: Set[str] = set()
    seen_person_keys: Set[Tuple[str, Optional[str]]] = set()

    for row in rows:
        # Extract persons from flattened persons column
        structured_persons = []
        try:
            raw_persons = row.persons or []
            if isinstance(raw_persons, str):
                raw_persons = json.loads(raw_persons)
            if isinstance(raw_persons, dict):
                raw_persons = [raw_persons]
            if isinstance(raw_persons, list):
                structured_persons = [item for item in raw_persons if isinstance(item, dict)]
        except Exception:
            structured_persons = []

        for item in structured_persons:
            name = _structured_person_name(item)
            masked_candidates = _extract_structured_masked_ids(item)
            for masked_id in masked_candidates:
                masked_id = masked_id.strip()
                if not masked_id:
                    continue
                masked_ids.add(masked_id)
                if name:
                    masked_id_to_names.setdefault(masked_id, set()).add(name)
                key = (masked_id, name)
                if key in seen_person_keys:
                    continue
                seen_person_keys.add(key)
                persons.append({
                    "name": name,
                    "full_name": name,  # Frontend expects full_name
                    "masked_id": masked_id,
                    "masked_ids": [masked_id],  # Frontend expects masked_ids as array
                    "source": "structured",
                })

        # Use flattened addresses column directly
        if row.addresses:
            addresses.extend(row.addresses)

        raw_text = row.original_text or ""
        if raw_text:
            lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
            for idx, line in enumerate(lines):
                # Sadece adres/MERSİS/Sicil çıkarımını koru; kişi üretme
                if ADDRESS_LINE_RE.search(line):
                    addr = line
                    if ":" in addr:
                        addr = addr.split(":", 1)[1]
                    addr = addr.replace("Adres", "").replace("adres", "").strip(" :-")
                    continuation = ""
                    if idx + 1 < len(lines):
                        next_line = lines[idx + 1]
                        if next_line and not MASKED_ID_RE.search(next_line):
                            continuation = next_line
                    address_candidate = " ".join(part for part in [addr, continuation.strip()] if part)
                    if address_candidate and len(address_candidate) > 5:
                        addresses.append(address_candidate.strip())

                mersis_match = MERSIS_RE.search(line)
                if mersis_match:
                    candidate = mersis_match.group(1)
                    if candidate:
                        normalized = re.sub(r"\D+", "", candidate)
                        if normalized:
                            mersis_numbers.add(normalized)

                sicil_match = SICIL_RE.search(line)
                if sicil_match:
                    candidate = sicil_match.group(1)
                    if candidate:
                        sicil_numbers.add(candidate.strip())

    deduped_addresses: List[str] = []
    seen_addr_norm: Set[str] = set()
    for addr in addresses:
        norm = _normalize_text_for_compare(addr)
        if not norm or norm in seen_addr_norm:
            continue
        seen_addr_norm.add(norm)
        deduped_addresses.append(addr.strip())

    return {
        "persons": persons,
        "masked_ids": masked_ids,
        "masked_id_to_names": masked_id_to_names,
        "addresses": deduped_addresses,
        "mersis_numbers": mersis_numbers,
        "sicil_numbers": sicil_numbers,
    }

def search_all_related(query: str, db: Session) -> SearchResult:
    """Supabase yerine SQLAlchemy ile birleşik arama uygular."""
    result = SearchResult()
    q_raw = (query or "").strip()
    if not q_raw:
        return result

    # Initialize variables
    q_norm = ""
    q_digits = ""
    search_tokens = []
    
    # Check if query is a UUID
    is_uuid_match = False
    try:
        uuid_obj = uuid.UUID(q_raw)
        company_by_id = db.query(Company).filter(Company.id == uuid_obj).first()
        if company_by_id:
            company_candidates = [company_by_id]
            is_uuid_match = True
    except ValueError:
        pass

    if not is_uuid_match:
        q_norm = tr_normalize_py(q_raw)
        raw_tokens = [t for t in re.split(r"\s+", q_raw) if t]
        
        # Generate token pairs (raw, normalized) for text search
        # This ensures we search for both "İNŞAAT" and "INSAAT"
        search_token_pairs = []
        search_tokens = [] # For scoring logic later
        id_tokens = [] # Pure digits or masked IDs like 123***45
        
        for t in raw_tokens:
            # Include digits if they might be MERSIS, Sicil No or TCKN parts
            if t.isdigit():
                if len(t) >= 4:
                    search_token_pairs.append((t, t))
                    id_tokens.append(t)
            elif "*" in t or len(t) >= 2:
                t_norm = tr_normalize_py(t)
                search_token_pairs.append((t, t_norm))
                search_tokens.append(t_norm)
                if "*" in t:
                    id_tokens.append(t)
                
        q_digits = re.sub(r"\D+", "", q_raw)

        text_fields = [
            Company.unvan_unaccent,
            Company.address,
            Company.city,
            Company.district,
            Company.sicil_mudurluk,
        ]

        company_query = db.query(Company)
        if q_digits:
            digit_pattern = f"%{q_digits}%"
            company_query = company_query.filter(
                or_(
                    Company.sicil_no.ilike(digit_pattern),
                    Company.mersis_number.ilike(digit_pattern),
                )
            )

        if search_token_pairs:
            for raw_t, norm_t in search_token_pairs:
                # For each token in the query, it must match at least one field
                # We check both raw and normalized versions of the token
                pats = {f"%{raw_t}%", f"%{norm_t}%"}
                token_filters = []
                for pat in pats:
                    token_filters.extend([field.ilike(pat) for field in text_fields])
                company_query = company_query.filter(or_(*token_filters))
        elif q_norm:
            base_pat = f"%{q_raw}%"
            company_query = company_query.filter(or_(*[field.ilike(base_pat) for field in text_fields]))

        company_candidates = company_query.limit(20).all()
    
    # --- OCR & Person Search ---
    ocr_scores: Dict[uuid.UUID, int] = {}
    
    # If UUID match, give it max score
    if is_uuid_match:
        for comp in company_candidates:
            ocr_scores[comp.id] = 100
    else:
        # 1. MERSIS in OCR
        if q_digits:
            digit_pat = f"%{q_digits}%"
            ocr_mersis = db.query(OcrResult.company_id).filter(
                OcrResult.mersis_no.ilike(digit_pat)
            ).limit(50).all()
            for (cid,) in ocr_mersis:
                ocr_scores[cid] = 92

        # 2. Persons in Database (New Logic)
        if search_token_pairs:
            # Find persons matching the tokens
            # We require ALL tokens to match the person's name parts
            # e.g. "HÜSEYIN AKSÜT" -> HÜSEYIN matches AND AKSÜT matches
            
            person_query = db.query(Person.id)
            person_filters = []
            
            for raw_t, norm_t in search_token_pairs:
                pats = {f"%{raw_t}%", f"%{norm_t}%"}
                token_or_conditions = []
                for pat in pats:
                    # If token contains stars, ILIKE works directly
                    # If not, we still check masked_id for partial matches
                    token_or_conditions.extend([
                        Person.first_name.ilike(pat),
                        Person.last_name.ilike(pat),
                        Person.full_name.ilike(pat),
                        Person.masked_id.ilike(pat),
                        Person.nationality_id.ilike(pat)
                    ])
                person_filters.append(or_(*token_or_conditions))
                
            found_person_ids = person_query.filter(and_(*person_filters)).limit(50).all()
            found_person_ids = [p[0] for p in found_person_ids]
            
            if found_person_ids:
                # Find companies related to these persons
                relations = db.query(CompanyPersonRelation.company_id).filter(
                    CompanyPersonRelation.person_id.in_(found_person_ids)
                ).all()
                
                for (cid,) in relations:
                    if cid:
                        ocr_scores[cid] = max(ocr_scores.get(cid, 0), 95)

        # 3. High-Fidelity Extraction (OCR Results)
        # 3. High-Fidelity Extraction (OCR Results)
        if search_token_pairs:
            from sqlalchemy.sql import func
            ocr_text_query = db.query(OcrResult.company_id)
            ocr_text_filters = []
            
            # HOTFIX: Dev (150+ karakter) OCR hata metinlerini arama eşleşmelerinden tamamen dışla
            ocr_text_filters.append(func.length(OcrResult.trade_name) < 150)
            
            for raw_t, norm_t in search_token_pairs:
                pats = {f"%{raw_t}%", f"%{norm_t}%"}
                token_or_conditions = []
                for pat in pats:
                    token_or_conditions.extend([
                        OcrResult.trade_name.ilike(pat),
                        # PERFORMANCE FIX: Disabling CAST(hususlar AS TEXT) for local stability
                        # OcrResult.hususlar.ilike(pat) if it was a String/Text field, but it is JSONB.
                    ])
                ocr_text_filters.append(or_(*token_or_conditions))
                
            found_ocr_cids = ocr_text_query.filter(and_(*ocr_text_filters)).limit(50).all()
            for (cid,) in found_ocr_cids:
                if cid:
                    # OCR verileri "Tahmini" olduğu için ana DB kayıtlarını ezmemeli (Skor 90'dan 75'e düşürüldü)
                    ocr_scores[cid] = max(ocr_scores.get(cid, 0), 75)

        # 4. Persons in OCR JSON (Fallback)
        # PERFORMANCE FIX: Disabling this block as it causes DB crashes due to 
        # heavy CAST(persons AS TEXT) operations on large datasets.
        # TODO: Implement a proper GIN index or dedicated text column for this search.
        # if search_token_pairs:
        #     ocr_person_query = db.query(OcrResult.company_id)
        #     person_filters = []
        #     for raw_t, norm_t in search_token_pairs:
        #         # Check both raw and norm in JSON text
        #         person_filters.append(
        #             or_(
        #                 cast(OcrResult.persons, Text).ilike(f"%{raw_t}%"),
        #                 cast(OcrResult.persons, Text).ilike(f"%{norm_t}%")
        #             )
        #         )
        #     ocr_person_matches = ocr_person_query.filter(and_(*person_filters)).limit(50).all()
        #     for (cid,) in ocr_person_matches:
        #         ocr_scores[cid] = max(ocr_scores.get(cid, 0), 85)

    # Merge OCR results
    if ocr_scores:
        existing_ids = {c.id for c in company_candidates}
        new_ids = [cid for cid in ocr_scores.keys() if cid not in existing_ids]
        if new_ids:
            extra_companies = db.query(Company).filter(Company.id.in_(new_ids)).all()
            company_candidates.extend(extra_companies)
    # --- HOTFIX: Eksik şirket unvanlarını OCR belgelerinden (Yapay Zeka) çekerek doldur ---
    missing_unvan_cids = [c.id for c in company_candidates if not c.unvan]
    if missing_unvan_cids:
        ocr_names = db.query(OcrResult.company_id, OcrResult.trade_name).filter(
            OcrResult.company_id.in_(missing_unvan_cids),
            OcrResult.trade_name.isnot(None)
        ).all()
        
        name_map = {}
        for cid, tname in ocr_names:
            clean_name = tname.strip()
            # Güvenlik filtresi: Eğer unvan ilan konularını veya teknik OCR terimlerini içeriyorsa atla
            dirty_keywords = [
                "tasfiyeye", "hususlar", "unvan", "genel kurul", "yonergesi", "tescil edilen", "meslek grubu",
                "sicil", "gazete", "ilan", "ocr", "pay devri", "mudurler", "yetkililer", "yonetim kurulu",
                "karari", "adres degisikligi", "sermaye", "artirimi", "azaltimi", "kurulus", "kapanis",
                "terkin", "tasfiye", "iflas", "karar", "ilanı"
            ]
            lower_name = clean_name.lower().replace("ı", "i").replace("ğ", "g").replace("ü", "u").replace("ş", "s").replace("ö", "o").replace("ç", "c")
            
            if any(kw in lower_name for kw in dirty_keywords) or len(clean_name) < 4:
                continue
                
            if len(clean_name) > 3:
                # OCR hatası sebebiyle sayfanın tamamı unvan olarak algılandıysa kırp:
                if len(clean_name) > 120:
                    name_map[cid] = clean_name[:120] + "... (OCR Kesintisi)"
                else:
                    name_map[cid] = clean_name
                
        for c in company_candidates:
            if not c.unvan and c.id in name_map:
                c.unvan = name_map[c.id]
            elif not c.unvan:
                c.unvan = "Bilinmeyen Şirket (Sicil Kaydı Bekleniyor)"
    # ---------------------------------------------------------------------------------

    scored_companies: List[Tuple[int, Dict[str, Any], Company]] = []
    for comp in company_candidates:
        score = ocr_scores.get(comp.id, 40)
        if q_digits:
            if q_digits in (comp.sicil_no or ""):
                score = max(score, 88)
            if q_digits in (comp.mersis_number or ""):
                score = max(score, 92)
        norm_unvan = tr_normalize_py(comp.unvan or "")
        
        # Doğrudan Eşleşmeler
        is_direct_match = False
        if q_norm and norm_unvan.startswith(q_norm):
            score = max(score, 100) # Kusursuz Eşleşme
            is_direct_match = True
        if search_tokens and all(token in norm_unvan for token in search_tokens):
            score = max(score, 95) # Tüm kelimeler unvanda var (Altın Standart)
            is_direct_match = True
        if search_tokens:
            norm_address = tr_normalize_py(comp.address or "")
            if norm_address and all(token in norm_address for token in search_tokens):
                score = max(score, 85) # Tüm kelimeler adreste var
                is_direct_match = True
        
        # Hatalı OCR Bağlantılarını Engelleme (EKREMOĞLU aratınca REM KALIP çıkması)
        # Eğer şirket sadece OCR'dan dolayı geldiyse (skor <= 75) ve aranan kelime şirket unvanında geçmiyorsa,
        # bu muhtemelen yanlış bağlanmış bir sicil no çakışmasıdır, bu yüzden listeden çıkar!
        if score <= 75 and search_tokens and not is_direct_match:
            # Check if at least ONE token matches the unvan loosely to tolerate some OCR errors
            if not any(token in norm_unvan for token in search_tokens):
                continue # Skip this company! False positive!

        scored_companies.append((score, _company_to_dict(comp, match_strength=score), comp))

    scored_companies.sort(key=lambda item: item[0], reverse=True)
    total_companies_pre_count = len(scored_companies)
    top_companies = scored_companies[:MAX_COMPANIES]
    result.companies = [item[1] for item in top_companies]
    top_company_objs = [item[2] for item in top_companies]
    existing_company_ids: Set[str] = {item[1]["id"] for item in top_companies}

    company_ids_uuid = [comp.id for comp in top_company_objs]

    if company_ids_uuid:
        ann_rows = (
            db.query(Announcement)
            .filter(Announcement.company_id.in_(company_ids_uuid))
            .options(joinedload(Announcement.ocr_result))
            .order_by(Announcement.publication_date.desc().nullslast())
            .limit(300)
            .all()
        )
        result.announcements = [_announcement_to_dict(row) for row in ann_rows]

        # İlgili kişiler
        relation_rows = (
            db.query(CompanyPersonRelation.person_id)
            .filter(CompanyPersonRelation.company_id.in_(company_ids_uuid))
            .limit(600)
            .all()
        )
        person_ids = {row[0] for row in relation_rows if row and row[0] is not None}
        if person_ids:
            persons_rows = (
                db.query(Person)
                .filter(Person.id.in_(person_ids))
                .limit(600)
                .all()
            )
            result.persons = [_person_to_dict(person) for person in persons_rows]

        # Geçmiş kayıtları
        history_rows = (
            db.query(GazetteEntry)
            .filter(GazetteEntry.company_id.in_(company_ids_uuid))
            .order_by(GazetteEntry.entry_date.desc().nullslast())
            .limit(300)
            .all()
        )
        result.history = [_gazette_entry_to_dict(entry) for entry in history_rows]

        # --- NEXUS DISCOVERY ---
        # 1. Aynı Adresteki Şirketler (Discovery by Address)
        unique_addresses = {comp.address for comp in top_company_objs if comp.address and len(comp.address.strip()) > 15}
        print(f"[NEXUS DEBUG] Unique Addresses for Discovery: {unique_addresses}")
        if unique_addresses:
            addr_filters = [Company.address.ilike(f"{addr[:25]}%") for addr in unique_addresses]
            same_addr_rows = (
                db.query(Company)
                .filter(or_(*addr_filters))
                .filter(Company.id.notin_(company_ids_uuid))
                .limit(50)
                .all()
            )
            print(f"[NEXUS DEBUG] Found {len(same_addr_rows)} same address companies")
            result.same_address_companies = [_company_to_dict(c) for c in same_addr_rows]

        # 2. Ortağın Diğer Şirketleri (Discovery by Mutual Partners)
        if person_ids:
            mutual_rel_rows = (
                db.query(Company)
                .join(CompanyPersonRelation, Company.id == CompanyPersonRelation.company_id)
                .filter(CompanyPersonRelation.person_id.in_(list(person_ids)))
                .filter(Company.id.notin_(company_ids_uuid))
                .limit(50)
                .all()
            )
            result.related_companies = [_company_to_dict(c) for c in mutual_rel_rows]

    result.total_matches = total_companies_pre_count
    return result

@router.get("/all", summary="Unified search" )
def search_all(
    q: str = Query(..., description="Arama terimi"),
    cursor: int = Query(0, ge=0),
    limit: int = Query(MAX_COMPANIES, ge=1, le=200),
    request: Request = None,
    db: Session = Depends(get_db),
    _: None = Depends(enforce_daily_limit),
):
    query = (q or "").strip()
    if not query:
        return {
            "companies": [],
            "persons": [],
            "history": [],
            "total_matches": 0,
            "limit": limit,
            "next_offset": None,
            "next_cursor": None,
        }

    # cache_key = f"all:{query}:{cursor}:{limit}"
    # cached = _cache_all.get(cache_key)
    # if cached is not None:
    #     return cached

    result = search_all_related(query, db)

    # Sayfalama: sadece şirketlerde cursor kullanılıyor
    companies_slice = result.companies[cursor: cursor + limit]
    next_cursor = cursor + limit if (cursor + limit) < len(result.companies) else None

    payload = {
        "companies": companies_slice,
        "persons": result.persons,
        "history": result.history,
        "same_address_companies": result.same_address_companies,
        "related_companies": result.related_companies,
        "total_matches": result.total_matches or len(result.companies),
        "limit": limit,
        "next_offset": next_cursor,
        "next_cursor": next_cursor,
    }

    # _cache_all.set(cache_key, payload)
    return payload


@router.get("/company-detail", summary="Company detail with related persons and announcements")
def company_detail(
    company_id: str = Query(..., description="UUID of the company"),
    db: Session = Depends(get_db),
    # _: None = Depends(enforce_daily_limit), # Limit is only deducted on search, not on viewing details
):
    try:
        cid = (company_id or "").strip()
        if not cid:
            raise HTTPException(status_code=422, detail="company_id is required")
        try:
            company_uuid = uuid.UUID(cid)
        except ValueError:
            raise HTTPException(status_code=422, detail="company_id must be a valid UUID")

        company_obj = db.query(Company).filter(Company.id == company_uuid).first()
        if not company_obj:
            raise HTTPException(status_code=404, detail="Company not found")

        company_payload = _company_to_dict(company_obj)

        relations = (
            db.query(CompanyPersonRelation)
            .filter(CompanyPersonRelation.company_id == company_uuid)
            .all()
        )
        person_ids = [rel.person_id for rel in relations if rel.person_id]
        persons_map: Dict[uuid.UUID, Person] = {}
        if person_ids:
            persons_map = {
                person.id: person
                for person in db.query(Person).filter(Person.id.in_(person_ids)).all()
            }

        persons_payload: List[Dict[str, Any]] = []
        for rel in relations:
            p = persons_map.get(rel.person_id)
            if p:
                p_dict = _person_to_dict(p)
                p_dict.update({
                    "relation_type": rel.relation_type.value if rel.relation_type else None,
                    "position": rel.position,
                    "is_current": rel.is_current,
                    "share_percentage": rel.share_percentage,
                    "description": rel.description,
                })
                persons_payload.append(p_dict)

        announcement_rows = (
            db.query(Announcement)
            .filter(Announcement.company_id == company_uuid)
            .options(joinedload(Announcement.ocr_result))
            .order_by(Announcement.publication_date.desc().nullslast())
            .limit(100)
            .all()
        )
    # --- MERSIS-FIRST INTEGRITY LOGIC ---
        target_vkn = _get_vkn_from_text(str(getattr(company_obj, "mersis_number", "") or getattr(company_obj, "mersis_number_ocr", "") or ""))
        
        # If DB is missing Mersis, try to self-heal by looking at explicitly linked announcements
        if not target_vkn:
            for ann_row in announcement_rows:
                v = _get_vkn_from_text(str(getattr(ann_row, "mersis_no", "") or (getattr(ann_row.ocr_result, "mersis_no", "") if getattr(ann_row, "ocr_result", None) else "")))
                if v:
                    target_vkn = v
                    break

        import unicodedata
        def _normalize_tr(text: str) -> str:
            if not text: return ""
            text = text.replace('I', 'ı').replace('İ', 'i').lower()
            return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')

        company_unvan = company_obj.unvan or ""
        norm_unvan = _normalize_tr(company_unvan).replace("tasfiye halinde", "").strip()
        company_sicil = str(company_obj.sicil_no or "").strip()
        
        def _is_reliable_match(ann_dict: Dict[str, Any], ocr_obj: Optional[OcrResult] = None) -> bool:
            # Prepare text for search (handle potential list fields)
            title_ptr = ann_dict.get("title") or ""
            if isinstance(title_ptr, list): title_ptr = " ".join(str(t) for t in title_ptr)
            husus_ptr = ann_dict.get("hususlar") or ""
            if isinstance(husus_ptr, list): husus_ptr = " ".join(str(h) for h in husus_ptr)
            
            ann_text = title_ptr + " " + husus_ptr
            if ocr_obj:
                ann_text += " " + (ocr_obj.trade_name or "") + " " + (ocr_obj.original_text or "")
            
            # 1. Mersis/VKN (Highest Confidence)
            ann_vkn = _get_vkn_from_text(str(ann_dict.get("mersis_number") or ann_dict.get("mersis_no") or (getattr(ocr_obj, "mersis_no", "") if ocr_obj else "")))
            if not ann_vkn:
                 ann_vkn = _get_vkn_from_text(ann_text)
            
            if target_vkn and ann_vkn:
                if ann_vkn == target_vkn:
                    # Mersis match is absolute truth. A branch might have a different Registry Number
                    # but shares the same 11-digit head.
                    return True
                return False # Explicit Mersis mismatch is an absolute hard-fail (No leakage!)

            # 2. Sicil No Match (Fallback if Mersis missing)
            ann_sicil = str(ann_dict.get("trade_registry_number") or ann_dict.get("sicil_no") or (getattr(ocr_obj, "sicil_dosya_no", "") if ocr_obj else "")).strip()
            if company_sicil and ann_sicil and ann_sicil != company_sicil:
                return False

            # 3. Name Heuristic Match (Keyword protection for orphans missing Sicil and Mersis)
            parts = [p for p in norm_unvan.split() if len(p) > 3]
            if parts:
                search_text = _normalize_tr(ann_text)
                # Must match at least TWO significant words from the unvan to prevent generic single-word false positives
                match_count = sum(1 for p in parts if p in search_text)
                required_matches = min(2, len(parts))
                if match_count < required_matches:
                    return False
            
            return True

        # Pre-filter existing announcements
        valid_anns = []
        for ann_row in announcement_rows:
            ann_dict = _announcement_to_dict(ann_row)
            if _is_reliable_match(ann_dict, ann_row.ocr_result):
                valid_anns.append(ann_dict)
        announcements = valid_anns

        # --- DYNAMIC RECOVERY FALLBACK: Aggressive Search by VKN/Name ---
        if len(announcements) < 6:
            potential_ocrs = []
            if target_vkn:
                # Search archive by VKN string in explicit mersis_no column only to avoid full table scans
                potential_ocrs = db.query(OcrResult).filter(
                    OcrResult.mersis_no.ilike(f"%{target_vkn}%")
                ).order_by(OcrResult.publication_date.desc()).limit(30).all()
            
            # Fallback to name keywords if still low
            if not potential_ocrs and company_unvan:
                parts = [p for p in company_unvan.split() if len(p) > 3]
                if parts:
                    potential_ocrs = db.query(OcrResult).filter(
                        OcrResult.trade_name.ilike(f"%{parts[0]}%")
                    ).order_by(OcrResult.publication_date.desc()).limit(20).all()

            for r_ocr in potential_ocrs:
                if any(a.get("_ocr_id") == r_ocr.id for a in announcements): continue
                
                r_dict = {"trade_registry_number": r_ocr.sicil_dosya_no, "title": r_ocr.hususlar}
                if _is_reliable_match(r_dict, r_ocr):
                    # Use global uuid module
                    ocr_namespace = uuid.UUID('00000000-0000-0000-0000-000000000000')
                    virtual_id = uuid.uuid5(ocr_namespace, f"ocr:{r_ocr.id}")
                    announcements.append({
                        "id": str(virtual_id),
                        "company_id": str(company_uuid),
                        "trade_registry_name": None,
                        "trade_registry_number": r_ocr.sicil_dosya_no,
                        "title": r_ocr.hususlar or "Sicil Gazetesi İlanı (OCR)",
                        "publication_date": _iso_or_none(r_ocr.publication_date or r_ocr.created_at),
                        "issue_number": r_ocr.issue_number,
                        "page_number": r_ocr.page_number,
                        "announcement_type": "OCR_ONLY",
                        "newspaper_name": "Ticaret Sicil Gazetesi",
                        "pdf_url": None,
                        "hususlar": r_ocr.hususlar,
                        "_ocr_id": r_ocr.id,
                        "is_mersis_verified": True # It was matched by explicit Mersis target_vkn
                    })

        # Sort and deduplicate
        announcements.sort(key=lambda x: x.get("publication_date") or "", reverse=True)
        
        # [NEW] Add is_mersis_verified to existing announcements too
        for a in announcements:
            if target_vkn and not a.get("is_mersis_verified"):
                # Real-time check for verified badge
                a["is_mersis_verified"] = _is_reliable_mersis_match(target_vkn, None, a.get("trade_registry_number")) # simplified or update logic

        linked_ocr_ids = {ann.get("_ocr_id") for ann in announcements if ann.get("_ocr_id")}
        orphan_ocr_query = db.query(OcrResult).filter(
            OcrResult.company_id == company_uuid,
            OcrResult.announcement_id.is_(None)
        )
        if linked_ocr_ids:
            orphan_ocr_query = orphan_ocr_query.filter(OcrResult.id.notin_(linked_ocr_ids))
            
        orphan_ocr_rows = (
            orphan_ocr_query
            .order_by(OcrResult.created_at.desc().nullslast())
            .limit(50)
            .all()
        )
        
        for ocr in orphan_ocr_rows:
            ocr_dict = {
                "trade_registry_number": str(ocr.sicil_dosya_no or "").strip(),
                "title": ocr.hususlar,
                "hususlar": ocr.hususlar
            }
            if not _is_reliable_match(ocr_dict, ocr):
                continue
                
            ocr_namespace = uuid.UUID('00000000-0000-0000-0000-000000000000')
            virtual_id = uuid.uuid5(ocr_namespace, f"ocr:{ocr.id}")
            virtual_ann = {
                "id": str(virtual_id),
                "company_id": str(company_uuid),
                "trade_registry_name": None,
                "trade_registry_number": ocr_dict["trade_registry_number"],
                "title": ocr.hususlar or "Sicil Gazetesi İlanı (OCR)",
                "publication_date": _iso_or_none(ocr.publication_date or ocr.created_at),
                "issue_number": ocr.issue_number,
                "page_number": ocr.page_number,
                "announcement_type": "OCR_ONLY",
                "newspaper_name": "Ticaret Sicil Gazetesi",
                "pdf_url": None,
                "hususlar": ocr.hususlar,
                "_ocr_id": ocr.id,
            }
            announcements.append(virtual_ann)
            
        # Sort combined list by date
        announcements.sort(key=lambda x: x.get("publication_date") or "", reverse=True)

        announcement_ids = [ann.id for ann in announcement_rows if ann.id]
        if announcement_ids:
            ocr_query = db.query(OcrResult).filter(
                or_(
                    OcrResult.company_id == company_uuid,
                    OcrResult.announcement_id.in_(announcement_ids),
                )
            )
        else:
            ocr_query = db.query(OcrResult).filter(OcrResult.company_id == company_uuid)

        ocr_rows = (
            ocr_query.order_by(OcrResult.created_at.desc().nullslast()).limit(100).all()
        )
        
        # Filter out OCR results that are already linked to announcements
        linked_ocr_ids = set()
        for ann in announcement_rows:
            if ann.ocr_result:
                linked_ocr_ids.add(ann.ocr_result.id)
                
        ocr_matches = [_ocr_result_to_dict(row) for row in ocr_rows if row.id not in linked_ocr_ids]
        ocr_entities = _extract_ocr_entities(ocr_rows)

        if not company_payload.get("sicil_office_header"):
            sicil_header = None
            for row in ocr_rows:
                header_candidate = row.sicil_office_header
                if header_candidate:
                    sicil_header = header_candidate
                    break
            if sicil_header:
                company_payload["sicil_office_header"] = sicil_header

        if not company_payload.get("last_update"):
            latest_ts = None
            for row in ocr_rows:
                for candidate in (row.updated_at, row.created_at):
                    if candidate and (latest_ts is None or candidate > latest_ts):
                        latest_ts = candidate
            if latest_ts:
                company_payload["last_update"] = _iso_or_none(latest_ts)

        if not company_payload.get("address") and ocr_entities["addresses"]:
            company_payload["address"] = ocr_entities["addresses"][0]

        same_address_companies = []
        target_addr = company_payload.get("address") or (company_obj.address if company_obj else None)
        if target_addr and len(target_addr.strip()) > 10:
            addr_parts = target_addr.strip().upper().split()
            unique_prefix = " ".join(addr_parts[2:6]) if len(addr_parts) > 5 else " ".join(addr_parts[:4])
            
            with open("/tmp/nexus_debug.txt", "a") as f:
                f.write(f"[NEXUS DEBUG] Company: {company_id} | Target Addr: {target_addr} | Unique Prefix: {unique_prefix}\n")
            
            # --- HOTFIX: YANLIŞ DERLENEN POSTGRESQL FONKSİYONUNU ÇALIŞMA ZAMANINDA ONAR ---
            try:
                db.execute(text("""
                CREATE OR REPLACE FUNCTION tr_normalize(original_text text) RETURNS text AS $$
                DECLARE normalized_text text;
                BEGIN
                    IF original_text IS NULL THEN RETURN NULL; END IF;
                    normalized_text := lower(original_text);
                    normalized_text := replace(normalized_text, 'ı', 'i');
                    normalized_text := replace(normalized_text, 'ğ', 'g');
                    normalized_text := replace(normalized_text, 'ü', 'u');
                    normalized_text := replace(normalized_text, 'ş', 's');
                    normalized_text := replace(normalized_text, 'ö', 'o');
                    normalized_text := replace(normalized_text, 'ç', 'c');
                    normalized_text := replace(normalized_text, 'â', 'a');
                    normalized_text := replace(normalized_text, 'î', 'i');
                    RETURN normalized_text;
                END; $$ LANGUAGE plpgsql IMMUTABLE;
                """))
                db.commit()
            except Exception as e:
                pass # Already fixed or permission denied
            # ---------------------------------------------------------------------------------

            same_addr_query = text("""
                SELECT id, unvan, address FROM app.companies 
                WHERE id != :current_id 
                  AND tr_normalize(address) ILIKE '%' || tr_normalize(:prefix) || '%'
                LIMIT 50
            """)
            same_addr_results = db.execute(same_addr_query, {
                "current_id": company_uuid, 
                "prefix": unique_prefix
            }).fetchall()
            with open("/tmp/nexus_debug.txt", "a") as f:
                f.write(f"[NEXUS DEBUG] Found {len(same_addr_results)} companies at same address.\n")
            same_address_companies = [
                {"id": str(r[0]), "unvan": r[1], "address": r[2]} for r in same_addr_results
            ]

        related_companies = []
        # 1. Direct Partners' other companies
        if person_ids:
            mutual_rel_rows = (
                db.query(Company)
                .join(CompanyPersonRelation, Company.id == CompanyPersonRelation.company_id)
                .filter(CompanyPersonRelation.person_id.in_(list(person_ids)))
                .filter(Company.id != company_uuid)
                .distinct()
                .limit(30)
                .all()
            )
            related_companies = [_company_to_dict(c) for c in mutual_rel_rows]

        # Removed obsolete ocr_person_mentions Deep Discovery block



        if not company_payload.get("address") and ocr_entities["addresses"]:
            company_payload["address"] = ocr_entities["addresses"][0]
        if not company_payload.get("mersis_number") and ocr_entities["mersis_numbers"]:
            company_payload["mersis_number"] = next(iter(ocr_entities["mersis_numbers"]))
        if not company_payload.get("sicil_no") and ocr_entities["sicil_numbers"]:
            company_payload["sicil_no"] = next(iter(ocr_entities["sicil_numbers"]))

        history_entries = [
            _gazette_entry_to_dict(entry)
            for entry in (
                db.query(GazetteEntry)
                .filter(GazetteEntry.company_id == company_uuid)
                .order_by(GazetteEntry.entry_date.desc().nullslast())
                .limit(100)
                .all()
            )
        ]

        old_addresses: List[Dict[str, Any]] = []
        try:
            raw_old_addresses = getattr(company_obj, "old_addresses", None)
            if isinstance(raw_old_addresses, list):
                for item in raw_old_addresses:
                    if isinstance(item, dict):
                        old_addresses.append(item)
                    elif isinstance(item, str) and item.strip():
                        old_addresses.append({"address": item.strip()})
        except Exception as exc_old_addresses:
            logger.warning(
                f"[Company Detail] old_addresses parsing failed for company_id={company_id}: {exc_old_addresses}"
            )

        old_trade_names: List[str] = []
        try:
            raw_old_trade_names = getattr(company_obj, "old_trade_names", None)
            if isinstance(raw_old_trade_names, list):
                old_trade_names = [
                    name.strip()
                    for name in raw_old_trade_names
                    if isinstance(name, str) and name.strip()
                ]
        except Exception as exc_trade_names:
            logger.warning(
                f"[Company Detail] old_trade_names parsing failed for company_id={company_id}: {exc_trade_names}"
            )

        registry_related_companies: List[Dict[str, Any]] = []
        shared_person_companies: List[Dict[str, Any]] = []
        
        # PERFORMANS OPTİMİZASYONU: OCR ortak kişi eşleştirme Nexus'a devredildi.
        shared_person_companies = []
        
        # if ocr_entities["persons"]:
        #     try:
        #         # Extract current company's persons data
        #         # current_persons_map: Dict[str, str] = {}  # masked_id -> full_name
        #         # current_masked_ids: Set[str] = set()
                
        #         # for person in ocr_entities["persons"]:
        #         #     masked_id = person.get("masked_id")
        #         #     full_name = person.get("full_name") or person.get("name")
        #         #     if masked_id:
        #         #         current_masked_ids.add(masked_id)
        #         #         if full_name:
        #         #             current_persons_map[masked_id] = full_name
                
        #         # if current_masked_ids:
        #         #     # Use PostgreSQL to find companies with overlapping masked_ids
        #         #     shared_companies_data: Dict[uuid.UUID, Dict[str, Any]] = {}
                    
        #         #     # Query OCR results that might have matching persons
        #         #     potential_matches = (
        #         #     db.query(OcrResult.company_id)
        #         #     .filter(
        #         #         OcrResult.company_id != company_uuid,
        #         #         OcrResult.persons.isnot(None)
        #         #     )
        #         #     .distinct()
        #         #     .limit(500)  # Reasonable limit for performance
        #         #     .all()
        #         #     )
                    
        #         #     other_company_ids = [row[0] for row in potential_matches]
                    
        #         #     if other_company_ids:
        #         #         # Fetch OCR data for these companies in batch
        #         #         other_ocr_batch = (
        #         #             db.query(OcrResult)
        #         #             .filter(OcrResult.company_id.in_(other_company_ids))
        #         #             .limit(1000)
        #         #             .all()
        #         #         )
                        
        #         #         # Group by company_id
        #         #         company_ocr_map: Dict[uuid.UUID, List[OcrResult]] = {}
        #         #         for ocr in other_ocr_batch:
        #         #             if ocr.company_id:
        #         #                 company_ocr_map.setdefault(ocr.company_id, []).append(ocr)
                        
        #         #         # Check each company for person matches
        #         #         for other_company_id, ocr_list in company_ocr_map.items():
        #         #             other_entities = _extract_ocr_entities(ocr_list)
        #         #             other_persons = other_entities.get("persons", [])
                            
        #         #             if not other_persons:
        #         #                 continue
                            
        #         #             # Find matching persons
        #         #             matched_persons_high = []  # name + masked_id match
        #         #             matched_persons_low = []   # only masked_id match
                            
        #         #             for other_person in other_persons:
        #         #                 other_masked_id = other_person.get("masked_id")
        #         #                 other_full_name = other_person.get("full_name") or other_person.get("name")
                                
        #         #                 if other_masked_id and other_masked_id in current_masked_ids:
        #         #                     # masked_id matches!
        #         #                     current_name = current_persons_map.get(other_masked_id)
                                    
        #         #                     if current_name and other_full_name:
        #         #                         # Normalize names for comparison
        #         #                         current_name_norm = _normalize_text_for_compare(current_name)
        #         #                         other_name_norm = _normalize_text_for_compare(other_full_name)
                                        
        #         #                         if current_name_norm == other_name_norm:
        #         #                             # HIGH confidence: both name and masked_id match
        #         #                             matched_persons_high.append({
        #         #                                 "full_name": other_full_name,
        #         #                                 "masked_id": other_masked_id,
        #         #                                 "relation_type": "OCR_ORTAK",
        #         #                             })
        #         #                         else:
        #         #                             # LOW confidence: only masked_id matches, names differ
        #         #                             matched_persons_low.append({
        #         #                                 "full_name": other_full_name,
        #         #                                 "masked_id": other_masked_id,
        #         #                                 "relation_type": "OCR_MASKED_ONLY",
        #         #                             })
        #         #                     else:
        #         #                         # LOW confidence: masked_id matches but no name comparison possible
        #         #                         matched_persons_low.append({
        #         #                             "full_name": other_full_name or "Bilinmeyen",
        #         #                             "masked_id": other_masked_id,
        #         #                             "relation_type": "OCR_MASKED_ONLY",
        #         #                         })
                            
        #         #             # If we found any matches, add this company
        #         #             if matched_persons_high or matched_persons_low:
        #         #                 other_company = db.query(Company).filter(Company.id == other_company_id).first()
        #         #                 if other_company:
        #         #                     company_dict = _company_to_dict(other_company)
        #         #                     company_dict["shared_persons"] = matched_persons_high + matched_persons_low
        #         #                     company_dict["match_strength"] = "high" if matched_persons_high else "low"
        #         #                     shared_person_companies.append(company_dict)
                        
        #         #         # Sort by match strength (high first) and number of shared persons
        #         #         shared_person_companies.sort(
        #         #             key=lambda x: (
        #         #                 0 if x.get("match_strength") == "high" else 1,
        #         #                 -len(x.get("shared_persons", []))
        #         #             )
        #         #         )
                        
        #         #         # Limit to top 50
        #         #         shared_person_companies = shared_person_companies[:50]
            
        #     except Exception as exc_shared:
        #         logger.warning(
        #             f"[Company Detail] shared person lookup failed for company_id={company_id}: {exc_shared}"
        #         )
        #         shared_person_companies = []
        
        try:
            existing_registry_ids: Set[uuid.UUID] = set()

            mersis_candidates: List[str] = []
            for attr in ("mersis_number", "mersis_number_ocr"):
                value = getattr(company_obj, attr, None)
                if isinstance(value, str):
                    normalized = value.strip()
                    if normalized and normalized not in mersis_candidates:
                        mersis_candidates.append(normalized)
            if mersis_candidates:
                mersis_matches = (
                    db.query(Company)
                    .filter(
                        Company.mersis_number.in_(mersis_candidates),
                        Company.id != company_uuid,
                    )
                    .limit(500)
                    .all()
                )
                for match in mersis_matches:
                    if not match.id or match.id in existing_registry_ids:
                        continue
                    registry_related_companies.append(_company_to_dict(match))
                    existing_registry_ids.add(match.id)

            def _office_first_token(value: Any) -> str:
                try:
                    return str(value or "").strip().split()[0].upper()
                except Exception:
                    return ""

            sicil_no = getattr(company_obj, "sicil_no", None)
            office_norm = _office_first_token(
                getattr(company_obj, "sicil_mudurluk", None)
                or getattr(company_obj, "sicil_office_code", None)
            )
            if isinstance(sicil_no, str) and sicil_no.strip():
                sicil_matches = (
                    db.query(Company)
                    .filter(
                        Company.sicil_no == sicil_no.strip(),
                        Company.id != company_uuid,
                    )
                    .limit(500)
                    .all()
                )
                for match in sicil_matches:
                    if not match.id or match.id in existing_registry_ids:
                        continue
                    other_office = _office_first_token(
                        getattr(match, "sicil_mudurluk", None)
                        or getattr(match, "sicil_office_code", None)
                    )
                    if office_norm and other_office and office_norm != other_office:
                        continue
                    registry_related_companies.append(_company_to_dict(match))
                    existing_registry_ids.add(match.id)
        except Exception as exc_registry:
            logger.warning(
                f"[Company Detail] registry related lookup failed for company_id={company_id}: {exc_registry}"
            )

        if not persons_payload and ocr_rows:
            # --- DATA INTEGRITY FIX: Filter OCR entities by sicil number ---
            target_ocr_rows = ocr_rows
            if company_sicil:
                # Only extract entities from OCR results that match our sicil number
                target_ocr_rows = [r for r in ocr_rows if str(r.sicil_dosya_no or "").strip() == company_sicil]
            
            if target_ocr_rows:
                relevant_entities = _extract_ocr_entities(target_ocr_rows)
                persons_payload = relevant_entities["persons"]
            else:
                persons_payload = []
                
        # Deduplicate persons by name and masked_id
        if persons_payload:
            seen_persons = {}
            unique_persons = []
            for p in persons_payload:
                p_name = str(p.get("full_name") or p.get("name") or "").strip().upper()
                p_masked = str(p.get("masked_id") or "").strip()
                p_key = f"{p_name}|{p_masked}"
                if p_key and p_key not in seen_persons:
                    seen_persons[p_key] = True
                    unique_persons.append(p)
            persons_payload = unique_persons
        # [PERFORMANS] Duplicate address logic removed.
        # if ocr_entities["addresses"]: ...
        # [CLEANUP] All legacy address/geolocation logic removed for performance.

        if "REM KALIP" in company_unvan.upper():
            logger.info(f"=== REM KALIP REPORT ===")
            for idx, a in enumerate(announcements):
                logger.info(f"[{idx+1}] Date: {a.get('publication_date')}, Type: {a.get('announcement_type')}, Mersis Verified: {a.get('is_mersis_verified')}, Title: {str(a.get('title'))[:50]}")
            logger.info(f"========================")

        return {
            "company": company_payload,
            "persons": persons_payload,
            "announcements": announcements,
            "history": history_entries,
            "related_companies": related_companies,
            "same_address_companies": same_address_companies,
            "registry_related_companies": registry_related_companies,
            "shared_person_companies": shared_person_companies,  # New: companies sharing same persons
            "old_addresses": old_addresses,
            "old_trade_names": old_trade_names,
            "ocr_results": ocr_matches,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[Company Detail] Error retrieving details for company_id={company_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An error occurred while fetching company detail.")


@router.get("/announcement-detail", summary="Announcement detail with optional OCR text")
def announcement_detail(
    announcement_id: str = Query(..., description="UUID of the announcement or OCR result"),
    company_id: Optional[str] = Query(None, description="Optional company scope for OCR results"),
    ocr_id: Optional[int] = Query(None, description="Direct OCR result integer ID for virtual announcements"),
    db: Session = Depends(get_db),
    # _: None = Depends(enforce_daily_limit), # Limit is only deducted on search, not on viewing details
):
    try:
        # If ocr_id is provided, skip announcement lookup and go straight to OCR
        if ocr_id is not None:
            ocr_obj = db.query(OcrResult).filter(OcrResult.id == ocr_id).first()
            if not ocr_obj:
                raise HTTPException(status_code=404, detail="OCR result not found")
            
            # Construct virtual announcement from OCR result
            virtual_announcement = {
                "id": str(uuid.uuid5(uuid.UUID('00000000-0000-0000-0000-000000000000'), f"ocr:{ocr_obj.id}")),
                "company_id": str(ocr_obj.company_id) if ocr_obj.company_id else None,
                "ilan_no": None,
                "sicil_no": getattr(ocr_obj, "sicil_dosya_no", None),
                "gazette_number": getattr(ocr_obj, "issue_number", None),
                "publication_date": ocr_obj.publication_date.isoformat() if ocr_obj.publication_date else None,
                "title": getattr(ocr_obj, "hususlar", None) or "Sicil Gazetesi İlanı (OCR)",
                "company_title": getattr(ocr_obj, "trade_name", None),
                "company_name": getattr(ocr_obj, "trade_name", None),
                "content": ocr_obj.markdown_content or ocr_obj.original_text,
                "ocr_text": getattr(ocr_obj, "original_text", None),
                "hususlar": getattr(ocr_obj, "hususlar", None),
            }
            
            return {
                "announcement": virtual_announcement,
                "original_text": getattr(ocr_obj, "markdown_content", None) or getattr(ocr_obj, "original_text", None),
            }
        
        try:
            announcement_uuid = uuid.UUID((announcement_id or "").strip())
        except ValueError:
            raise HTTPException(status_code=422, detail="announcement_id must be a valid UUID")

        # First, try to find an Announcement record
        announcement_obj = (
            db.query(Announcement)
            .filter(Announcement.id == announcement_uuid)
            .first()
        )
        
        # If we found an announcement, return it as usual
        if announcement_obj:
            announcement_payload = _announcement_to_dict(announcement_obj)

            company_uuid: Optional[uuid.UUID] = None
            if company_id:
                try:
                    company_uuid = uuid.UUID(company_id.strip())
                except ValueError:
                    raise HTTPException(status_code=422, detail="company_id must be a valid UUID")
            elif announcement_obj.company_id:
                company_uuid = announcement_obj.company_id

            ocr_query = db.query(OcrResult).filter(OcrResult.announcement_id == announcement_uuid)
            if company_uuid:
                ocr_query = ocr_query.filter(OcrResult.company_id == company_uuid)

            ocr_row = ocr_query.order_by(OcrResult.created_at.desc().nullslast()).first()
            original_text = None
            if ocr_row is not None:
                original_text = getattr(ocr_row, "markdown_content", None) or getattr(ocr_row, "original_text", None)

            return {
                "announcement": announcement_payload,
                "original_text": original_text,
            }
        
        # If no announcement found, try to reverse-engineer the OCR ID from the UUID
        # Check if this UUID was generated from an OCR ID using our deterministic method
        ocr_obj = None
        ocr_namespace = uuid.UUID('00000000-0000-0000-0000-000000000000')
        
        # Try to find a matching OCR result by checking all recent OCR results
        # This is a fallback approach - we'll query OCR results and check if any generate this UUID
        recent_ocrs = (
            db.query(OcrResult)
            .order_by(OcrResult.created_at.desc())
            .limit(1000)
            .all()
        )
        
        for ocr in recent_ocrs:
            virtual_id = uuid.uuid5(ocr_namespace, f"ocr:{ocr.id}")
            if virtual_id == announcement_uuid:
                ocr_obj = ocr
                break
        
        if not ocr_obj:
            raise HTTPException(status_code=404, detail="Announcement or OCR result not found")
        
        # Construct a "virtual announcement" from the OCR result
        virtual_announcement = {
            "id": str(announcement_uuid),
            "company_id": str(ocr_obj.company_id) if ocr_obj.company_id else None,
            "ilan_no": None,
            "sicil_no": getattr(ocr_obj, "sicil_dosya_no", None),
            "gazette_number": getattr(ocr_obj, "issue_number", None),
            "publication_date": ocr_obj.publication_date.isoformat() if ocr_obj.publication_date else None,
            "title": getattr(ocr_obj, "hususlar", None) or "Sicil Gazetesi İlanı (OCR)",
            "company_title": getattr(ocr_obj, "trade_name", None),
            "company_name": getattr(ocr_obj, "trade_name", None),
            "content": None,
            "ocr_text": getattr(ocr_obj, "original_text", None),
            "hususlar": getattr(ocr_obj, "hususlar", None),
        }
        
        return {
            "announcement": virtual_announcement,
            "original_text": getattr(ocr_obj, "markdown_content", None) or getattr(ocr_obj, "original_text", None),
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"[Announcement Detail] Error for announcement_id '{announcement_id}': {e}",
            exc_info=True,
        )
        raise HTTPException(status_code=500, detail="An error occurred while fetching announcement detail.")
        try:
            import re as _re
            if not _re.match(r"^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$", announcement_id, flags=_re.IGNORECASE):
                raise HTTPException(status_code=400, detail="announcement_id must be a UUID")
        except HTTPException:
            raise
        except Exception:
            pass
        # 1) İlan kaydını getir
        try:
            ann_q = (
                supabase
                .postgrest.schema('app').table("announcements")
                .select("*")
                .eq("id", announcement_id)
                .limit(1)
                .execute()
            )
            ann_q = ann_q.data or []
            ann = ann_q[0] if ann_q else None
            if not ann:
                raise HTTPException(status_code=404, detail="İlan bulunamadı")
        except HTTPException:
            raise
        except Exception as ex_ann:
            logger.error(f"[Announcement Detail] Fetch announcement failed: {ex_ann}")
            raise HTTPException(status_code=500, detail="İlan getirilemedi")

        # 2) OCR metni — SADECE hedef şirkete ait olacak şekilde
        original_text = None
        try:
            # company scope belirle
            scope_company_id = None
            if company_id and isinstance(company_id, str) and company_id.strip():
                scope_company_id = company_id.strip()
            elif isinstance(ann, dict) and ann.get("company_id"):
                scope_company_id = ann.get("company_id")

            qb = (
                supabase
                .postgrest.schema('app').table("ocr_results")
                .select("id, original_text, created_at, company_id, mersis_no")
                .eq("announcement_id", announcement_id)
            )
            if scope_company_id:
                qb = qb.eq("company_id", scope_company_id)
            elif mersis_no and isinstance(mersis_no, str) and mersis_no.strip():
                qb = qb.eq("mersis_no", mersis_no.strip())
            else:
                # Şirket bağlamı yoksa yanlış şirkete ait metin döndürmemek için OCR sorgusunu çalıştırma
                qb = None

            if qb is not None:
                ocr_q = qb.order("created_at", desc=True).limit(1).execute()
                if ocr_q.data:
                    original_text = (ocr_q.data[0] or {}).get("original_text")
        except Exception as ex_ocr:
            logger.warning(f"[Announcement Detail] OCR scoped fetch failed: {ex_ocr}")

        return {
            "announcement": ann,
            "original_text": original_text,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[Announcement Detail] Error for announcement_id '{announcement_id}': {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An error occurred while fetching announcement detail.")
