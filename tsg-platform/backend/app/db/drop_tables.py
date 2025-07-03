import os
import sys

# Proje kök dizinini path'e ekle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.db.base import Base, engine
from app.db import base  # noqa: F401 - Tüm modellerin import edilmesini sağlar

def drop_all_tables():
    print("Mevcut tüm tablolar kaldırılıyor...")
    try:
        from sqlalchemy import text

        with engine.connect() as connection:
            connection.execute(text('DROP TABLE IF EXISTS alembic_version;'))
            connection.commit()
        print("'alembic_version' tablosu başarıyla kaldırıldı (veya mevcut değildi).")

        Base.metadata.drop_all(bind=engine)
        print("Tüm tablolar başarıyla kaldırıldı.")
    except Exception as e:
        print(f"Tablolar kaldırılırken bir hata oluştu: {e}")

if __name__ == "__main__":
    drop_all_tables()
