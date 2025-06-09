# TSG Platform - API ve Servis Bağlantıları

## API Dokümantasyonu
- **Swagger UI (Interactive API Docs):** http://localhost:5001/api/docs
- **ReDoc (Alternative Docs):** http://localhost:5001/api/redoc
- **OpenAPI JSON:** http://localhost:5001/api/openapi.json

## API Endpointleri

### Kimlik Doğrulama (Authentication)
- `POST /api/v1/auth/login` - Kullanıcı girişi
- `POST /api/v1/auth/register` - Yeni kullanıcı kaydı
- `POST /api/v1/auth/forgot-password` - Şifremi unuttum
- `POST /api/v1/auth/reset-password` - Şifre sıfırlama
- `POST /api/v1/auth/refresh` - Token yenileme

### Kullanıcılar (Users)
- `GET /api/v1/users/` - Tüm kullanıcıları listele
- `POST /api/v1/users/` - Yeni kullanıcı oluştur
- `GET /api/v1/users/me` - Giriş yapmış kullanıcı bilgileri
- `GET /api/v1/users/{user_id}` - Kullanıcı detayları
- `PUT /api/v1/users/{user_id}` - Kullanıcı güncelle
- `DELETE /api/v1/users/{user_id}` - Kullanıcı sil

### Firmalar (Companies)
- `GET /api/v1/companies/` - Tüm firmaları listele
- `POST /api/v1/companies/` - Yeni firma oluştur
- `GET /api/v1/companies/{company_id}` - Firma detayları
- `PUT /api/v1/companies/{company_id}` - Firma güncelle
- `DELETE /api/v1/companies/{company_id}` - Firma sil

### Kişiler (Persons)
- `GET /api/v1/persons/` - Tüm kişileri listele
- `POST /api/v1/persons/` - Yeni kişi oluştur
- `GET /api/v1/persons/{person_id}` - Kişi detayları
- `PUT /api/v1/persons/{person_id}` - Kişi güncelle
- `DELETE /api/v1/persons/{person_id}` - Kişi sil

### Resmi Gazeteler (Gazettes)
- `GET /api/v1/gazettes/` - Tüm resmi gazeteleri listele
- `POST /api/v1/gazettes/` - Yeni resmi gazete ekle
- `GET /api/v1/gazettes/{gazette_id}` - Resmi gazete detayları
- `PUT /api/v1/gazettes/{gazette_id}` - Resmi gazete güncelle
- `DELETE /api/v1/gazettes/{gazette_id}` - Resmi gazete sil

### Dosya Yüklemeleri (File Uploads)
- `GET /api/v1/file-uploads/` - Tüm yüklenen dosyaları listele
- `POST /api/v1/file-uploads/` - Dosya yükle
- `GET /api/v1/file-uploads/{file_id}` - Dosya bilgileri
- `GET /api/v1/file-uploads/{file_id}/download` - Dosyayı indir
- `DELETE /api/v1/file-uploads/{file_id}` - Dosyayı sil

### İşler (Jobs)
- `GET /api/v1/jobs/` - Tüm işleri listele
- `POST /api/v1/jobs/` - Yeni iş oluştur
- `GET /api/v1/jobs/{job_id}` - İş detayları
- `PUT /api/v1/jobs/{job_id}` - İş güncelle
- `DELETE /api/v1/jobs/{job_id}` - İşi sil

### Yardımcı Araçlar (Utilities)
- `GET /api/v1/utils/health` - API sağlık kontrolü
- `GET /api/v1/utils/version` - API versiyon bilgisi
- `GET /api/v1/utils/settings` - Uygulama ayarları
- `POST /api/v1/utils/search` - Genel arama

## Frontend
- **Ana Sayfa:** http://localhost:3000
- **Giriş Sayfası:** http://localhost:3000/login
- **Kayıt Sayfası:** http://localhost:3000/register

## Veritabanı
- **PgAdmin (Database Management):** http://localhost:5050
  - Email: admin@admin.com
  - Şifre: admin

## Diğer Servisler
- **Redis Commander (Redis Yönetimi):** http://localhost:8081
- **MinIO (Dosya Depolama):** http://localhost:9001
  - Kullanıcı Adı: minioadmin
  - Şifre: minioadmin

## Not
Bu bağlantılar, yerel geliştirme ortamınız için geçerlidir. Canlı ortamda domain ve portlar farklı olacaktır.

# Docker Compose ile tüm servisleri başlatma
docker-compose up -d
docker-compose up --build -d

# Sadece belirli bir servisi başlatmak için (örneğin sadece backend)
docker-compose up -d backend

# Logları görüntülemek için
docker-compose logs -f

# Tüm konteynerleri durdurmak için
docker-compose down

# Tüm konteynerleri ve volume'leri silmek için
docker-compose down -v

lsof -ti :3002 | xargs kill -9