# TSG Platform Projesi Analizi

Bu proje, **TSG Platform** adında tam teşekküllü bir web uygulamasıdır. Modern bir mimariyle, backend ve frontend katmanları net bir şekilde ayrılmıştır.

### **Genel Mimarisi**

*   **Full-Stack Uygulama:** Proje, bir Python/FastAPI backend'i ve bir TypeScript/Next.js frontend'inden oluşuyor.
*   **Konteynerizasyon:** `docker-compose.yml` ve her katmandaki `Dockerfile` dosyaları, projenin geliştirme ve dağıtım için Docker ile konteynerize edildiğini gösteriyor. Bu, servislerin (backend, frontend, veritabanı vb.) birlikte kolayca çalıştırılmasını sağlar.
*   **Monorepo Yapısı:** Backend ve frontend kodları aynı ana depoda (`tsg-platform`) bulunuyor.

### **Backend Analizi (`backend/`)**

*   **Teknoloji:** Python kullanılıyor. `requirements.txt` dosyasına göre ana framework **FastAPI**. Bu, yüksek performanslı API'ler oluşturmak için modern bir seçimdir.
*   **Veritabanı ve ORM:** `alembic.ini` dosyasının varlığı, veritabanı şema göçleri (migrations) için **Alembic**'in kullanıldığını gösteriyor. Bu da genellikle **SQLAlchemy** ORM (Object-Relational Mapper) ile birlikte kullanılır. `app/db/` ve `app/models/` klasörleri bu yapıyı doğruluyor.
*   **Mimari ve Kod Yapısı:**
    *   **Katmanlı Mimari:** Kod, sorumluluklara göre `api`, `crud`, `models`, `schemas`, `services` gibi klasörlere ayrılmış. Bu, temiz ve sürdürülelebilir bir kod tabanı için harika bir pratiktir.
    *   **`crud` Katmanı:** Veritabanı işlemlerini (Create, Read, Update, Delete) yönetir.
    *   **`schemas` Katmanı:** Pydantic modellerini içerir ve API veri doğrulamasını ve serileştirmesini sağlar.
    *   **`services` Katmanı:** İş mantığını içerir. `scraper_service.py` dosyasının varlığı, projenin **web scraping** (veri kazıma) yeteneklerine sahip olduğunu gösteriyor.
    *   **`ocr_service`:** Optik Karakter Tanıma (OCR) için ayrı bir servis bulunuyor. Bu servis muhtemelen taranmış belgelerden veya resimlerden (örneğin `data/gazette_pdfs/` içindeki PDF'lerden) metin çıkarmak için kullanılıyor.
*   **Arka Plan Görevleri:** `app/tasks/` ve `app/core/scheduler.py` dosyaları, periyodik olarak çalışan arka plan görevleri (örneğin, takılı kalmış işleri kontrol etme, temizlik yapma) olduğunu gösteriyor.

### **Frontend Analizi (`frontend/`)**

*   **Teknoloji:** **TypeScript** ile yazılmış bir **Next.js** (React framework'ü) uygulaması. Bu, hem sunucu tarafında render (SSR) hem de statik site oluşturma (SSG) yetenekleri sunan popüler ve güçlü bir seçimdir.
*   **Stil (Styling):** `tailwind.config.js` dosyası, stil için **Tailwind CSS** kullanıldığını gösteriyor. Bu, hızlı ve tutarlı bir şekilde modern arayüzler oluşturmayı sağlar.
*   **Kod Yapısı:** `src/` altında `app`, `components`, `contexts`, `hooks`, `lib` gibi standart ve modern bir React/Next.js proje yapısı kullanılıyor.
*   **Dağıtım (Deployment):** `nginx.conf` dosyası, production ortamında Next.js uygulamasını sunmak için Nginx'in bir reverse proxy olarak kullanıldığını düşündürüyor.

### **Özet ve Çıkarım**

TSG Platform, muhtemelen resmi belgelerden (ticaret sicili gazetesi gibi, `gazette` isminden yola çıkarak) veya diğer web kaynaklarından veri kazıyan, bu verileri OCR ile işleyen ve kullanıcıların (şirketler, kişiler vb.) bu verileri arayüz üzerinden görüntülemesini ve yönetmesini sağlayan bir veri platformudur.

Kullanılan teknolojiler ve proje yapısı, modern, ölçeklenebilir ve bakımı kolay bir uygulama geliştirme hedefini yansıtıyor.
