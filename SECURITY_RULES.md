# TSG Platform Security Rules

Bu belge, veritabanı saldırısından (Ransomware) alınan dersler sonucunda projenin kalıcı güvenlik manifestosu olarak hazırlanmıştır. Projeye katkı sağlayan ve kod yazan tüm LLM ajanları (Makineler) ve geliştiriciler bu kuralları ihlal edemez.

## Kural 1: Docker ve UFW İlişkisi (Kesin Kural)
Docker, UFW iptables kural zincirlerini varsayılan olarak atlar. Bir portu "dışarıya kapattım" demek UFW ile yeterli değildir. `docker-compose.yml` içinde arka planda kalması gereken (Public olmayan) hiçbir servis `0.0.0.0`'a veya direkt host'a açılamaz.

**YANLIŞ (Tehlikeli):**
```yaml
ports:
  - "5432:5432" # Tüm dünyaya açılır! UFW bunu engelleyemez.
  - "9000:9000"
```

**DOĞRU (Güvenli):**
```yaml
ports:
  - "127.0.0.1:5432:5432" # Sadece localhost'tan (veya SSH tünelinden) erişilebilir.
  - "127.0.0.1:9000:9000"
```

## Kural 2: Varsayılan Parolalar (Kesin Kural)
Ne olursa olsun, `.env` dosyalarında veya `docker-compose.yml` içinde `postgres`, `admin`, `12345` gibi varsayılan, tahmin edilebilir şifreler kullanılamaz. En az 16 karakterli karmaşık parolalar kullanılmalıdır.
- Kullanıcı isimleri de tahmin edilemez olmalıdır (örn: db_admin_xyz veya proje_adi_admin).

## Kural 3: SSH Tüneli Mimarisi
Geliştirme amacıyla uzaktaki veritabanına bağlanılacaksa, uzak makinenin hiçbir portu dışarıya açılmaz (Kural 1). Bunun yerine lokalde çalışan `start_local.sh` gibi betikler yerel bir kanca (socket) açarak trafiği SSH üzerinden uzak sunucunun `127.0.0.1`'ine yönlendirir.
Örnek komut:
`ssh -N -L 127.0.0.1:5434:127.0.0.1:5432 user@remote_ip`

## Kural 4: Ağ İzolasyonu
Gelecekte Microservice mimarisi eklenirse, servisler birbiriyle Docker'ın dahili ağı üzerinden köprü oluşturarak haberleşir (`networks`). Host'a port açmak GEREKSİZDİR ve sadece Nginx/Caddy gibi dış dünyaya hizmet veren ters vekiller (Reverse Proxies) için 80/443 portlarında uygulanır.

*Last Updated Context: Remote Ransomware DB Wipe Recovery.*
