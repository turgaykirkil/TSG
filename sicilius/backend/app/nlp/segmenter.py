# -*- coding: utf-8 -*-
from __future__ import annotations
import re
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Tuple, Optional

import orjson
from rapidfuzz import fuzz, process
import dateparser
from unidecode import unidecode  # noqa: F401  # gelecekte normalizasyon varyantları için
import phonenumbers

# ------------------------------------------------------------
# Yardımcı: Güvenli JSON dump (hızlı)
# ------------------------------------------------------------

def dump_json(obj: Any) -> str:
    return orjson.dumps(obj, option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SERIALIZE_NUMPY).decode("utf-8")


# ------------------------------------------------------------
# Normalizasyon + ortak yardımcılar (HAM METNİ KORURUZ!)
# ------------------------------------------------------------
OCR_COMMON_FIXES = [
    (r"İ̇", "İ"),              # çift noktalı i artığı
    (r"\u00ad", ""),           # soft hyphen
    (r"[ \t]+\n", "\n"),     # satır sonu öncesi fazla boşluk
    (r"\n{3,}", "\n\n"),     # fazla boş satır
]

WHITESPACE_RE = re.compile(r"[ \t]+")


def normalize_text(raw: str) -> str:
    txt = raw
    for pat, rep in OCR_COMMON_FIXES:
        txt = re.sub(pat, rep, txt)
    txt = WHITESPACE_RE.sub(" ", txt)
    return txt.strip()


# Türkçe para -> (amount_minor:int, currency:str)
MONEY_RE = re.compile(
    r"(?P<amount>(?:\d{1,3}(?:\.\d{3})*|\d+)(?:,\d{1,2})?)\s*(?P<cur>TL|TRY|Türk Liras[ıi]|TL\.)",
    re.IGNORECASE,
)

PERCENT_RE = re.compile(r"%(?:\s*)?(?P<pct>\d{1,3}(?:[.,]\d{1,2})?)")

DATE_TOKEN_RE = re.compile(
    r"(?P<date>(?:\d{1,2}[./-]\d{1,2}[./-]\d{2,4})|(?:\d{1,2}\s+(?:ocak|şubat|mart|nisan|mayıs|haziran|temmuz|ağustos|eylül|ekim|kasım|aralık)\s+\d{4}))",
    re.IGNORECASE,
)

INT_RE = re.compile(r"\d+")


def tr_amount_to_minor(s: str) -> Optional[int]:
    if not s:
        return None
    s = s.strip().replace(".", "").replace(",", ".")
    try:
        return int(round(float(s) * 100))
    except Exception:
        return None


def norm_percent(s: str) -> Optional[float]:
    s = s.replace(",", ".")
    try:
        return float(s)
    except Exception:
        return None


def extract_money_spans(text: str) -> List[Dict[str, Any]]:
    out = []
    for m in MONEY_RE.finditer(text):
        amount_s = m.group("amount")
        cur = m.group("cur")
        amt_minor = tr_amount_to_minor(amount_s)
        out.append(
            {
                "value": f"{amount_s} {cur}",
                "text": m.group(0),
                "span": [m.start(), m.end()],
                "method": "regex",
                "pattern_id": "money.generic",
                "confidence": 0.9,
                "extras": {
                    "amount_minor": amt_minor,
                    "currency": cur.upper().replace("TÜRK LİRASI", "TRY").replace("TL.", "TL"),
                },
            }
        )
    return out


def extract_percent_spans(text: str) -> List[Dict[str, Any]]:
    out = []
    for m in PERCENT_RE.finditer(text):
        p = norm_percent(m.group("pct"))
        out.append(
            {
                "value": p,
                "text": m.group(0),
                "span": [m.start(), m.end()],
                "method": "regex",
                "pattern_id": "percent.generic",
                "confidence": 0.9,
            }
        )
    return out


def extract_dates(text: str) -> List[Dict[str, Any]]:
    out = []
    for m in DATE_TOKEN_RE.finditer(text):
        raw = m.group("date")
        dt = dateparser.parse(raw, languages=["tr"])  # mümkünse normalize et
        norm = dt.date().isoformat() if dt else None
        out.append(
            {
                "value": norm or raw,
                "text": m.group(0),
                "span": [m.start(), m.end()],
                "method": "regex",
                "pattern_id": "date.generic",
                "confidence": 0.8 if norm else 0.4,
            }
        )
    return out


