#!/bin/bash
# start_local.sh - TSG_Platform Tüm Servisleri Tek Terminalde Başlatıcı (Maksimum Stabilite Versiyonu)

BASE_DIR="$(pwd)/sicilius"
LOG_DIR="$BASE_DIR/logs"
REMOTE_IP="89.252.153.102"
REMOTE_USER="ubuntu"
REMOTE_PASS="q27MB7kCAJryfz"

echo "🚀 TSG_Platform Lokal Ortam Hazırlanıyor..."

# 0. Liman Temizliği (Daha agresif)
echo "🧹 Eski bağlantılar temizleniyor (5001, 3000, 5432)..."
lsof -ti:5001,3000,5432,5433,5434 | xargs kill -9 2>/dev/null
sleep 2

# Log klasörünü oluştur
mkdir -p "$LOG_DIR"

# 1. Veritabanı Tüneli (SSH Tunnel) - PERSISTENT & IPv4 ONLY
echo "🔗 Veritabanı tüneli kuruluyor (Persistence & IPv4)..."
cat << EOF > /tmp/db_tunnel.exp
#!/usr/bin/expect -f
set timeout -1
# -o ExitOnForwardFailure=yes ile port çakışması varsa hata verir
spawn ssh -o StrictHostKeyChecking=no -o PreferredAuthentications=password -o ServerAliveInterval=15 -o ServerAliveCountMax=4 -o ExitOnForwardFailure=yes -N -L 127.0.0.1:5434:172.18.0.6:5432 $REMOTE_USER@$REMOTE_IP
expect {
    "*assword:*" {
        send "$REMOTE_PASS\r"
        exp_continue
    }
    eof
}
EOF
chmod +x /tmp/db_tunnel.exp

# Tüneli bir döngü içinde arka planda başlat (koparsa geri gelir)
(
    while true; do
        /tmp/db_tunnel.exp >> "$LOG_DIR/tunnel.log" 2>&1
        echo "⚠️ Tünel koptu/kapandı ($(date)), 5 saniye içinde yeniden bağlanılıyor..." >> "$LOG_DIR/tunnel.log"
        sleep 5
    done
) &
TUNNEL_PARENT_PID=$!

# 2. Tünelin Hazır Olmasını Bekle (IPv4 ile Kontrol)
echo -n "⏳ Veritabanı bağlantısı (127.0.0.1) bekleniyor"
MAX_RETRIES=30
COUNT=0
while ! nc -z -v 127.0.0.1 5434 2>/dev/null; do
    echo -n "."
    sleep 1
    COUNT=$((COUNT+1))
    if [ $COUNT -ge $MAX_RETRIES ]; then
        echo -e "\n❌ HATA: Tünel kurulamadı! $LOG_DIR/tunnel.log dosyasına bakın."
        kill $TUNNEL_PARENT_PID
        exit 1
    fi
done
echo -e "\n✅ Veritabanı tüneli aktif!"

# Trap: Ctrl+C (PID temizliği güncellendi)
trap "echo -e '\n🛑 Kapatılıyor...'; kill $TUNNEL_PARENT_PID; lsof -ti:5432 | xargs kill -9 2>/dev/null; rm /tmp/db_tunnel.exp 2>/dev/null; kill 0" SIGINT SIGTERM EXIT

# Ortam Değişkenleri
export LOG_LEVEL=INFO
export REQUEST_LOGGING=true
export PYTHONPATH=$BASE_DIR/backend
export ENVIRONMENT=development

# 3. Backend (Port 5001)
echo "▶ Backend başlatılıyor..."
(cd "$BASE_DIR/backend" && uvicorn app.main:app --reload --host 0.0.0.0 --port 5001 --log-level info) 2>&1 | sed -u -e "s/^/\x1b[32m[BACKEND]\x1b[0m /" | tee -a "$LOG_DIR/backend.log" &

# 4. Celery Scraping Worker
echo "▶ Scraping Worker başlatılıyor..."
(cd "$BASE_DIR/backend" && celery -A app.core.celery_app worker --loglevel=info --concurrency=1) 2>&1 | sed -u -e "s/^/\x1b[33m[CELERY ]\x1b[0m /" | tee -a "$LOG_DIR/celery.log" &

# 5. Frontend (Port 3000)
echo "▶ Frontend başlatılıyor..."
(cd "$BASE_DIR/frontend" && npm run dev) 2>&1 | sed -u -e "s/^/\x1b[36m[FRONTEN]\x1b[0m /" | tee -a "$LOG_DIR/frontend.log" &

# 6. Swift OCR App
echo "▶ OCR App başlatılıyor..."
(cd "$BASE_DIR/ocr_app" && swift run ocr_app) 2>&1 | sed -u -e "s/^/\x1b[35m[OCR_APP]\x1b[0m /" | tee -a "$LOG_DIR/ocr.log" &

echo "✅ Sistem hazır! 'localhost:3000' adresinden giriş yapabilirsin."
wait
