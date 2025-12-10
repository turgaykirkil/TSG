# Backend Configuration Update

After DNS is configured and SSL certificates are obtained, update your local backend environment:

## File to Edit

`sicilius/backend/.env`

## Changes Required

Find these lines:
```bash
MINIO_ENDPOINT=localhost:9000
MINIO_USE_SSL=false
```

**Replace with:**
```bash
MINIO_ENDPOINT=s3.turgaysicil.com:443
MINIO_USE_SSL=true
```

## Keep These Unchanged

```bash
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=ChangeMe_12345
MINIO_BUCKET_GAZETTE_PDFS=gazette-pdfs
MINIO_BUCKET_COMPANY_GAZETTES=company-gazettes
```

## After Making Changes

Restart your backend service:

```bash
# In terminal running uvicorn, press Ctrl+C
# Then restart:
cd sicilius/backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 5001
```

## Verify It Works

1. **Check logs** - should see no MinIO connection errors
2. **Admin panel** - http://localhost:3000/admin/usage should show 255 files
3. **Scraping** - should save PDFs without errors
4. **OCR app** - should read PDFs from storage successfully

## If Problems Occur

Check backend logs for connection errors. Common issues:

**Connection refused:**
- DNS not propagated yet - wait a few more minutes
- SSL cert not ready - check Caddy logs

**Authentication failed:**
- Wrong credentials in .env
- Check docker-compose.yml for correct MinIO credentials

**Timeout:**
- Firewall blocking ports 80/443
- Server not accessible from internet
