<div align="center">

# ⚡ SICILIUS — TSG PLATFORM
### Autonomous Commercial Intelligence, Knowledge Graph & B2B Lead Generation Engine

<p align="center">
  <strong>Türkiye Ticaret Sicil Gazetesi verilerini otonom tarayan, yerel LLM (Llama 3.2) ile yapılandıran, 3D ilişki ağlarını haritalandıran ve PostGIS ile saha satışına dönüştüren yeni nesil RegTech ve Ticari İstihbarat Ekosistemi.</strong>
</p>

[![Next.js 14](https://img.shields.io/badge/Frontend-Next.js%2014%20(App%20Router)-black?style=for-the-badge&logo=next.js)](https://nextjs.org)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Llama 3.2](https://img.shields.io/badge/AI%20Engine-Llama%203.2%20(Ollama)-0466c8?style=for-the-badge&logo=meta&logoColor=white)](https://ollama.com)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL%2015%20%2B%20PostGIS-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![React Native](https://img.shields.io/badge/Mobile-Expo%20%2F%20React%20Native-61dafb?style=for-the-badge&logo=react&logoColor=black)](https://expo.dev)
[![Swift](https://img.shields.io/badge/Vision%20OCR-Apple%20Swift%20%2F%20VisionKit-FA7343?style=for-the-badge&logo=swift&logoColor=white)](https://developer.apple.com/swift/)
[![Docker](https://img.shields.io/badge/DevOps-Docker%20%26%20Caddy%202-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

---

[🚀 Canlı Platform (sicilius.com.tr)](https://sicilius.com.tr) • [🕸️ NEXUS Graph Motoru](https://sicilius.com.tr/nexus) • [📊 Yönetici Raporları](https://sicilius.com.tr/admin/reports) • [📑 İnteraktif Pitch Deck](https://sicilius.com.tr/presentation)

</div>

---

## 💡 Proje Vizyonu ve Ne Çözüyor?

Türkiye Ticaret Sicili, her gün binlerce şirketin **kuruluş, sermaye artırımı, adres nakli, birleşme ve yönetim kurulu/yetkili değişikliklerini** dağınık, taranmış ve çok sütunlu PDF formatında yayımlar.

Geleneksel yöntemlerle bu verileri takip etmek imkansızdır. **Sicilius**, Türkiye'deki tüm ticari sicil hareketlerini saniyeler içinde yakalayan, çok katmanlı yapay zeka hattından geçiren ve B2B şirketlere, bankalara, faktoring kuruluşlarına ve saha satış ekiplerine **doğrudan aksiyon alınabilir sıcak lead ve risk istihbaratı** sağlayan tam teşekküllü bir platformdur.

---

## 🏗️ Uçtan Uca Sistem Mimarisi

```
 ┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
 │                                       DATA INGESTION STAGE                                       │
 └──────────────────────────────────────────────────────────────────────────────────────────────────┘
            │
            ▼
 ┌────────────────────────┐      ┌────────────────────────┐      ┌──────────────────────────────────┐
 │  Playwright Headless   │ ───► │  Guardian Vision OCR   │ ───► │   Ollama Llama 3.2 (3B Native)   │
 │ Autonomous Web Crawler │      │ Multi-Column PDF Split │      │  Deterministic Structured Output │
 └────────────────────────┘      └────────────────────────┘      └──────────────────────────────────┘
                                                                                   │
                                                                                   ▼
 ┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
 │                                   STORAGE & GRAPH KNOWLEDGE HUB                                  │
 └──────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                   │
                   ┌───────────────────────────────┴───────────────────────────────┐
                   ▼                                                               ▼
 ┌──────────────────────────────────┐                            ┌──────────────────────────────────┐
 │  PostgreSQL 15 + PostGIS Engine  │                            │  NEXUS 3D Knowledge Graph Model  │
 │  Spatial Radar & Company Index   │                            │  UBO & Risk Contagion Engine     │
 └──────────────────────────────────┘                            └──────────────────────────────────┘
                   │                                                               │
                   └───────────────────────────────┬───────────────────────────────┘
                                                   ▼
 ┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
 │                                  DELIVERY & INTERFACE CHANNELS                                   │
 └──────────────────────────────────────────────────────────────────────────────────────────────────┘
                   │                                                               │
                   ▼                                                               ▼
 ┌──────────────────────────────────┐                            ┌──────────────────────────────────┐
 │  Next.js 14 Glassmorphic UI      │                            │  React Native / Expo Field App   │
 │  Real-time Ops, Maps & BI Reps   │                            │  100% Free OSM Radar & Quests    │
 └──────────────────────────────────┘                            └──────────────────────────────────┘
```

---

## 🌟 Öne Çıkan Süper Güçler

### 1. 🤖 Otonom Web Scraper Motoru (Playwright Stealth)
*   **Akıllı Boşluk Doldurma (Gap-Fill):** 81 ilin ticaret sicil müdürlüğünü tarar, atlanmış sicil numaralarını tespit eder ve aralıksız veri çeker.
*   **Anti-Bot & Stealth Orkestrasyonu:** Cloudflare/WAF korumalarını aşan insan simülasyonlu akıllı oturum yönetimi.
*   **Canlı Durum ve Kalan Göstergesi:** Web konsolu üzerinden anlık işlenen, kalan ve hedef sayaçları.

### 2. 👁️ Guardian Vision OCR & Akıllı Parçalayıcı (Chunker)
*   Tek bir gazete sayfasındaki 3-10 farklı şirket ilanını sütun sınırlarından ve başlık tipografisinden algılayarak bağımsız bloklara böler.
*   Tesseract OCR ve Apple Silicon Neural Engine (Swift VisionKit) ile milisaniyeler seviyesinde metin ayrıştırma.

### 3. 🧠 Yerel LLM Yapılandırılmış Çıktı Motoru (Llama 3.2 / Ollama)
*   **Sıfır Halüsinasyon (Temperature: 0.0):** Prompt içi zorlama yerine Ollama'nın native JSON Schema motorunu (`Pydantic model_json_schema`) kullanır.
*   Ham OCR metninden **Şirket Unvanı, MERSİS No, Vergi Kimlik No, Eski/Yeni Sermaye Tutarları, Yönetim Kurulu Üyeleri ve Temsil Yetkileri** %100 tip güvenli JSON olarak çıkarılır.

### 4. 🕸️ NEXUS 3D İlişki Ağı ve Risk Yayılım Motoru (Contagion Engine)
*   **2. ve 3. Derece Bağlantı Analizi:** Şirketler, ortaklar ve yöneticiler arasındaki dolaylı sahiplik ve holding ağlarını 3D Force-Directed Graph ile canlandırır.
*   **Risk Contagion Simülasyonu:** Bir şirketteki finansal iflas, konkordato veya icra riskinin ortaklık zinciri üzerinden hangi bağlı şirketlere sıçrayacağını matematiksel olarak modeller.
*   **Sankey Sermaye Akışı:** Şirketler arası sermaye transferlerini ve para hareketlerini görselleştirir.

### 5. 📍 Coğrafi Konum Analitiği ve PostGIS Saha Satış Radarı
*   Türkiye genelindeki şirket adreslerini normalize ederek PostGIS uzamsal koordinatlarına (`POINT(4326)`) dönüştürür.
*   `ST_DWithin` ve uzamsal indeksler (`GIST`) ile saha satışçısına **"500 Metremdeki Sıcak Fırsatlar"** radarını anlık sunar.

### 6. 📱 Çapraz Platform Saha Satış Mobil Uygulaması (React Native / Expo)
*   **%100 Ücretsiz Harita Altyapısı:** Google Maps faturalandırma zorunluluğunu ortadan kaldıran OpenStreetMap Tile Server motoru.
*   **Oyunlaştırma (Gamification):** Satışçılara günlük rota görevleri, mesafe doğrulama (50m GPS geofence), XP ve anonim liderlik tablosu.
*   **Çevrimdışı Öncelikli (Offline-First):** İnternet çekmeyen binalarda ziyaret notlarını yerel SQLite/AsyncStorage kuyruğuna alır, bağlantı kurulunca arka planda senkronize eder.

### 7. 📊 Yönetici İş Zekası & Raporlama Paneli (Executive Analytics)
*   Piyasaya enjekte edilen sermaye hacmi, kurulan vs kapanan şirket oranları, il bazlı pazar payı pasta grafikleri.
*   Tek tıkla **Excel/CSV dışa aktarımı** ve C-Level PDF brifing oluşturucu.

---

## 🧰 Teknoloji Yığını (Tech Stack)

| Alan | Teknolojiler |
| :--- | :--- |
| **Frontend Web** | Next.js 14 (App Router), TypeScript, Tailwind CSS, Recharts, React Force Graph, Leaflet, Framer Motion |
| **Backend API** | Python 3.10+, FastAPI, SQLAlchemy, Alembic, Pydantic V2, Celery |
| **Yapay Zeka & OCR** | Ollama (Llama 3.2:3b Native JSON Mode), Tesseract OCR, Poppler, Swift VisionKit |
| **Veritabanı & Cache** | PostgreSQL 15, PostGIS Spatial Extension, pg_trgm, Redis, MinIO (S3 Object Storage) |
| **Mobil Uygulama** | React Native, Expo Router, TypeScript, Zustand, FlashList, OpenStreetMap Tile Engine |
| **DevOps & Proxy** | Docker Compose, Caddy 2 (Auto SSL/TLS Reverse Proxy), Linux / macOS Metal Acceleration |

---

## 📁 Monorepo Klasör Mimarisi

```text
TSG_Platform/
├── 📁 sicilius/
│   ├── 📁 backend/                # FastAPI REST & GraphQL API Gateway
│   │   ├── app/api/              # REST Endpointleri (Companies, Analytics, Scraper, NEXUS)
│   │   ├── app/models/           # SQLAlchemy DB Modelleri (PostGIS Spatial Schema)
│   │   ├── app/services/         # LLM Extraction & Ingestion Servisleri
│   │   └── app/scraping_browser.py # Playwright Otonom Kazıma Motoru
│   │
│   ├── 📁 frontend/               # Next.js 14 Glassmorphic Web Uygulaması
│   │   ├── src/app/(app)/        # App Router Sayfaları (Dashboard, Operations, Reports, Nexus)
│   │   ├── src/components/       # Yeniden Kullanılabilir UI Bileşenleri (Shadcn/UI)
│   │   └── public/presentation/  # İnteraktif Girişim ve Pitch Deck Modülü
│   │
│   ├── 📁 mobile/                 # React Native / Expo Saha Satış Mobil Uygulaması
│   │   ├── app/(tabs)/           # Harita, Radar, Müşteri CRM ve Görev Ekranları
│   │   ├── store/                # Zustand State Yönetimi
│   │   └── services/             # Offline-First Senkronizasyon Motoru
│   │
│   ├── 📁 ocr_app/                # Swift / Apple Silicon Neural Engine OCR Companion
│   ├── 📄 Caddyfile              # Otomatik SSL ve Yönlendirme Kuralları
│   └── 📄 docker-compose.yml     # Çoklu Konteyner Orkestrasyonu
│
├── 📄 start_local.sh             # Tek Tuşla Yerel Geliştirme Başlatıcı
├── 📄 deploy_old_mac.sh          # Sıfır Downtime Uzak Sunucu Dağıtım Betiği
└── 📄 README.md                  # Ana Dokümantasyon
```

---

## ⚡ Hızlı Başlangıç (Quick Start)

### Gereksinimler
*   Docker 20.10+ ve Docker Compose
*   Node.js 18+ ve Python 3.10+ (Yerel geliştirme için)
*   Ollama (`ollama run llama3.2:3b`)

### 1. Projeyi Klonlayın
```bash
git clone https://github.com/turgaykirkil/TSG_Platform.git
cd TSG_Platform
```

### 2. Ortam Değişkenlerini Tanımlayın
```bash
cp sicilius/backend/.env.example sicilius/backend/.env
cp sicilius/frontend/.env.local.example sicilius/frontend/.env.local
```

### 3. Tek Komutla Başlatın
```bash
# Docker ile Tüm Servisleri Ayağa Kaldırın
cd sicilius
docker-compose up -d --build

# Veya Yerel Geliştirme Scriptini Çalıştırın
./start_local.sh
```

### Servis Portları:
*   🌐 **Web Dashboard:** [http://localhost:3000](http://localhost:3000)
*   🚀 **Backend API Swagger:** [http://localhost:5001/docs](http://localhost:5001/docs)
*   📦 **MinIO S3 Panel:** [http://localhost:9001](http://localhost:9001)

---

## 🚢 Canlı Ortam Dağıtımı (Production Deployment)

Sistem; sıfır kesinti (zero-downtime) ve güvenli senkronizasyon için özel bir CI/CD otomasyon betiği barındırır:

```bash
./deploy_old_mac.sh
```

Bu betik:
1. Frontend projesini production standalone modunda derler.
2. Hassas dosyaları (`.env`, `.sh`) filtreleyerek `rsync` ile hedef sunucuya aktarır.
3. Docker konteynerlerini yeniden inşa eder ve Alembic veritabanı migrasyonlarını (`upgrade head`) otomatik uygular.

---

## 🛡️ Güvenlik, Gizlilik ve KVKK Uyumluluğu

*   **Veri Minimizasyonu:** Bireysel finansal/özel veriler yerine yalnızca kamuya açık resmi Ticaret Sicil Gazetesi ilanları işlenir.
*   **Maskeli Kimlik Koruması:** T.C. Kimlik numaraları sistem içerisinde otomatik olarak tuzlanıp maskelenir (`123******45`).
*   **RBAC & JWT:** Güçlü şifreleme ve yetki bazlı erişim denetimi.

---

## 📄 Lisans

Bu proje [MIT Lisansı](LICENSE) kapsamında açık kaynak olarak lisanslanmıştır.

<div align="center">
  <sub>Sicilius Core Architecture • Built with passion for high-performance RegTech & B2B Intelligence</sub>
</div>