# ------------------------------------------------------------
# Başlık/alan sözlükleri ve regex desenleri
# ------------------------------------------------------------
HEADER_SYNONYMS = {
    "company": [
        "ünvan",
        "unvan",
        "şirket ünvanı",
        "ticaret unvanı",
        "ticaret ünvanı",
        "şirket adı",
        "firma adı",
    ],
    "address": ["adres", "merkez adresi", "iş adresi", "şube adresi"],
    "mersis": ["mersis", "mersİs", "mersıs", "mercis", "mersis no", "mersis numarası"],
    "tax_id": ["vergi no", "vkn", "vergi kimlik no", "vergi kimlik numarası"],
    "registry_no": ["ticaret sicil no", "sicil no", "ticaret sicil numarası"],
    "capital": ["sermaye", "ödenmiş sermaye", "çıkarılmış sermaye"],
    "partners": [
        "ortaklar",
        "hisse devri",
        "pay devir",
        "pay devri",
        "pay oranı",
        "pay dağılımı",
    ],
    "board": [
        "yönetim kurulu",
        "müdür",
        "temsil ve ilzam",
        "temsil yetkisi",
        "müdürler kurulu",
    ],
    "event": [
        "tescil",
        "kuruluş",
        "tasfiye",
        "iflas",
        "konkordato",
        "birleşme",
        "devralma",
        "bölünme",
        "unvan değişikliği",
        "adres değişikliği",
        "merkez nakli",
        "sermaye artırımı",
        "sermaye azaltımı",
        "ana sözleşme tadili",
        "şube açılışı",
        "şube kapanışı",
    ],
    "court": ["mahkeme", "asliye ticaret", "icra", "karar no", "esas no", "karar"],
    "gazette": ["sicil gazetesi", "ticaret sicil gazetesi", "gazete no", "gazete tarihi"],
    "chamber": ["ticaret odası", "ticaret sicil müdürlüğü", "sicil müdürlüğü", "oda"],
}

RE_MERSIS = re.compile(r"\b0\d{15}\b")  # 16 haneli ve 0 ile başlar
RE_VKN = re.compile(r"\b\d{10}\b")
RE_TCKN = re.compile(r"\b\d{11}\b")
RE_REGISTRY_NO = re.compile(r"(?:ticaret\s+)?sicil\s*(?:no|numarası)[:\s]*([0-9/ -]+)", re.IGNORECASE)
RE_COMPANY_AFTER_LABEL = re.compile(
    r"(?:ünvan[ıi]|unvan[ıi]|şirket\s+ünvan[ıi]|ticaret\s+ünvan[ıi])[:\s]+(?P<name>.+?)(?:$|\n)",
    re.IGNORECASE,
)
RE_ADDRESS_AFTER_LABEL = re.compile(r"(?:adres|merkez\s+adresi)[:\s]+(?P<addr>.+?)(?:$|\n)", re.IGNORECASE)
RE_CAPITAL = re.compile(
    r"(?:sermaye|ödenmiş\s+sermaye|çıkarılmış\s+sermaye)[:\s]+(?P<cap>.+?)(?:$|\n)",
    re.IGNORECASE,
)

RE_PARTNER_LINE = re.compile(r"(?P<name>(?:[A-ZÇĞİÖŞÜ][A-ZÇĞİÖŞÜ' .-]{1,100}))(?::|\s|-|,)+(?P<rest>.+)", re.IGNORECASE)
RE_BOARD_LINE = re.compile(
    r"(?:yönetim\s+kurulu|müdür(?:ler)?|temsil\s+ve\s+ilzam|temsil\s+yetkisi)[:\s]+(?P<rest>.+)",
    re.IGNORECASE,
)


# ------------------------------------------------------------
# Fuzzy satır bazlı başlık bulucu
# ------------------------------------------------------------

def fuzzy_find_header(line: str, kind: str, threshold: int = 86) -> bool:
    targets = HEADER_SYNONYMS.get(kind, [])
    if not targets:
        return False
    m = process.extractOne(line.lower(), targets, scorer=fuzz.WRatio)
    return bool(m and m[1] >= threshold)


# ------------------------------------------------------------
# Span yardımcıları
# ------------------------------------------------------------

def find_all_spans(text: str, substring: str) -> List[Tuple[int, int]]:
    spans = []
    start = 0
    while True:
        i = text.find(substring, start)
        if i == -1:
            break
        spans.append((i, i + len(substring)))
        start = i + 1
    return spans


# ------------------------------------------------------------
# Ana ayrıştırıcı
# ------------------------------------------------------------

@dataclass
class ParseResult:
    raw_text: str
    clean_text: str
    meta: Dict[str, Any] = field(default_factory=dict)
    entities: Dict[str, List[Dict[str, Any]]] = field(default_factory=lambda: {})
    sections: List[Dict[str, Any]] = field(default_factory=list)
    unparsed_fragments: List[str] = field(default_factory=list)
    coverage: Dict[str, Any] = field(default_factory=dict)

    def add_entity(self, etype: str, item: Dict[str, Any]):
        self.entities.setdefault(etype, []).append(item)


