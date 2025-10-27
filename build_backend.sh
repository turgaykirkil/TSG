#!/usr/bin/env bash
set -euo pipefail
: > build.status || true
/usr/local/bin/docker compose build backend --no-cache && echo BUILD_OK > build.status || echo BUILD_FAIL > build.status
