import subprocess
import time
import socket
import os
import signal
import sys

# Configuration
TUNNELS = [
    {"name": "Database", "local_port": 5433, "remote_target": "localhost:5432"},
    {"name": "MinIO", "local_port": 9000, "remote_target": "localhost:9000"},
    {"name": "MinIO Console", "local_port": 9001, "remote_target": "localhost:9001"},
]
SSH_USER = "ubuntu"
SSH_HOST = "89.252.153.102"

def is_port_open(port):
    """Checks if a local port is listening."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def kill_process_on_port(port):
    """Finds and kills process utilizing the port."""
    try:
        # lsof -t -i:port returns PID
        pid = subprocess.check_output(["lsof", "-t", f"-i:{port}"]).decode().strip()
        if pid:
            os.kill(int(pid), signal.SIGKILL)
            print(f"Killed stale process {pid} on port {port}")
    except (subprocess.CalledProcessError, ValueError):
        pass

def start_tunnel(tunnel_config):
    """Starts a specific SSH tunnel."""
    cmd = [
        "ssh", "-N", 
        "-L", f"{tunnel_config['local_port']}:{tunnel_config['remote_target']}",
        "-o", "ServerAliveInterval=30",
        "-o", "ServerAliveCountMax=3",
        "-o", "ExitOnForwardFailure=yes",
        f"{SSH_USER}@{SSH_HOST}"
    ]
    # Start in background, but we keep the Popen object to check status if needed
    # Usage of nohup or similar isn't strictly needed if we run this script as a daemon/service,
    # but here we just spawn it.
    print(f"Starting {tunnel_config['name']} tunnel on port {tunnel_config['local_port']}...")
    return subprocess.Popen(cmd)

def monitor():
    processes = {}
    
    # Clean up start
    for t in TUNNELS:
        kill_process_on_port(t['local_port'])
        
    while True:
        for t in TUNNELS:
            port = t['local_port']
            name = t['name']
            
            # Check if port is listening
            if not is_port_open(port):
                print(f"⚠️  {name} tunnel (port {port}) is DOWN. Restarting...")
                kill_process_on_port(port) # Ensure clean slate
                processes[port] = start_tunnel(t)
                time.sleep(2) # Give it a moment to bind
            else:
                # Optional: Check if the specific process object we spawned is still alive
                # But simple port check is often more robust for 'is it working'
                pass
                
        time.sleep(10)

if __name__ == "__main__":
    print("🚀 Monitoring SSH Tunnels...")
    try:
        monitor()
    except KeyboardInterrupt:
        print("\nStopping monitor...")
