#!/usr/bin/env python3
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # .../TSG_Platform
BACKEND_ENV = ROOT / "sicilius" / "backend" / ".env"
TARGET_ENV = Path(__file__).resolve().parent / ".env.backend"

KEYS = [
    "TSG_DATABASE_URL",
    "TSG_SUPABASE_URL",
    "TSG_SUPABASE_KEY",
    "TSG_SUPABASE_SERVICE_ROLE_KEY",
    "TSG_LOCATIONIQ_TOKEN",
]

# Simple .env parser (key=value), keeps quotes if present
env_line_re = re.compile(r"^\s*([A-Za-z0-9_]+)\s*=\s*(.*)\s*$")

def read_env(path: Path) -> dict:
    data = {}
    if not path.exists():
        return data
    for line in path.read_text(encoding="utf-8").splitlines():
        m = env_line_re.match(line)
        if not m:
            continue
        k, v = m.group(1), m.group(2)
        data[k] = v
    return data

def write_env(path: Path, data: dict, order_hint: list[str]):
    # Preserve order by using order_hint first, then others
    lines = []
    used = set()
    for k in order_hint:
        if k in data:
            lines.append(f"{k}={data[k]}")
            used.add(k)
    for k, v in data.items():
        if k not in used:
            lines.append(f"{k}={v}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")

src = read_env(BACKEND_ENV)
if not src:
    raise SystemExit(f"Source env not found or empty: {BACKEND_ENV}")

dst = read_env(TARGET_ENV)

# Ensure mandatory prod flags
dst["TSG_API_ONLY"] = dst.get("TSG_API_ONLY", "true")
dst["TSG_ENVIRONMENT"] = "production"
# keep existing CORS if present

# Copy secrets without printing them
for k in KEYS:
    if k in src:
        dst[k] = src[k]

write_env(TARGET_ENV, dst, order_hint=[
    "TSG_API_ONLY","TSG_ENVIRONMENT","TSG_SECURE_COOKIE","TSG_CORS_ORIGINS",
    *KEYS,
])
