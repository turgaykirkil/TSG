#!/bin/bash
set -e

# Renkler
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

SERVER_IP="89.252.153.102"
USER="root"
REMOTE_DIR="/var/www/nexus"

echo -e "${BLUE}🚀 Starting Fast Deployment (Mac Build -> Server Deploy)...${NC}"

# M3 Mac üzerinde derleme yaparken, hedef sunucunun (Linux x86_64) mimarisine göre derleme yapmasını zorluyoruz.
export DOCKER_DEFAULT_PLATFORM=linux/amd64

# 1. Local Build (M3 Mac)
echo -e "${GREEN}📦 Building Docker images locally using your powerful Mac...${NC}"
# --build-arg vb. tüm ayarları docker-compose.prod.yml'den otomatik okuyacak
docker compose -f docker-compose.prod.yml build

# 2. Transfer Images
echo -e "${BLUE}🚢 Transferring Frontend image to server (This might take a minute)...${NC}"
docker save sicilius_frontend:latest | ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=60 -o ServerAliveCountMax=120 $USER@$SERVER_IP "sudo docker load"

echo -e "${BLUE}🚢 Transferring Backend image to server...${NC}"
docker save sicilius_backend:latest | ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=60 -o ServerAliveCountMax=120 $USER@$SERVER_IP "sudo docker load"

# 3. Sync configs (Sadece gerekli ayar dosyaları, kaynak kodlar gitmeyecek çünkü imajın içinde var)
echo -e "${GREEN}📁 Syncing configuration files...${NC}"
rsync -avz --delete \
    -e "ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=60 -o ServerAliveCountMax=120" \
    --exclude 'frontend/' \
    --exclude 'backend/' \
    --exclude 'venv' \
    --exclude 'node_modules' \
    --exclude '__pycache__' \
    --exclude '.git' \
    --exclude '.env' \
    --exclude '.DS_Store' \
    --exclude '.next' \
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

# 4. Restart remote compose
echo -e "${BLUE}🔄 Restarting containers on server...${NC}"
ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=60 -o ServerAliveCountMax=120 $USER@$SERVER_IP << EOF
    cd $REMOTE_DIR
    
    if [ ! -f .env ]; then
        cp .env.example .env
        echo "⚠️ Created .env from example."
    fi

    echo "🏗️ Starting Docker Compose with pre-built images..."
    # --build parametresi kaldırıldı! Sadece hazır imajları kullanarak ayağa kaldıracak.
    sudo docker compose -f docker-compose.prod.yml up -d --remove-orphans
    
    sudo docker image prune -f
EOF

echo -e "${GREEN}✅ Deployment Complete! Artık saatlerce beklemek yok.${NC}"
