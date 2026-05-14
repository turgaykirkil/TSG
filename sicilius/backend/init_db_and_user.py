import sys
import psycopg2
from alembic.config import Config
from alembic import command

# 1. Clean up and provide extensions
conn = psycopg2.connect("postgresql://sicilius:uqN6_J8bWpT2_YzXkR_3mS@127.0.0.1:5434/sicilius")
conn.autocommit = True
cur = conn.cursor()
cur.execute("DROP SCHEMA IF EXISTS app CASCADE;")
cur.execute("DROP TYPE IF EXISTS userrole CASCADE;")
cur.execute("DROP TYPE IF EXISTS gazettetype CASCADE;")
cur.execute("CREATE SCHEMA IF NOT EXISTS app;")
cur.execute("CREATE EXTENSION IF NOT EXISTS postgis;")
cur.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")
cur.execute("""
CREATE OR REPLACE FUNCTION tr_normalize(original_text text)
RETURNS text AS $$
DECLARE
    normalized_text text;
BEGIN
    IF original_text IS NULL THEN
        RETURN NULL;
    END IF;
    normalized_text := lower(original_text);
    normalized_text := replace(normalized_text, 'ı', 'i');
    normalized_text := replace(normalized_text, 'ğ', 'g');
    normalized_text := replace(normalized_text, 'ü', 'u');
    normalized_text := replace(normalized_text, 'ş', 's');
    normalized_text := replace(normalized_text, 'ö', 'o');
    normalized_text := replace(normalized_text, 'ç', 'c');
    normalized_text := replace(normalized_text, 'â', 'a');
    normalized_text := replace(normalized_text, 'î', 'i');
    RETURN normalized_text;
END;
$$ LANGUAGE plpgsql IMMUTABLE;
""")
conn.close()
print("Extensions and functions created.")

# 2. Let FastAPI create the model tables perfectly
from app.db.base import init_db
init_db()

# 3. Stamp Alembic so future migrations don't break
try:
    alembic_cfg = Config("alembic.ini")
    command.stamp(alembic_cfg, "head")
    print("Alembic stamped to head.")
except Exception as e:
    print(f"Alembic stamp failed (safe to ignore for now): {e}")

# 4. Create the Admin User
from app.db.session import SessionLocal
from app.crud.crud_user import user as user_crud
from app.schemas.user import UserCreate

db = SessionLocal()
u = user_crud.get_by_email(db, email="turgaykirkil@me.com")
if not u:
    user_crud.create(db, obj_in=UserCreate(email="turgaykirkil@me.com", password="Sicilius2024!", is_superuser=True))
    print("\n----------------\nUSER CREATED SUCCESSFULLY.\n----------------")
else:
    print("\n----------------\nUSER ALREADY EXISTS.\n----------------")
