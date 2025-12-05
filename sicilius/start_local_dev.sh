#!/bin/bash
# Local Development Helper Script - Robust Version
# This script sets up SSH tunnels and keeps them alive.
# IT WILL BLOCK THE TERMINAL. Keep this terminal open or run in a separate tab.

trap 'kill $(jobs -p)' EXIT

echo "🔧 Setting up robust local development environment..."
echo "ℹ️  This script will keep running to ensure tunnels stay alive."
echo "ℹ️  Press Ctrl+C to stop all tunnels."
echo ""

# Function to manage tunnel
start_tunnel() {
    local local_port=$1
    local remote_target=$2
    local name=$3
    
    while true; do
        echo "📡 [$name] Connecting tunnel ($local_port -> $remote_target)..."
        # -N: Do not execute a remote command
        # -L: Port forwarding
        # -o ServerAliveInterval=60: Send keepalive every 60s
        # -o ServerAliveCountMax=3: Disconnect after 3 missed keepalives
        # -o ExitOnForwardFailure=yes: Exit if port binding fails (so we can retry)
        ssh -N -L $local_port:$remote_target \
            -o ServerAliveInterval=60 \
            -o ServerAliveCountMax=3 \
            -o ExitOnForwardFailure=yes \
            nalanmerci@192.168.1.5
            
        exit_code=$?
        echo "⚠️ [$name] Tunnel disconnected (code $exit_code). Retrying in 2s..."
        sleep 2
    done
}

# Start tunnels in background
start_tunnel 5433 "localhost:5432" "Database" &
start_tunnel 9000 "localhost:9000" "MinIO" &
start_tunnel 9001 "localhost:9001" "MinIO Console" &

echo "✅ Tunnels initialized."
echo ""
echo "📝 Configuration:"
echo "   DB: postgresql://sicilius:wa4Q7UJ3D7VQSsxYMYah1oKX@localhost:5433/sicilius"
echo "   MinIO: http://localhost:9000"
echo ""

# Wait for all background jobs
wait
