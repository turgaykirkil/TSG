import re
import unicodedata

SAMPLES = [
    "ŞİRİNEVLER MH.FETİH 4.SK.DENİZ BL.NO:11A / BAHÇELİEVLER",
    "BOSTANLI MAH. 2016/2 SK. DAMLA NO: 11 İÇ KAPI NO: 7 KARŞIYAKA / İZMİR",
    "ESENTEPE MAH. BÜYÜKDERE CAD. LOFT RESIDANCE NO:201/116 / ŞİŞLİ",
    "GÜZELCE MAH. D-100 KARAYOLU CAD. NO: 977 İÇ KAPI NO: 1 / BÜYÜKÇEKMECE",
    "MALTEPE MAH.GÜMÜŞSUYU CAD. MİTHATPAŞA ST.N.2 İÇ KAPI N.10 / ZEYTİNBURNU",
    "İOSB MH.AYKOSAN 4 L B BL.SK. AYKOSAN SİT.4'LÜ B BL.N.1B/51 / BAŞAKŞEHİR",
    "NİSBETİYE MAH. GAZİ GÜÇNAR SK. UYGUR IŞ MERKEZI NO:4/2 / BEŞİKTAŞ",
]

def normalize_for_geocoding(address: str) -> str:
    s = address or ""
    s = unicodedata.normalize("NFC", s)
    s = re.sub(r"\s+", " ", s).strip()
    s = s.replace("ISTANBUL", "İstanbul").replace("İSTANBUL", "İstanbul").replace("istanbul", "İstanbul")
    s = s.replace("IZMIR", "İzmir").replace("İZMİR", "İzmir").replace("izmir", "İzmir")
    s = re.sub(r"\b(MH|MH\.|MAH|MAH\.)\b", "Mahallesi", s, flags=re.IGNORECASE)
    s = re.sub(r"\b(CD|CD\.|CAD|CAD\.|CADD?E?)\b", "Cadde", s, flags=re.IGNORECASE)
    s = re.sub(r"\b(SOK|SOK\.|SK|SK\.)\b", "Sokak", s, flags=re.IGNORECASE)
    s = re.sub(r"\b(BUL|BUL\.|BLV|BLV\.|BLVR?)\b", "Bulvarı", s, flags=re.IGNORECASE)
    s = re.sub(r"\bNO\s*[:\.]?\s*", "No ", s, flags=re.IGNORECASE)
    s = re.sub(r"\bİÇ\s*KAPI\s*NO\s*[:\.]?\s*", "İç Kapı No ", s, flags=re.IGNORECASE)
    s = re.sub(r"\bN[O\.]?\s*[:\.]?\s*(\d+)", r"No \1", s, flags=re.IGNORECASE)
    s = re.sub(r"\bST\b\.?", "Sokak", s, flags=re.IGNORECASE)
    s = re.sub(r"\bBLK?\b\.?", "Blok", s, flags=re.IGNORECASE)
    s = re.sub(r"\b(Mahallesi|Cadde|Sokak|Bulvarı)\.", r"\1", s, flags=re.IGNORECASE)
    s = re.sub(r"\s*\.\s*", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def main() -> None:
    for s in SAMPLES:
        n = normalize_for_geocoding(s)
        print("- Orijinal:", s)
        print("  Normal:", n)
        print()

if __name__ == "__main__":
    main()
