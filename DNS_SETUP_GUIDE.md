# DNS Configuration for MinIO Subdomain

## Required DNS Records

Add these records in your Cloudflare dashboard:

### Record 1: MinIO Console

| Setting | Value |
|---------|-------|
| Type | CNAME |
| Name | `minio` |
| Target | `turgaysicil.com` (or your server's IP if A record) |
| Proxy status | ☁️ Proxied (Orange Cloud) |
| TTL | Auto |

### Record 2: MinIO S3 API

| Setting | Value |
|---------|-------|
| Type | CNAME |
| Name | `s3` |
| Target | `turgaysicil.com` (or your server's IP if A record) |
| Proxy status | ☁️ Proxied (Orange Cloud) |
| TTL | Auto |

## Alternative: A Records (if CNAME doesn't work)

If you prefer A records pointing directly to your server's public IP:

### Get your public IP first:
```bash
ssh nalanmerci@192.168.1.5 "curl -s ifconfig.me"
```

Then create these records:

| Type | Name | IPv4 Address | Proxy |
|------|------|--------------|-------|
| A | `minio` | [YOUR_PUBLIC_IP] | ☁️ Proxied |
| A | `s3` | [YOUR_PUBLIC_IP] | ☁️ Proxied |

## Steps to Add in Cloudflare

1. **Login:** https://dash.cloudflare.com
2. **Select Domain:** `turgaysicil.com`
3. **Go to DNS:** Left sidebar → DNS → Records
4. **Click "Add record"**
5. **Fill in details from table above**
6. **Save**
7. **Repeat for second record**

## Verification

After adding records, wait 1-2 minutes, then test:

```bash
# Check DNS resolution
nslookup minio.turgaysicil.com
nslookup s3.turgaysicil.com
```

Both should show your server's IP.

## What Happens Next

Once DNS records are added:
1. Caddy will automatically detect the domain is resolvable
2. Caddy will obtain SSL certificates from Let's Encrypt  
3. HTTPS will become available for both subdomains
4. You can then update local backend .env and start using MinIO

## Current Status

✅ Caddy configuration updated
✅ Caddy container restarted  
⏳ Waiting for DNS records
❌ SSL certificates pending (normal - needs DNS first)

## Check Progress

After adding DNS, monitor Caddy logs:

```bash
ssh nalanmerci@192.168.1.5 'export PATH=$PATH:/opt/homebrew/bin && docker logs sicilius-caddy --tail 50'
```

Look for messages like:
- `certificate obtained successfully`
- `tls: got certificate`
