import importlib.util
import textwrap
from pathlib import Path

# nlp_service modülünü dosyadan yükle
svc_path = Path(__file__).resolve().parents[1] / "app" / "services" / "nlp_service.py"
spec = importlib.util.spec_from_file_location("nlp_service", str(svc_path))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def test_extract_address_block_segment_basic():
    sample = textwrap.dedent(
        """
        T.C. İSTANBUL TİCARET SİCİLİ MÜDÜRLÜĞÜ
        İLAN SIRA NO: 2024/12345
        Unvan: ABC TEKNOLOJİ A.Ş.
        Adres: RASİMPAŞA MAH. YOĞURTÇU PARKI CAD. NO: 12/3 KAT: 4 D:8
        34716 KADIKÖY / İSTANBUL
        Telefon: 0 216 000 00 00
        Yukarıdaki Bilgiler gereğince tescil ve ilan olunur.
        """
    )
    out = mod.extract_address_block_segment(sample)
    assert out is not None
    # Çok satırlı blok korunmalı
    assert "YOĞURTÇU PARKI CAD." in out
    assert "KADIKÖY / İSTANBUL" in out


def test_extract_address_block_segment_with_stop_fallback():
    sample = textwrap.dedent(
        """
        UNVAN: XYZ GIDA LTD. ŞTİ.
        Adres: İSTİKLAL MAH. DEMOKRASİ CAD. NO:5 KAT:2 D:4
        SANCAKTEPE / İSTANBUL
        Tel: 0 216 111 22 33
        Madde 1- Şirket hakkında...
        """
    )
    out = mod.extract_address_block_segment(sample)
    assert out is not None
    assert "İSTİKLAL MAH. DEMOKRASİ CAD." in out
    assert "SANCAKTEPE / İSTANBUL" in out


def test_parse_announcement_text_addresses_prefers_block():
    sample = textwrap.dedent(
        """
        İLAN SIRA NO: 2024/55
        Unvan: QWE BİLİŞİM SAN. ve TİC. LTD. ŞTİ.
        Adres: ATATÜRK MAH. İNÖNÜ CAD. NO:10/A
        34760 ÜMRANİYE / İSTANBUL
        Telefon: 0 212 123 45 67
        Yukarıdaki Bilgiler gereğince tescil ve ilan olunur.
        """
    )
    parsed = mod.parse_announcement_text(sample)
    addrs = parsed.get("addresses") or []
    assert isinstance(addrs, list) and len(addrs) >= 1
    # İlk eleman çok satırlı blok olmalı
    assert "ATATÜRK MAH." in addrs[0]
    assert "ÜMRANİYE / İSTANBUL" in addrs[0]
