#!/usr/bin/env python3
"""
Veritabanını gerekli tablolar ve başlangıç verileriyle başlatır.
"""
import os
import sys
from pathlib import Path

# Uygulama modüllerini import edebilmek için üst dizini yola ekle
sys.path.append(str(Path(__file__).parent.parent))

from app.db.base import init_db, SessionLocal, Base, engine
from app.core.config import settings
from app.models import (
    User, Company, Gazette, GazetteEntry, Person, 
    CompanyPersonRelation, FileUpload, JobHistory
)
from app.core.security import get_password_hash

def create_initial_data(db):
    """Uygulama için başlangıç verilerini oluşturur."""
    # Admin kullanıcısını oluştur (eğer yoksa)
    admin = db.query(User).filter(User.email == "admin@tsg.com").first()
    if not admin:
        admin_user = User(
            email="admin@tsg.com",
            hashed_password=get_password_hash("changeme"),
            full_name="Admin User",
            role="admin",
            is_active=True
        )
        db.add(admin_user)
        db.commit()
        print("Admin kullanıcısı oluşturuldu")
    
    # Diğer başlangıç verilerini ekle
    # ...

def main():
    print("Veritabanı başlatılıyor...")
    
    # Tüm tabloları oluştur
    Base.metadata.create_all(bind=engine)
    
    # Başlangıç verilerini oluştur
    db = SessionLocal()
    try:
        create_initial_data(db)
        print("Veritabanı başarıyla başlatıldı!")
    except Exception as e:
        print(f"Veritabanı başlatılırken hata oluştu: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()
