#!/bin/bash
# Cloudflare Tunnel Kurulum Scripti
# Kullanım: ./setup_tunnel.sh

# Cloudflared kurulu mu?
if ! command -v cloudflared &> /dev/null; then
    echo "☁️ Cloudflared bulunamadı. Brew ile kuruluyor..."
    # Intel Mac / Apple Silicon ayrımı gerekebilir ama brew halleder
    brew install cloudflare/cloudflare/cloudflared
else
    echo "✅ Cloudflared zaten kurulu."
fi

echo "🔑 Cloudflare Girişi (Login)..."
echo "Lütfen açılan tarayıcı penceresinden (veya linkten) giriş yapın."
cloudflared tunnel login

echo "
✅ Giriş işlemi tamamlandıktan sonra yapılması gerekenler:

1. Tünel Oluşturma:
   cloudflared tunnel create sicilius-tunnel

2. DNS Yönlendirme:
   cloudflared tunnel route dns sicilius-tunnel sicilius.com.tr
   cloudflared tunnel route dns sicilius-tunnel api.sicilius.com.tr

3. Config Dosyası (~/.cloudflared/config.yml):
   tunnel: <TUNNEL_UUID>
   credentials-file: /Users/nalanmerci/.cloudflared/<TUNNEL_UUID>.json
   ingress:
     - hostname: sicilius.com.tr
       service: http://localhost:3000
     - hostname: api.sicilius.com.tr
       service: http://localhost:5001
     - service: http_status:404

4. Tüneli Başlatma:
   cloudflared tunnel run sicilius-tunnel
"
