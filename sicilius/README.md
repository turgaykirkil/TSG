<div align="center">

# 🏢 SICILIUS PLATFORM
### Next-Gen B2B Intelligence & Autonomous Trade Registry Pipeline

<p align="center">
  <strong>FastAPI, Next.js 14, PostGIS, Llama 3.2 AI, and React Native Powered End-to-End RegTech Ecosystem.</strong>
</p>

[![Production](https://img.shields.io/badge/Production-Active-success.svg)](https://sicilius.com.tr)
[![Architecture](https://img.shields.io/badge/Clean%20Architecture-Enabled-blue.svg)](#-mimari-ve-veri-akisi)
[![AI Model](https://img.shields.io/badge/AI%20NLP-Llama%203.2%20(Ollama%20JSON%20Mode)-purple.svg)](#-yapay-zeka-ve-otonom-ocr-hatti)
[![Spatial](https://img.shields.io/badge/Spatial-PostGIS%20Spatial%20Indexing-orange.svg)](#-postgis-cografi-istihbarat)

</div>

---

## 📑 İçindekiler
- [🎯 Proje Özeti](#-proje-özeti)
- [🏗️ Mimari ve Veri Akışı](#-mimari-ve-veri-akisi)
- [🧠 Yapay Zeka ve Otonom OCR Hattı](#-yapay-zeka-ve-otonom-ocr-hatti)
- [🕸️ NEXUS Graph & Risk Motoru](#-nexus-graph--risk-motoru)
- [🗺️ PostGIS Coğrafi İstihbarat](#-postgis-cografi-istihbarat)
- [📱 Saha Satış Mobil Mimarisi](#-saha-satis-mobil-mimarisi)
- [📊 İş Zekası & Yönetici Raporları](#-is-zekasi--yonetici-raporlari)
- [🚀 Kurulum ve Dağıtım](#-kurulum-ve-dagitim)

---

## 🎯 Proje Özeti

**Sicilius**, Türkiye Ticaret Sicil Gazetesi'nde yayımlanan resmi şirket ilanlarını (yeni kuruluş, sermaye artırımı, hisse devri, yetkili değişiklikleri, tasfiye ve konkordato) otonom tarayarak yapılandıran, şirketler ve ortaklar arasındaki dolaylı bağları 3D graf motoruyla haritalandıran ve saha satış ekiplerine gerçek zamanlı coğrafi lead üreten yeni nesil bir **B2B Ticari İstihbarat Platformudur**.

---

## 🏗️ Mimari ve Veri Akışı

```
[ TSG Web Portalı ]
       │
       ▼ (Headless Playwright Crawler)
[ Raw Gazette PDFs ]
       │
       ▼ (Tesseract / VisionKit Multi-Column Splitter)
[ OCR Text Chunks ]
       │
       ▼ (Ollama Llama 3.2:3b - Deterministic JSON Schema Mode)
[ Structured Company & Person JSON ]
       │
       ├──► [ PostgreSQL 15 (app schema) ] ──► [ PostGIS Spatial Radar ]
       ├──► [ MinIO S3 Bucket ]            ──► [ Original Document Storage ]
       └──► [ NEXUS 3D Graph Model ]       ──► [ Risk Contagion & Flow Analysis ]
```

---

## 🧠 Yapay Zeka ve Otonom OCR Hattı

### 1. Vision & Sayfa Parçalama (Chunking)
- Çok sütunlu ve karmaşık dizgili resmi gazete sayfaları satır/sütun koordinatlarına göre taranır.
- Her ilan tekil bir `OcrResult` kaydı olarak izole edilir.

### 2. Ollama Native Structured Output (Llama 3.2:3b)
- `temperature = 0.0` ve sabit `seed = 42` ile deterministik bilgi çıkarımı.
- Çıkarılan Veri Şeması:
  ```json
  {
    "trade_name": "ÖRNEK TEKNOLOJİ ANONİM ŞİRKETİ",
    "sicil_no": "105432-5",
    "mersis_no": "012345678900001",
    "capital": 5000000.0,
    "old_capital": 1000000.0,
    "announcement_type": "SERMAYE ARTIRIMI",
    "persons": [
      {
        "name": "AHMET YILMAZ",
        "role": "YÖNETİM KURULU BAŞKANI",
        "masked_id": "123******89"
      }
    ]
  }
  ```

---

## 🕸️ NEXUS Graph & Risk Motoru

*   **Derinlik 2/3 Ağ Taraması:** Bir şirketin ortakları, o ortakların diğer şirketlerdeki hisseleri ve yönetim kurulu bağlantıları tek bir grafikte birleştirilir.
*   **Contagion (Risk Sıçraması) Modeli:** Finansal sıkıntıya giren veya tasfiye sürecindeki bir şirketin, ortaklık zinciri üzerinden risk puanı hesaplanarak ilişkili firmalar uyarılır.
*   **Sankey Sermaye Grafiği:** Şirketler arası sermaye akışları ve para transfer hacimleri görselleştirilir.

---

## 🗺️ PostGIS Coğrafi İstihbarat

*   Tüm şirket adresleri geocoding motorundan geçirilerek `POINT(4326)` formatında haritaya işlenir.
*   `ST_DWithin` sorguları ile mobil veya web üzerinden satış temsilcisine anlık mesafe bazlı müşteri radarı sunulur:
    ```sql
    SELECT id, unvan, ST_Distance(koordinat, ST_MakePoint($lon, $lat)::geography) as distance
    FROM app.companies
    WHERE ST_DWithin(koordinat, ST_MakePoint($lon, $lat)::geography, 1000)
    ORDER BY distance ASC;
    ```

---

## 📱 Saha Satış Mobil Mimarisi (React Native / Expo)

*   **OpenStreetMap Entegrasyonu:** Sıfır Google Maps API maliyeti ile sınırsız harita katmanı.
*   **Pil Dostu Konum:** Mesafe filtreli (`distanceFilter: 50m`) akıllı GPS takibi.
*   **Oyunlaştırma & Görevler:** Ziyaret doğrulama, XP puanlama ve anonim satış ligi liderlik tablosu.

---

## 📊 İş Zekası & Yönetici Raporları

*   Günlük/Aylık sermaye artış hacimleri, kuruluş vs. kapanış istatistikleri.
*   İl bazında şirket yoğunlukları ve sektörel dağılım analizleri.
*   Tek tıkla **CSV / Excel** ve **Yönetici PDF Özeti** indirme.

---

## 🚀 Kurulum ve Dağıtım

```bash
# 1. Depoyu klonlayın
git clone https://github.com/turgaykirkil/TSG_Platform.git
cd TSG_Platform/sicilius

# 2. Servisleri Docker ile başlatın
docker-compose up -d --build

# 3. Veritabanı migrasyonlarını uygulayın
docker-compose exec backend alembic upgrade head
```

<div align="center">
  <sub>Sicilius — Engineered with Precision for B2B Excellence.</sub>
</div>
