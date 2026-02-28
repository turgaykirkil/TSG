from __future__ import annotations

import re
import unicodedata
from typing import Iterable, List, Set, Optional


def tr_normalize_py(s: Optional[str]) -> str:
    """
    Türkçe aksan ve noktalı I/ı duyarsız normalize edici.
    - 'İ' -> 'I', 'ı' -> 'i'
    - Unicode accent kaldırma
    - lower()
    - trim
    """
    if not s:
        return ""
    s = s.replace("İ", "I").replace("ı", "i")
    s = unicodedata.normalize("NFKD", s)
    s = s.encode("ascii", "ignore").decode("ascii")
    return s.lower().strip()


def tr_letters_digits(s: Optional[str]) -> str:
    """Normalize et ve harf/rakam dışını çıkar."""
    if not s:
        return ""
    return re.sub(r"[^a-z0-9]+", "", tr_normalize_py(s))


def tokenize_for_search(text: Optional[str], *, min_len: int = 2, max_tokens: int = 20) -> List[str]:
    """
    Basit arama token'ları üretir:
    - Türkçe normalize (unaccent + lower + I/ı düzeltmesi)
    - Harf/rakam + boşluk dışını temizler
    - Boşluklardan bölüp min_len filtresi uygular
    - Yinelenen token'ları kaldırır (orijinal sırayı korumaya çalışır)
    """
    if not text:
        return []
    norm = tr_normalize_py(text)
    # boşluk dışındaki karakterleri sadeleştir
    norm = re.sub(r"[^a-z0-9\s]+", " ", norm)
    parts = [p for p in re.split(r"\s+", norm) if len(p) >= min_len]
    seen: Set[str] = set()
    out: List[str] = []
    for p in parts:
        if p not in seen:
            seen.add(p)
            out.append(p)
        if len(out) >= max_tokens:
            break
    return out
