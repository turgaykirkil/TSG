# Değişiklik Kaydı

Bu dosya, TSG Araştırma Platformu'nda yapılan tüm önemli değişiklikleri içerir.

## [Unreleased]

### Eklendi
- Arka plan görev yönetimi için kapsamlı bir sistem eklendi
  - `Scheduler` sınıfı ile periyodik görev yönetimi
  - Takılan işleri tespit etme ve yönetme özelliği
  - Eski iş kayıtlarını otomatik temizleme
- Yeni görev türleri eklendi:
  - `check_stuck_jobs`: Uzun süren işleri kontrol eder
  - `cleanup_jobs`: Eski iş kayıtlarını temizler
- Yapılandırılabilir görev ayarları eklendi
- Görev durumunu izlemek için API endpoint'leri eklendi
- Kapsamlı dokümantasyon eklendi

### Değiştirildi
- Ana uygulama başlatma ve kapatma işlemleri güncellendi
- Yapılandırma ayarları genişletildi
- Loglama iyileştirmeleri yapıldı

### Düzeltmeler
- CORS yapılandırması düzeltildi
- Görev yönetimi ile ilgili hatalar giderildi

## [0.1.0] - 2023-01-01

### Eklendi
- İlk sürüm oluşturuldu
- Temel CRUD işlemleri eklendi
- Kullanıcı kimlik doğrulama sistemi eklendi
