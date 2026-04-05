#!/bin/bash
# TSG_Platform - Canlı Sunucu (Oracle) Deployment Scripti
set -e

SERVER_IP="89.252.153.102"
USER="ubuntu"
REMOTE_DIR="~/sicilius"

echo "🚀 Deploying to $SERVER_IP..."

# 1. Dosyaları Senkronize Et
# exports klasörünü de ekledik ki bir daha asla gitmesin
echo "📦 Syncing CLEAN files via rsync..."
rsync -avz --delete \
    -e "ssh -o StrictHostKeyChecking=no" \
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
    ./ $USER@$SERVER_IP:$REMOTE_DIR

# 2. Sunucuda Container'ları Yeniden Başlat
echo "🔄 Rebuilding and restarting containers on server..."
ssh -o StrictHostKeyChecking=no $USER@$SERVER_IP << EOF
    cd $REMOTE_DIR
    
    if [ ! -f .env ]; then
        cp .env.example .env
        echo "⚠️ Created .env from example."
    fi

    echo "🏗️ Starting Docker Compose..."
    sudo docker compose -f docker-compose.prod.yml up -d --build --remove-orphans
    
    sudo docker image prune -f
EOF

echo "✅ Canlıya çıkış (Deployment) başarıyla tamamlandı!"
