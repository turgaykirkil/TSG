# Arka Plan Görev Sistemi

Bu doküman, TSG Araştırma Platformu'nun arka plan görev sistemi hakkında detaylı bilgi içerir.

## Genel Bakış

Arka plan görev sistemi, uzun süren işlemleri asenkron olarak yönetmek için tasarlanmıştır. Bu sistem şu bileşenlerden oluşur:

1. **Görev Yöneticisi (Scheduler)**: Periyodik olarak çalışacak görevleri yönetir.
2. **Görev İşleyicileri**: Belirli bir işi yapan fonksiyonlardır.
3. **İzleme ve Raporlama**: Görevlerin durumunu izlemek ve raporlamak için API'ler.

## Mevcut Görevler

### 1. Takılan İşleri Kontrol Etme

**Dosya**: `app/tasks/check_stuck_jobs.py`

Bu görev, çok uzun süredir çalışan ve muhtemelen takılmış işleri kontrol eder.

**Özellikler**:
- Çalışma süresi belirli bir eşiği aşan işleri tespit eder
- Otomatik olarak yeniden deneyebilir veya başarısız olarak işaretleyebilir
- Yapılandırılabilir yeniden deneme sayısı ve zaman aşımı süreleri

**Varsayılan Çalışma Sıklığı**: 5 dakikada bir

### 2. Eski İş Kayıtlarını Temizleme

**Dosya**: `app/tasks/cleanup_jobs.py`

Bu görev, eski iş kayıtlarını veritabanından temizler.

**Özellikler**:
- Tamamlanmış işleri belirli bir süre sonra siler
- Başarısız işleri daha uzun süre saklayabilir
- Yapılandırılabilir saklama süreleri

**Varsayılan Çalışma Sıklığı**: Günde bir kez

## Yeni Görev Ekleme

Yeni bir arka plan görevi eklemek için şu adımları izleyin:

1. `app/tasks/` dizininde yeni bir Python modülü oluşturun (örneğin, `my_task.py`)
2. Modül içinde `run_<görev_adi>` fonksiyonunu tanımlayın:

```python
def run_my_task(context):
    """Görev açıklaması."""
    # Görev parametrelerini al
    params = context.get("parameters", {})
    db = context.get("db")
    update_progress = context.get("update_progress")
    
    # İlerlemeyi güncelle
    if update_progress:
        update_progress(10, "İşlem başlıyor...")
    
    # Görev mantığı buraya gelecek
    
    # İşlem tamamlandı
    if update_progress:
        update_progress(100, "İşlem tamamlandı")
    
    return {"status": "completed", "message": "İşlem başarıyla tamamlandı"}
```

3. Görevi `app/core/scheduler.py` dosyasındaki `init_scheduler` fonksiyonuna ekleyin:

```python
from app.tasks.my_task import run_my_task

# Mevcut görevlerin arasına ekleyin
scheduler.add_task(
    func=run_my_task,
    interval=3600,  # saniye cinsinden çalışma aralığı
    name="my_task",
    run_immediately=False
)
```

## API Uç Noktaları

### 1. Zamanlanmış Görevlerin Durumunu Alma

```
GET /scheduler/status
```

**Yanıt Örneği**:

```json
{
  "status": "running",
  "tasks": [
    {
      "name": "check_stuck_jobs",
      "interval": 300,
      "last_run": "2023-01-01T12:00:00Z",
      "next_run": "2023-01-01T12:05:00Z",
      "is_running": false,
      "current_runs": 0,
      "max_concurrent": 1
    }
  ]
}
```

## Yapılandırma

Arka plan görevleri, `app/core/config.py` dosyasındaki aşağıdaki ayarlarla yapılandırılabilir:

```python
# Maksimum eşzamanlı çalışacak işçi sayısı
BACKGROUND_TASKS_MAX_WORKERS = 10

# Bir işin takılı kabul edilmeden önce çalışabileceği maksimum süre (saniye)
JOB_TIMEOUT_SECONDS = 3600  # 1 saat

# Takılan işlerin kontrol edilme sıklığı (saniye)
STUCK_JOB_CHECK_INTERVAL = 300  # 5 dakika

# Bir işin takılı kabul edilmesi için geçmesi gereken minimum süre (saniye)
JOB_STUCK_AFTER_SECONDS = 1800  # 30 dakika

# Başarısız işler için maksimum yeniden deneme sayısı
MAX_JOB_RETRIES = 3

# Başarısız işlerin otomatik olarak yeniden denenip denemeyeceği
AUTO_RETRY_FAILED_JOBS = True

# Tamamlanmış iş kayıtlarının saklanma süresi (gün)
COMPLETED_JOB_RETENTION_DAYS = 30

# Başarısız iş kayıtlarının saklanma süresi (gün)
FAILED_JOB_RETENTION_DAYS = 90
```

## Hata Ayıklama

### Görevler Çalışmıyorsa

1. Scheduler'ın çalıştığından emin olun:
   ```bash
   curl http://localhost:5001/scheduler/status
   ```

2. Uygulama loglarını kontrol edin:
   ```bash
   tail -f logs/tsg_platform.log
   ```

3. Görevin doğru şekilde kaydedildiğinden emin olun:
   - Görev fonksiyonu `run_<isim>` formatında olmalı
   - Görev `app/tasks/` dizininde olmalı
   - Görev `init_scheduler` fonksiyonuna eklenmeli

### Görevler Çok Sık Çalışıyorsa

- Görevin `interval` değerini kontrol edin (saniye cinsinden)
- Aynı görevden birden fazla örneğin çalışmadığından emin olun

## En İyi Uygulamalar

1. **Hata Yönetimi**: Tüm görevler hata yönetimi içermelidir
2. **Kaynak Kullanımı**: Uzun süren görevler düzenli olarak ilerleme bildirmelidir
3. **Eşzamanlılık**: Aynı kaynağı kullanan görevler için uygun eşzamanlılık kontrolleri yapılmalıdır
4. **Loglama**: Tüm görevler yeterli loglama yapmalıdır
5. **İzlenebilirlik**: Her görev, ilerleme durumunu ve sonucunu raporlamalıdır
