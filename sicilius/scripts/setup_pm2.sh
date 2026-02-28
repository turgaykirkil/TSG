#!/bin/bash
# PM2 Başlangıç ve Log Ayarları Scripti
# Kullanım: ./setup_pm2.sh

# PM2 kurulu mu?
if ! command -v pm2 &> /dev/null; then
    echo "⚠️ PM2 bulunamadı. Kuruluyor..."
    npm install -g pm2
fi

# Startup Ayarı (macOS için LaunchAgent oluşturur)
echo "🔧 PM2 Startup ayarlanıyor..."
pm2 startup
# Not: Eğer çıktı bir komut verirse, onu kopyalayıp çalıştırmanız gerekebilir.
# MacOS'ta genellikle otomatik yapar veya şunu önerir:
# pm2 startup launchd

# Log Rotate Eklentisi (Disk dolmasını önlemek için)
echo "🔄 PM2 Log Rotate kuruluyor..."
pm2 install pm2-logrotate

# Ayarlar (Örn: Maksimum 10MB log, 10 yedek)
pm2 set pm2-logrotate:max_size 10M
pm2 set pm2-logrotate:retain 10
pm2 set pm2-logrotate:compress true

echo "✅ PM2 ayarları tamamlandı. Mevcut süreçleri kaydetmek için 'pm2 save' çalıştırılıyor..."
pm2 save
