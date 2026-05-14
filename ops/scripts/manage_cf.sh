#!/bin/bash

# Cloudflare Management Script for Sicilius
# Usage: ./manage_cf.sh [check|purge|ssl_strict]

CONFIG_FILE="/Users/turgaykirkil/Apps/TSG_Platform/.cloudflare_config"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ Error: Config file not found at $CONFIG_FILE"
    exit 1
fi

source "$CONFIG_FILE"

API_BASE="https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID"
AUTH_HEADER="Authorization: Bearer $CLOUDFLARE_API_TOKEN"

case "$1" in
    check)
        echo "📡 Checking Cloudflare Connection..."
        curl -s -X GET "$API_BASE" -H "$AUTH_HEADER" -H "Content-Type: application/json" | python3 -c "import sys, json; r=json.load(sys.stdin); print('✅ Connected to ' + r['result']['name']) if r['success'] else print('❌ Failed: ' + r['errors'][0]['message'])"
        ;;
    purge)
        echo "🧹 Purging Cloudflare Cache..."
        curl -s -X POST "$API_BASE/purge_cache" \
             -H "$AUTH_HEADER" \
             -H "Content-Type: application/json" \
             --data '{"purge_everything":true}' | python3 -c "import sys, json; r=json.load(sys.stdin); print('✅ Cache Purged Successfully!') if r['success'] else print('❌ Purge Failed: ' + r['errors'][0]['message'])"
        ;;
    ssl_strict)
        echo "🔒 Setting SSL Mode to Full (Strict)..."
        curl -s -X PATCH "$API_BASE/settings/ssl" \
             -H "$AUTH_HEADER" \
             -H "Content-Type: application/json" \
             --data '{"value":"strict"}' | python3 -c "import sys, json; r=json.load(sys.stdin); print('✅ SSL Set to Strict!') if r['success'] else print('❌ SSL Update Failed: ' + r['errors'][0]['message'])"
        ;;
    *)
        echo "Usage: $0 {check|purge|ssl_strict}"
        exit 1
        ;;
esac
