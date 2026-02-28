#!/bin/bash
# Sicilius Veritabanı Geri Yükleme Scripti
# Kullanım: ./restore_db.sh <sql_dosyası_yolu>

if [ -z "$1" ]; then
    echo "❌ Hata: Lütfen bir SQL dosyası belirtin."
    echo "Kullanım: ./restore_db.sh /path/to/backup.sql"
    exit 1
fi

SQL_FILE="$1"

# Ayarlar
DB_USER="sicilius_user"
DB_HOST="localhost"
DB_NAME="sicilius"

echo "⚠️  DİKKAT: Bu işlem '$DB_NAME' veritabanı üzerine yazacaktır!"
echo "Veriler silinebilir veya dğeişebilir."
read -p "Devam etmek istiyor musunuz? (evet/hayir): " CONFIRM

if [ "$CONFIRM" != "evet" ]; then
    echo "İşlem iptal edildi."
    exit 1
fi

echo "📦 Geri yükleme başlıyor: $SQL_FILE..."

if command -v psql &> /dev/null; then
    # Hata durumunda durma opsiyonu (-v ON_ERROR_STOP=1) eklenebilir
    psql -U "$DB_USER" -h "$DB_HOST" -d "$DB_NAME" < "$SQL_FILE"
else
    echo "⚠️ psql bulunamadı! Docker kullanıyorsanız scripti güncelleyin."
    exit 1
fi

if [ $? -eq 0 ]; then
    echo "✅ Geri yükleme başarıyla tamamlandı."
else
    echo "❌ Geri yükleme sırasında hata oluştu."
    exit 1
fi
