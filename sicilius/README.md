# 🏢 Sicilius — Akıllı Şirket Araştırma ve Ağ Analizi Platformu

<div align="center">

![Version](https://img.shields.io/badge/version-1.1.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/production-active-success.svg)

**Türkiye Ticaret Sicil Gazetesi verilerini yapay zeka ile analiz eden, ilişki ağlarını haritalandıran ve kurumsal risk tespiti yapan yeni nesil istihbarat platformu.**

[sicilius.com.tr](https://sicilius.com.tr) · [NEXUS Modülü](/nexus) · [Pazarlama & Sunum Sayfası](/presentation)

</div>

---

## 📸 Genel Bakış ve Mimari

Sicilius; Türkiye Ticaret Sicil Gazetesi'nde (TSG) yayınlanan dağınık şirket ilanlarını otonom olarak tarayan, OCR ve NLP (Doğal Dil İşleme) teknolojileriyle yapılandırılmış verilere dönüştüren ve bu veriler üzerinden şirketler/kişiler arasındaki dolaylı bağları ortaya çıkaran modern bir RegTech (Regulatory Technology) platformudur.

```
                    ┌────────────────────────┐
                    │  Kullanıcı Arayüzü     │◀─── (Next.js 14, Tailwind CSS, Leaflet)
                    └───────────┬────────────┘
                                │ (HTTPS / API v1)
                                ▼
                    ┌────────────────────────┐
                    │ Caddy Reverse Proxy    │
                    └───────────┬────────────┘
                                │
                                ▼
                    ┌────────────────────────┐
                    │ FastAPI API Gateway    │
                    └────┬──────────────┬────┘
                         │              │
                         ▼              ▼
       ┌────────────────────┐        ┌────────────────────┐
       │ PostgreSQL/PostGIS │        │ MinIO (S3 Storage) │
       └────────────────────┘        └────────────────────┘
                 ▲
                 │ (İlişki Ağı ve Coğrafi Konum Verisi)
                 │
       ┌─────────┴──────────┐
       │ NEXUS Graph Engine │◄─── (Contagion & ML Anomali Modülleri)
       └────────────────────┘
                 ▲
                 │ (OCR & NLP Yapılandırılmış Çıktılar)
                 │
       ┌─────────┴──────────┐
       │  Scraping Worker   │◄─── (Python Tesseract OCR & NLP Parser)
       └────────────────────┘
```

---

## ✨ Temel Modüller ve Yetenekler

### 1. 🕸️ NEXUS Ağ Analizi ve Risk Motoru
Şirketler, ortaklar ve yöneticiler arasındaki ilişkileri derinlik 2'ye (Depth-2) kadar tarayarak ağ grafiği oluşturur.
*   **İnteraktif Graf:** React Force Graph ile 3D/2D ilişki görselleştirme.
*   **Contagion (Risk Yayılım) Simülasyonu:** Bir şirketteki finansal/hukuki risklerin ortaklık bağları üzerinden diğer şirketlere nasıl sirayet edebileceğini modeller.
*   **Sankey Akış Diyagramı:** Şirketler arası sermaye ve kredi geçişlerini görselleştirir.
*   **ML Anomali Tespiti:** Ağ üzerindeki şüpheli kümelenmeleri, paravan şirket yapılarını ve dolaylı ortaklıkları arka planda otomatik olarak analiz eder.

### 2. 🤖 Otonom OCR & NLP Veri İşleme Hattı (Pipeline)
*   **Otonom Worker:** Ticaret Sicil Gazetesi'nden her gün otomatik olarak yayınlanan PDF'leri çeker.
*   **Tesseract OCR:** Taranmış PDF'leri yüksek doğrulukla metne dönüştürür.
*   **NLP Parser:** Türkçe dil modellerine uygun kurallarla metinlerden şirket unvanı, MERSİS no, VKN, kurucu ortaklar, imza yetkilileri, adresler ve sermaye değişimlerini yapısal JSON formatında ayıklar.

### 3. 🗺️ Coğrafi Konum Analizi (PostGIS)
*   Adres verilerini otomatik temizler, normalize eder ve Nominatim / LocationIQ API'leri aracılığıyla koordinatlara (`Point(4326)`) dönüştürür.
*   PostGIS uzamsal indeksleme kullanarak bölgesel şirket yoğunluklarını Leaflet harita üzerinde kümeler halinde görselleştirir.

### 4. 📧 Entegre Mailbox Sistemi
*   Brevo API ve SMTP entegrasyonu sayesinde sistem içi davetler ve kullanıcı iletişim mesajları tek bir merkezden yönetilir.
*   Admin panel üzerinden gelen mesajlara anlık yanıt verme yeteneği mevcuttur.

---

## 🛠️ Teknoloji Yığını (Tech Stack)

### Frontend
*   **Next.js 14 (App Router):** Standalone production build modu ile optimize edilmiş yükleme süreleri.
*   **TypeScript:** Statik tip güvenliği.
*   **Tailwind CSS:** Glassmorphic ve modern koyu tema tasarımı.
*   **Leaflet.js:** Coğrafi kümeleme haritaları.
*   **React Force Graph & Plotly:** NEXUS ağ analizi grafiklerim.

### Backend
*   **FastAPI:** Python tabanlı, yüksek performanslı ve asenkron API altyapısı.
*   **SQLAlchemy & Alembic:** Veritabanı ORM ve güvenli migrasyon yönetimi.
*   **Celery / Arka Plan Görevleri:** OCR ve geocoding gibi ağır işlemleri asenkron yönetme.

### Veri & DevOps
*   **PostgreSQL 15 + PostGIS:** Uzamsal (Spatial) veri sorguları ve ilişkisel veritabanı.
*   **MinIO (S3 Uyumlu):** PDF dokümanları ve görsel dosyaları için yerel Object Storage çözümü.
*   **Caddy 2:** Otomatik Let's Encrypt SSL/TLS yönetimi ve güvenli ters proxy (Reverse Proxy).
*   **Docker & Docker Compose:** Tüm servislerin containerized olarak tek komutla ayağa kaldırılması.

---

## 🚀 Yerel Geliştirme (Local Development)

Yerel geliştirme ortamını kurmak için aşağıdaki adımları izleyin:

```bash
# 1. Projeyi klonlayın
git clone <repo-url>
cd sicilius

# 2. Çevre değişkenlerini yapılandırın
cp backend/.env.example backend/.env
cp frontend/.env.local.example frontend/.env.local

# 3. Docker container'larını başlatın
docker-compose up -d --build

# 4. Veritabanı migrasyonlarını uygulayın
docker-compose exec backend alembic upgrade head
```

Yerel erişim adresleri:
*   **Frontend:** `http://localhost:3000`
*   **Backend API Swagger:** `http://localhost:5001/docs`

---

## 🛡️ Canlı Sunucu Deployment (Production)

Sicilius, şirket bünyesindeki Mac Mini sunucusunda (`sicilius-server.local`) Docker üzerinde canlı olarak çalışmaktadır.

Canlıya güvenli geçiş için hazırlanan `deploy_old_mac.sh` scripti yerel terminalden tek tetikleme ile çalışır:
```bash
./deploy_old_mac.sh
```
*Bu script; yerelde Next.js build'ini alır, gerekli kaynakları rsync ile sunucuya taşır, sunucuda Docker imajlarını sıfır downtime ile yeniden derler ve database migrasyonlarını otomatik tamamlar.*

---

## 📂 Proje Dizin Yapısı

```
sicilius/
├── backend/            # FastAPI backend projesi
│   ├── app/            # API endpointleri, modeller, servisler ve görevler
│   └── alembic/        # Veritabanı migrasyon geçmişi
├── frontend/           # Next.js 14 frontend projesi
│   ├── src/            # Sayfalar (App Router), bileşenler ve grafikler
│   └── public/         # Statik sayfalar, görseller, NEXUS ve presentation assetleri
├── ocr_app/            # Swift tabanlı yerel OCR companion modülü
├── Caddyfile           # Caddy web sunucusu proxy kuralları
├── docker-compose.yml  # Docker servis tanımları
└── deploy_old_mac.sh   # Otomatik deployment betiği
```

---

## 🔒 Güvenlik

*   **JWT & RBAC:** Kullanıcı yetkilendirmesi ve Rol Tabanlı Erişim Kontrolü (Admin, Standart).
*   **İçerik Güvenlik Politikası (CSP):** Next.js ve CDN kütüphanelerine özel tanımlı katı CSP kuralları.
*   **Hassas Dosya Koruması:** `.env` ve SSH anahtarı gibi gizli veriler Git geçmişinden ve rsync transferlerinden tamamen izole edilmiştir.
