#!/bin/bash

echo "Starting MacOS Server Optimization..."

# 1. Disable Sleep (Prevent server from sleeping)
echo "Disabling System Sleep..."
sudo pmset -a sleep 0
sudo pmset -a displaysleep 0
sudo pmset -a disksleep 0
sudo pmset -a hibernatemode 0
sudo pmset -a autorestart 1
sudo pmset -a womp 1 # Wake on LAN

# 2. Disable Spotlight Indexing (High CPU Usage Fix)
echo "Disabling Spotlight Indexing..."
sudo mdutil -i off /
sudo mdutil -E / # Erase index to free space/cpu

# 3. Disable Time Machine (Backups can kill IO)
echo "Disabling Time Machine auto-backup..."
sudo tmutil disablelocal

# 4. Renice Postgres (Give Database Higher Priority)
echo "Giving Priority to Postgres..."
pg_pid=$(pgrep -f "postgres" | head -n 1)
if [ -n "$pg_pid" ]; then
    sudo renice -n -10 -p $pg_pid
    echo "Postgres (PID $pg_pid) priority increased."
fi

# 5. Flush DNS (Network Stability)
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder

echo "Optimization Complete. System is now tuned for Server Mode."