def parse_document(raw_text: str, meta: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    clean = normalize_text(raw_text)
    res = ParseResult(raw_text=raw_text, clean_text=clean, meta=meta or {})

    # 1) Parçacıkların temel çıkarımı (para, yüzde, tarih)
    for itm in extract_money_spans(raw_text):
        res.add_entity("money", itm)
    for itm in extract_percent_spans(raw_text):
        res.add_entity("percent", itm)
    for itm in extract_dates(raw_text):
        res.add_entity("date", itm)

    # 2) Etiketli alanlar – doğrudan regex
    m = RE_COMPANY_AFTER_LABEL.search(clean)
    if m:
        name = m.group("name").strip(" .:-")
        span = find_all_spans(raw_text, m.group("name"))[:1] or [[0, 0]]
        res.add_entity(
            "company",
            {
                "value": name,
                "text": m.group(0),
                "span": span[0],
                "method": "regex",
                "pattern_id": "company.after_label",
                "confidence": 0.95,
            },
        )

    m = RE_ADDRESS_AFTER_LABEL.search(clean)
    if m:
        addr = m.group("addr").strip(" .-")
        span = find_all_spans(raw_text, m.group("addr"))[:1] or [[0, 0]]
        res.add_entity(
            "address",
            {
                "value": addr,
                "text": m.group(0),
                "span": span[0],
                "method": "regex",
                "pattern_id": "address.after_label",
                "confidence": 0.9,
            },
        )

    # Sermaye: hem etiketli hem parasal yakalama
    m = RE_CAPITAL.search(clean)
    if m:
        cap_line = m.group("cap").strip()
        money_in = extract_money_spans(cap_line)
        cap_minor = None
        if money_in:
            cap_minor = money_in[0]["extras"].get("amount_minor")
        res.add_entity(
            "capital",
            {
                "value": cap_line,
                "text": m.group(0),
                "span": [raw_text.find(cap_line), raw_text.find(cap_line) + len(cap_line)],
                "method": "regex",
                "pattern_id": "capital.after_label",
                "confidence": 0.9,
                "extras": {"amount_minor": cap_minor, "currency": "TRY" if cap_minor else None},
            },
        )

    # Ticaret sicil no (etiketli)
    m = RE_REGISTRY_NO.search(clean)
    if m:
        val = m.group(1).strip()
        res.add_entity(
            "registry_no",
            {
                "value": val,
                "text": m.group(0),
                "span": [raw_text.find(m.group(0)), raw_text.find(m.group(0)) + len(m.group(0))],
                "method": "regex",
                "pattern_id": "registry.no",
                "confidence": 0.9,
            },
        )

    # MERSİS – çıplak 16 hane
    for mm in RE_MERSIS.finditer(clean):
        seg = mm.group(0)
        res.add_entity(
            "mersis",
            {
                "value": seg,
                "text": seg,
                "span": [mm.start(), mm.end()],
                "method": "regex",
                "pattern_id": "mersis.16digits",
                "confidence": 0.95,
            },
        )

    # VKN – 10 hane (etiketle teyit etmeye çalış)
    for mm in RE_VKN.finditer(clean):
        seg = mm.group(0)
        left = max(0, mm.start() - 25)
        right = min(len(clean), mm.end() + 25)
        window = clean[left:right].lower()
        has_label = any(k in window for k in ["vergi", "vkn", "kimlik"])
        res.add_entity(
            "tax_id",
            {
                "value": seg,
                "text": clean[mm.start() : mm.end()],
                "span": [mm.start(), mm.end()],
                "method": "regex" if has_label else "heuristic",
                "pattern_id": "vkn.10digits",
                "confidence": 0.92 if has_label else 0.6,
            },
        )

    # TCKN adayları
    for mm in RE_TCKN.finditer(clean):
        seg = mm.group(0)
        left = max(0, mm.start() - 20)
        right = min(len(clean), mm.end() + 20)
        window = clean[left:right].lower()
        has_label = any(k in window for k in ["t.c.", "tc", "kimlik"])
        res.add_entity(
            "id_number",
            {
                "value": seg,
                "text": clean[mm.start() : mm.end()],
                "span": [mm.start(), mm.end()],
                "method": "regex" if has_label else "heuristic",
                "pattern_id": "tckn.11digits",
                "confidence": 0.9 if has_label else 0.5,
            },
        )

    # 3) Satır bazlı tarama – fuzzy başlıklarla bölümlendirme ve özel kalıplar
    lines = clean.split("\n")
    line_spans: List[Tuple[int, int]] = []
    cursor = 0
    for ln in lines:
        line_spans.append((cursor, cursor + len(ln)))
        cursor += len(ln) + 1  # '\n'

    def add_section(title: str, start_idx: int, end_idx: int):
        res.sections.append({"title": title, "span": [start_idx, end_idx], "text": clean[start_idx:end_idx]})

    for i, ln in enumerate(lines):
        for kind in HEADER_SYNONYMS.keys():
            if fuzzy_find_header(ln, kind):
                start = line_spans[i][0]
                j = i + 1
                while j < len(lines) and not any(
                    fuzzy_find_header(lines[j], k) for k in HEADER_SYNONYMS.keys()
                ):
                    j += 1
                end = line_spans[j - 1][1] if j > i + 1 else line_spans[i][1]
                add_section(kind, start, end)

                section_text = clean[start:end]
                if kind in ("partners",):
                    for pm in RE_PARTNER_LINE.finditer(section_text):
                        name = pm.group("name").strip(" :-,")
                        rest = pm.group("rest")
                        pct = None
                        pct_m = PERCENT_RE.search(rest)
                        if pct_m:
                            pct = norm_percent(pct_m.group("pct"))
                        money = extract_money_spans(rest)
                        id_nums = []
                        for cand in INT_RE.findall(rest):
                            if len(cand) in (10, 11, 16):
                                id_nums.append(cand)
                        res.add_entity(
                            "partner",
                            {
                                "value": name,
                                "text": pm.group(0),
                                "span": [start + pm.start(), start + pm.end()],
                                "method": "regex",
                                "pattern_id": "partner.line",
                                "confidence": 0.85,
                                "extras": {
                                    "share_pct": pct,
                                    "nominal_minor": money[0]["extras"]["amount_minor"] if money else None,
                                    "id_numbers": id_nums or None,
                                },
                            },
                        )

                if kind in ("board",):
                    for bm in RE_BOARD_LINE.finditer(section_text):
                        res.add_entity(
                            "board",
                            {
                                "value": bm.group("rest").strip(),
                                "text": bm.group(0),
                                "span": [start + bm.start(), start + bm.end()],
                                "method": "regex",
                                "pattern_id": "board.line",
                                "confidence": 0.85,
                            },
                        )

                if kind in ("event",):
                    ev_hits = []
                    low = section_text.lower()
                    for ev in HEADER_SYNONYMS["event"]:
                        if ev in low:
                            ev_hits.append(ev)
                    if ev_hits:
                        res.add_entity(
                            "event",
                            {
                                "value": list(sorted(set(ev_hits))),
                                "text": section_text,
                                "span": [start, end],
                                "method": "keyword",
                                "pattern_id": "event.keywords",
                                "confidence": 0.8,
                            },
                        )

    # 4) Telefon/IBAN gibi ek sinyaller
    for match in re.finditer(r"[A-Z]{2}\d{2}[A-Z0-9]{11,30}", clean):
        res.add_entity(
            "iban",
            {
                "value": match.group(0),
                "text": match.group(0),
                "span": [match.start(), match.end()],
                "method": "regex",
                "pattern_id": "iban.generic",
                "confidence": 0.8,
            },
        )

    for m in re.finditer(r"(?:\+?90|0)\s?\d{3}\s?\d{3}\s?\d{2}\s?\d{2}", clean):
        try:
            pn = phonenumbers.parse(m.group(0), "TR")
            if phonenumbers.is_valid_number(pn):
                res.add_entity(
                    "phone",
                    {
                        "value": phonenumbers.format_number(pn, phonenumbers.PhoneNumberFormat.E164),
                        "text": m.group(0),
                        "span": [m.start(), m.end()],
                        "method": "regex",
                        "pattern_id": "phone.tr",
                        "confidence": 0.9,
                    },
                )
        except phonenumbers.NumberParseException:
            pass

    # 5) Basit kapsama/rapor ve unparsed
    captured_ranges = [sec["span"] for sec in res.sections]
    lines_clean = clean.split("\n")
    cursor = 0
    for ln in lines_clean:
        span = (cursor, cursor + len(ln))
        inside = any(span[0] >= s[0] and span[1] <= s[1] for s in captured_ranges)
        if (not inside) and ln.strip():
            res.unparsed_fragments.append(ln.strip())
        cursor += len(ln) + 1

    res.coverage = {
        "money_count": len(res.entities.get("money", [])),
        "percent_count": len(res.entities.get("percent", [])),
        "date_count": len(res.entities.get("date", [])),
        "mersis_count": len(res.entities.get("mersis", [])),
        "tax_id_count": len(res.entities.get("tax_id", [])),
        "registry_no_count": len(res.entities.get("registry_no", [])),
        "section_count": len(res.sections),
        "unparsed_line_count": len(res.unparsed_fragments),
    }

    return asdict(res)


# ------------------------------------------------------------
# Toplu çalıştırma (metin listesi -> NDJSON)
# ------------------------------------------------------------

def parse_corpus(texts: List[Tuple[str, str]], out_path: str):
    with open(out_path, "w", encoding="utf-8") as f:
        for doc_id, raw in texts:
            rec = parse_document(raw, meta={"doc_id": doc_id})
            f.write(dump_json(rec) + "\n")
