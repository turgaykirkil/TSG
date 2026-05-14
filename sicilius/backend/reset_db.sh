#!/bin/bash
set -e

echo "1. Localdeki eski dosyaları siliyoruz..."
rm -rf app/db/migrations/versions/*

echo "2. Düzeltilmiş company.py dosyasını sunucuya gönderiyoruz..."
rsync -avz -e "ssh -o StrictHostKeyChecking=no" app/models/company.py ubuntu@89.252.153.102:~/sicilius/backend/app/models/company.py

echo "3. Sunucudaki eski migration dosyalarını siliyoruz..."
ssh ubuntu@89.252.153.102 "rm -rf ~/sicilius/backend/app/db/migrations/versions/*"
ssh ubuntu@89.252.153.102 "sudo docker exec -u root sicilius-backend-1 sh -c 'rm -rf /app/app/db/migrations/versions/*'"

echo "4. Container içindeki company.py dosyasını güncelliyoruz ve izinlerini düzeltiyoruz..."
ssh ubuntu@89.252.153.102 "sudo docker cp ~/sicilius/backend/app/models/company.py sicilius-backend-1:/app/app/models/company.py && sudo docker exec -u root sicilius-backend-1 chmod 777 /app/app/models/company.py"

echo "5. Veritabanını sıfırlıyoruz..."
ssh ubuntu@89.252.153.102 "sudo docker exec sicilius-db-1 psql -U postgres -d sicilius -c 'DROP SCHEMA IF EXISTS app CASCADE; CREATE SCHEMA app;'"

echo "6. tr_normalize fonksiyonunu veritabanına ekliyoruz..."
ssh ubuntu@89.252.153.102 "sudo docker cp ~/sicilius/backend/create_func.sql sicilius-db-1:/tmp/create_func.sql && sudo docker exec sicilius-db-1 psql -U postgres -d sicilius -f /tmp/create_func.sql"

echo "7. Yeni, tek parça migration oluşturuluyor..."
ssh ubuntu@89.252.153.102 "sudo docker exec sicilius-backend-1 python -m alembic revision --autogenerate -m 'Initial schema setup'"

echo "8. geoalchemy2 import'u ekleniyor ve çakışan indeks komutu temizleniyor..."
ssh ubuntu@89.252.153.102 "sudo docker exec sicilius-backend-1 sh -c 'for f in /app/app/db/migrations/versions/*.py; do echo \"import geoalchemy2\" | cat - \"\$f\" > /tmp/temp.py && mv /tmp/temp.py \"\$f\"; sed -i \"/idx_companies_koordinat/d\" \"\$f\"; done'"

echo "9. Veritabanına uygulanıyor (Upgrade Head)..."
ssh ubuntu@89.252.153.102 "sudo docker exec sicilius-backend-1 python -m alembic upgrade head 2>&1"

echo "10. Başarılı migration dosyası lokale çekiliyor..."
ssh ubuntu@89.252.153.102 "sudo docker cp sicilius-backend-1:/app/app/db/migrations/versions/. ~/sicilius/backend/app/db/migrations/versions/"
rsync -avz -e "ssh -o StrictHostKeyChecking=no" ubuntu@89.252.153.102:~/sicilius/backend/app/db/migrations/versions/ app/db/migrations/versions/

echo "Tüm işlemler BAŞARIYLA TAMAMLANDI!"
