#!/bin/bash
# Sicilius Veritabanı Yedekleme Scripti
# Kullanım: ./backup_db.sh
# Bu script veritabanını döküm (dump) alıp masaüstündeki 'Sicilius_Backups' klasörüne kaydeder.
# Son 7 günden eski yedekleri otomatik siler.

# Ayarlar
DB_USER="sicilius_user"     # Veritabanı kullanıcısı (Remote sunucuya göre ayarlayın)
DB_HOST="localhost"         # Veritabanı sunucusu
DB_NAME="sicilius"          # Veritabanı adı
BACKUP_ROOT="$HOME/Desktop/Sicilius_Backups" # Yedekleme klasörü
DATE=$(date +"%Y%m%d_%H%M%S")
FILENAME="sicilius_backup_$DATE.sql"

# Klasör oluştur
mkdir -p "$BACKUP_ROOT"

echo "📦 Veritabanı yedekleniyor: $DB_NAME..."

# pg_dump komutu (Docker kullanıyorsanız 'docker exec' eklemeniz gerekebilir)
# Eğer native postgres ise:
if command -v pg_dump &> /dev/null; then
    pg_dump -U "$DB_USER" -h "$DB_HOST" "$DB_NAME" > "$BACKUP_ROOT/$FILENAME"
else
    echo "⚠️ pg_dump bulunamadı! Eğer Docker kullanıyorsanız scripti güncelleyin."
    exit 1
fi

if [ $? -eq 0 ]; then
    echo "✅ Yedek alındı: $BACKUP_ROOT/$FILENAME"
else
    echo "❌ Yedekleme başarısız oldu!"
    exit 1
fi

# Temizlik (7 günden eski dosyaları sil)
echo "🧹 Eski yedekler temizleniyor (7 günden eski)..."
find "$BACKUP_ROOT" -type f -name "sicilius_backup_*.sql" -mtime +7 -exec rm {} \;
echo "✅ İşlem tamamlandı."
