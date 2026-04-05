#!/bin/bash

LOG_FILE="system_logs.md"
MAX_LINES=10000

# Eski log dosyasının 10.000 satırdan fazlasını silerek dosyanın sonsuza dek büyümesini engelliyoruz.
if [ -f "$LOG_FILE" ]; then
    # Son MAX_LINES kadarını tutup temizliyoruz
    tail -n $MAX_LINES "$LOG_FILE" > "${LOG_FILE}.tmp" && mv "${LOG_FILE}.tmp" "$LOG_FILE"
    echo -e "\n\n---\n**YENİ OTURUM BAŞLADI:** $(date)\n---\n" >> "$LOG_FILE"
else
    echo "# Sicilius Tüm Servis Logları" > "$LOG_FILE"
    echo -e "\n**OTURUM BAŞLADI:** $(date)\n---\n" >> "$LOG_FILE"
fi

echo "Tüm servisler (Frontend, Uvicorn Backend, Celery ve Docling) tek terminalde başlatılıyor..."
echo "Kapatmak için CTRL+C tuşlarına basmanız yeterlidir."
echo "Tüm loglar anlık olarak $LOG_FILE dosyasına, maksimum $MAX_LINES satır kalacak şekilde kaydediliyor."

# --timestamp-format ve --prefix özellikleri ile tarih saat basıyoruz.
# | tee -a komutuyla çıktıları hem ekranda gösteriyor hem de md dosyasına anlık yazıyoruz.
npx concurrently \
  --timestamp-format "yyyy-MM-dd HH:mm:ss" \
  --prefix "[{time}] [{name}]" \
  -c "bgBlue.bold,bgGreen.bold,bgMagenta.bold,bgYellow.bold" \
  -n "FRONTEND,BACKEND,CELERY,DOCLING" \
  "cd frontend && yarn dev" \
  "./run_backend.sh" \
  "cd backend && celery -A app.core.celery_app worker -l info --pool=solo" \
  "cd backend && opendataloader-pdf-hybrid --port 5002" 2>&1 | tee -a "$LOG_FILE"
