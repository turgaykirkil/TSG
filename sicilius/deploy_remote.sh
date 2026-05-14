#!/bin/bash
# TSG_Platform - Canlı Sunucu (Oracle) Deployment Scripti
set -e

SERVER_IP="89.252.153.102"
USER="ubuntu"
REMOTE_DIR="~/sicilius"

echo "🚀 Deploying to $SERVER_IP..."

# 1. Frontend'i Lokalde Derle (Sunucunun RAM'i yetmiyor)
echo "🏗️ Frontend'i lokalde derliyoruz (NEXT_PUBLIC_API_URL=https://sicilius.com.tr)..."
cd frontend
# .env.local'i geçici olarak devre dışı bırak
if [ -f .env.local ]; then
    mv .env.local .env.local.bak
fi
NEXT_PUBLIC_API_URL=https://sicilius.com.tr npm run build
# .env.local'i geri yükle
if [ -f .env.local.bak ]; then
    mv .env.local.bak .env.local
fi
cd ..
echo "✅ Frontend derlemesi tamamlandı!"

# 2. Dosyaları Senkronize Et (.next dahil, ama .env hariç)
echo "📦 Syncing files via rsync (.next dahil)..."
rsync -avz --delete \
    -e "ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=60 -o ServerAliveCountMax=120" \
    --exclude 'venv' \
    --exclude 'node_modules' \
    --exclude '__pycache__' \
    --exclude '.git' \
    --exclude '.env*' \
    --exclude '.DS_Store' \
    --exclude '.pytest_cache' \
    --exclude '.playwright_user_data' \
    --exclude 'pw-browsers' \
    --exclude 'test_pdfs' \
    --exclude 'ocr_batch_results*' \
    --exclude 'exports' \
    --exclude 'data' \
    --exclude '.build' \
    --exclude '.swiftpm' \
    --exclude 'ops' \
    ./ $USER@$SERVER_IP:$REMOTE_DIR

# 2. Sunucuda Container'ları Yeniden Başlat
echo "🔄 Rebuilding and restarting containers on server..."
# SSH bağlantısı için de Keep-Alive parametrelerini ekledik
ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=60 -o ServerAliveCountMax=120 $USER@$SERVER_IP << EOF
    cd $REMOTE_DIR
    
    if [ ! -f .env ]; then
        cp .env.example .env
        echo "⚠️ Created .env from example."
    fi

    echo "🧹 Cleaning old containers and caches..."
    sudo docker compose -f docker-compose.prod.yml down --remove-orphans
    
    # Docker build cache ve eski imajları temizle (DİKKAT: volume'ları silmiyoruz, veritabanı korunur)
    sudo docker system prune -af
    
    echo "🏗️ Starting FRESH Build (No-Cache, This will take time)..."
    export DOMAIN_NAME=sicilius.com.tr
    sudo -E docker compose -f docker-compose.prod.yml up -d --build --force-recreate
    
    echo "🧹 Final cleanup of intermediate build images..."
    sudo docker image prune -f
EOF

echo "✅ Canlıya çıkış (Deployment) başarıyla tamamlandı!"
