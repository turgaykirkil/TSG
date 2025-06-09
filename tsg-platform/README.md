# TSG Araştırma Platformu

Bu proje, TSG Araştırma Platformu'nun arka uç uygulamasını içerir.

## Gereksinimler

- Docker 20.10+ ve Docker Compose
- Python 3.10+
- PostgreSQL 13+
- Redis 6+

## Kurulum

1. Depoyu klonlayın:
   ```bash
   git clone https://github.com/yourusername/tsg-platform.git
   cd tsg-platform
   ```

2. Gerekli ortam değişkenlerini ayarlayın:
   ```bash
   cp backend/.env.example backend/.env
   ```
   Ardından `backend/.env` dosyasını düzenleyerek gerekli ayarları yapın.

3. Docker konteynerlerini başlatın:
   ```bash
   docker-compose up -d
   ```

4. Veritabanı migrasyonlarını çalıştırın:
   ```bash
   docker-compose exec backend alembic upgrade head
   ```

## Geliştirme Ortamı

### Yerel Geliştirme İçin

1. Python sanal ortamı oluşturun ve etkinleştirin:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # veya
   .\venv\Scripts\activate  # Windows
   ```

2. Gerekli bağımlılıkları yükleyin:
   ```bash
   pip install -r backend/requirements.txt
   ```

3. Veritabanı ve Redis başlatın:
   ```bash
   docker-compose up -d db redis
   ```

4. Uygulamayı çalıştırın:
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

## API Dokümantasyonu

Uygulama çalıştıktan sonra aşağıdaki adreslerden API dokümantasyonuna ulaşabilirsiniz:

- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## Test

Testleri çalıştırmak için:

```bash
pytest
```

## Dağıtım

Üretim ortamı için:

1. `.env` dosyasında `ENVIRONMENT=production` olarak ayarlayın
2. Güvenli bir `SECRET_KEY` belirleyin
3. `docker-compose -f docker-compose.prod.yml up -d` komutuyla üretim ortamını başlatın

## Lisans

Bu proje [MIT lisansı](LICENSE) altında lisanslanmıştır.
