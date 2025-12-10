#!/bin/bash
# MinIO Cloudflare Tunnel Deployment Script
# Automated deployment for production server

set -e

echo "=== MinIO Cloudflare Tunnel Configuration ==="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# 1. Check prerequisites
echo -e "${YELLOW}1. Checking prerequisites...${NC}"
if ! command -v cloudflared &> /dev/null; then
    echo -e "${RED}ERROR: cloudflared not found${NC}"
    exit 1
fi
echo -e "${GREEN}✓ cloudflared installed${NC}"

# 2. Backup
echo ""
echo -e "${YELLOW}2. Backing up current configuration...${NC}"
BACKUP_FILE="/root/.cloudflared/config.yml.backup.$(date +%Y%m%d_%H%M%S)"
cp /root/.cloudflared/config.yml "$BACKUP_FILE"
echo -e "${GREEN}✓ Backup: $BACKUP_FILE${NC}"

# 3. Extract tunnel info from current config
TUNNEL_ID=$(grep "^tunnel:" /root/.cloudflared/config.yml | awk '{print $2}')
CREDENTIALS_FILE=$(grep "^credentials-file:" /root/.cloudflared/config.yml | awk '{print $2}')

# 4. Create new configuration
echo ""
echo -e "${YELLOW}4. Creating new configuration with MinIO rules...${NC}"

cat > /root/.cloudflared/config.yml << EOF
tunnel: $TUNNEL_ID
credentials-file: $CREDENTIALS_FILE

ingress:
  # MinIO Console (Web UI)
  - hostname: minio.turgaysicil.com
    service: http://localhost:9001
  
  # MinIO S3 API
  - hostname: s3.turgaysicil.com
    service: http://localhost:9000
  
  # Frontend Application
  - hostname: turgaysicil.com
    service: http://localhost:3000
  
  # Backend API
  - hostname: api.turgaysicil.com
    service: http://localhost:5001
  
  # Catch-all (MUST be last)
  - service: http_status:404
EOF

echo -e "${GREEN}✓ Configuration updated${NC}"

# 5. Restart service
echo ""
echo -e "${YELLOW}5. Restarting cloudflared service...${NC}"
systemctl restart cloudflared
sleep 3

# 6. Check status
if systemctl is-active --quiet cloudflared; then
    echo -e "${GREEN}✓ cloudflared service is running${NC}"
else
    echo -e "${RED}ERROR: Service failed to start${NC}"
    echo "Rolling back..."
    cp "$BACKUP_FILE" /root/.cloudflared/config.yml
    systemctl restart cloudflared
    exit 1
fi

echo ""
echo -e "${GREEN}=== Deployment Complete ===${NC}"
echo ""
echo "Next steps:"
echo "1. Verify DNS records in Cloudflare:"
echo "   - minio.turgaysicil.com"
echo "   - s3.turgaysicil.com"
echo ""
echo "2. Test endpoints:"
echo "   curl https://minio.turgaysicil.com"
echo "   curl https://s3.turgaysicil.com"
echo ""
echo "3. Update local backend .env:"
echo "   MINIO_ENDPOINT=s3.turgaysicil.com:443"
echo "   MINIO_USE_SSL=true"
