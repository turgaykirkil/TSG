#!/bin/bash
# start_local.sh - TSG_Platform Tüm Servisleri Tek Terminalde Başlatıcı (Maksimum Stabilite Versiyonu)

BASE_DIR="$(pwd)/sicilius"
LOG_DIR="$BASE_DIR/logs"
REMOTE_IP="sicilius-server.local"
REMOTE_USER="nalanmerci"
REMOTE_PASS="6118"

echo "🚀 TSG_Platform Lokal Ortam Hazırlanıyor..."

# 1. Aynı Wi-Fi kontrolü (Eski Mac erişilebilir mi?)
echo "🔍 Cihaz bağlantısı kontrol ediliyor (sicilius-server.local)..."
if nc -z -w 3 sicilius-server.local 22 &>/dev/null; then
    echo "🏠 Ev ağındasınız (Same Wi-Fi). Yerel tünel kuruluyor..."
    OUTSIDE="false"
else
    echo "🌍 Dış ağdasınız (Kafe/Ofis). Cloudflare TCP Tüneli kuruluyor..."
    OUTSIDE="true"
fi

# 0. Liman Temizliği (Daha agresif)
echo "🧹 Eski bağlantılar temizleniyor (5001, 3000, 5432)..."
lsof -ti:5001,3000,5432,5433,5434,9000 | xargs kill -9 2>/dev/null
sleep 2

# Log klasörünü oluştur
mkdir -p "$LOG_DIR"

if [ "$OUTSIDE" = "false" ]; then
    # --- EVDEYKEN (LOCAL SSH TUNNEL) ---
    echo "🔗 Veritabanı tüneli kuruluyor (SSH)..."
    (
        while true; do
            ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=15 -o ServerAliveCountMax=4 -o ExitOnForwardFailure=yes -N -L 127.0.0.1:5434:127.0.0.1:5432 $REMOTE_USER@$REMOTE_IP >> "$LOG_DIR/tunnel.log" 2>&1
            sleep 5
        done
    ) &
    TUNNEL_PARENT_PID=$!
else
    # --- DIŞARIDAYKEN (CLOUDFLARE TCP TUNNEL) ---
    echo "🔗 Cloudflare TCP Tüneli başlatılıyor (db.sicilius.com.tr)..."
    (
        while true; do
            cloudflared access tcp --hostname db.sicilius.com.tr --url 127.0.0.1:5434 >> "$LOG_DIR/tunnel.log" 2>&1
            sleep 5
        done
    ) &
    TUNNEL_PARENT_PID=$!
fi

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
trap "echo -e '\n🛑 Kapatılıyor...'; kill $TUNNEL_PARENT_PID; lsof -ti:5434,5001,3000 | xargs kill -9 2>/dev/null; kill 0" SIGINT SIGTERM

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


echo "✅ Sistem hazır! 'localhost:3000' adresinden giriş yapabilirsin."
wait
