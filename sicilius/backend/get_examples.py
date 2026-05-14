import sys
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = "postgresql://sicilius:Kr6_vP9_Xz2_Nb7_Qj1_Sm@127.0.0.1:5434/sicilius"
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session()

# SQLAlchemy Core to execute raw SQL easily
from sqlalchemy import text

def get_examples():
    print("--- 10 RISKLI FIRMA ---")
    
    # Riskli Firmalar (Tasfiye, İflas gibi kelimeler geçenler)
    risky_sql = text("""
        SELECT id, unvan FROM companies 
        WHERE unvan ILIKE '%TASFİYE%' 
           OR unvan ILIKE '%İFLAS%' 
           OR unvan ILIKE '%KONKORDATO%'
        LIMIT 10;
    """)
    risky_results = session.execute(risky_sql).fetchall()
    
    # Eğer eksikse rastgele risk flagli bulalım (tabi taglere bakılarak)
    if not risky_results:
        risky_sql_fallback = text("""
            SELECT c.id, c.unvan FROM companies c
            JOIN announcements a ON c.id = a.company_id
            WHERE a.announcement_type ILIKE '%TASFİYE%' 
               OR a.announcement_type ILIKE '%İFLAS%'
            LIMIT 10;
        """)
        risky_results = session.execute(risky_sql_fallback).fetchall()
        
    for r in risky_results:
         print(f"- {r[1]}")
         
    print("\n--- 10 TEMIZ FIRMA ---")
    clean_sql = text("""
        SELECT id, unvan FROM companies 
        WHERE unvan NOT ILIKE '%TASFİYE%' 
          AND unvan NOT ILIKE '%İFLAS%' 
          AND is_active = true
        LIMIT 10;
    """)
    clean_results = session.execute(clean_sql).fetchall()
    for c in clean_results:
         print(f"- {c[1]}")

if __name__ == "__main__":
    get_examples()
