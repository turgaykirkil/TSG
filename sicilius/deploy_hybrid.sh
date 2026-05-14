#!/bin/bash
# TSG_Platform - Hibrit Deployment Scripti
# Mac'te Frontend'i derler, sunucuda sadece hafif paket kurulumu yapar (OOM'yi engeller).
set -e

# Renkler
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

SERVER_IP="89.252.153.102"
USER="ubuntu"
REMOTE_DIR="~/sicilius"

echo -e "${BLUE}🚀 Hibrit Deployment Başlıyor (Mac'te Derle -> Sunucuda Çalıştır)...${NC}"

# 1. Frontend Build (Mac üzerinde)
echo -e "${GREEN}📦 Mac üzerinde Frontend derleniyor (npm run build)...${NC}"
cd frontend
# Eğer node_modules yoksa kur
if [ ! -d "node_modules" ]; then
    npm install --legacy-peer-deps
fi
npm run build
cd ..

# 2. Dosyaları Senkronize Et
echo -e "${BLUE}📁 Dosyalar sunucuya gönderiliyor (Mac'te derlenen .next klasörü dahil)...${NC}"
# Dikkat: --exclude '.next' KALDIRILDI! Çünkü Mac'te derlediğimizi sunucuya atıyoruz.
rsync -avz --delete \
    -e "ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=60 -o ServerAliveCountMax=120" \
    --exclude 'frontend/node_modules' \
    --exclude 'backend/venv' \
    --exclude 'venv' \
    --exclude 'node_modules' \
    --exclude '__pycache__' \
    --exclude '.git' \
    --exclude '.env' \
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

# 3. Sunucuda Container'ları Yeniden Başlat
echo -e "${BLUE}🔄 Sunucuda Docker işlemleri başlatılıyor (Çok daha az RAM harcayacak)...${NC}"
ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=60 -o ServerAliveCountMax=120 $USER@$SERVER_IP << EOF
    cd $REMOTE_DIR
    
    if [ ! -f .env ]; then
        cp .env.example .env
        echo "⚠️ Created .env from example."
    fi

    echo "🏗️ Starting Docker Compose for sicilius.com.tr..."
    # DOMAIN_NAME'i burada set ediyoruz ki hem Caddy hem Frontend kullansın.
    sudo DOMAIN_NAME=sicilius.com.tr docker compose -f docker-compose.prod.yml up -d --build --remove-orphans
    
    sudo docker image prune -f
EOF

echo -e "${GREEN}✅ Hibrit Deployment başarıyla tamamlandı!${NC}"
