#!/bin/bash
# Sicilius Backend Development Startup Script
# Automatically ensures the SSH tunnel to the production database is established
# before starting the FastAPI server.

echo ">>> Sicilius Backend Startup Sequence Initiated <<<"

# 1. Clean up any existing broken/zombie SSH tunnels on port 5433
if lsof -i:5433 -t >/dev/null; then
  echo "[+] Eski (zombi) SSH tüneli bulundu, temizleniyor..."
  lsof -i:5433 -t | xargs kill -9
  sleep 1
fi

echo "[+] Yeni SSH database tüneli kuruluyor. Uzak veritabanı IP'si bulunuyor..."

# Dinamik olarak sicilius-db-1 container IP'sini uzak sunucudan alıyoruz
DB_IP=$(ssh ubuntu@89.252.153.102 "docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' sicilius-db-1")

if [ -z "$DB_IP" ]; then
    echo "[-] Failed to discover remote database IP!"
    exit 1
fi

echo "[+] Remote database IP found: $DB_IP. Establishing tunnel..."

# -o ServerAliveInterval=60 parametresi uykudan uyanmalarda bağlantının takılı kalmasını önler
ssh -f -N -o ServerAliveInterval=60 -L 5433:$DB_IP:5432 -L 9000:localhost:9000 ubuntu@89.252.153.102

if [ $? -eq 0 ]; then
    echo "[+] SSH Tunnel successfully established to $DB_IP."
else
    echo "[-] Failed to establish SSH tunnel. Make sure you have SSH access to 89.252.153.102."
    exit 1
fi

# 2. Get backend directory absolute path relative to this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/backend" || exit 1

# 3. Start the FastAPI application
echo "[+] Starting FastAPI server..."
uvicorn app.main:app --host 0.0.0.0 --port 5001
