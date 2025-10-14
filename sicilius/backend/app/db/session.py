"""
Database session management
"""
from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import NullPool

from app.core.config import settings
from app.db.base import Base  # Use the unified Base for all models

# Create database engine
# Convert PostgresDsn to string for checks
DATABASE_URL_STR = str(settings.DATABASE_URL)

# Build connect args
connect_args = {}
if "sqlite" in DATABASE_URL_STR:
    connect_args["check_same_thread"] = False

# Supabase requires SSL; also serverless Postgres benefits from avoiding long-lived pools
is_supabase = ("supabase.co" in DATABASE_URL_STR) or ("supabase" in DATABASE_URL_STR)
if is_supabase and "sslmode=" not in DATABASE_URL_STR:
    # Ensure SSL for psycopg2
    connect_args["sslmode"] = "require"

engine_kwargs = {
    "pool_pre_ping": True,
}

if is_supabase:
    # Avoid stale pooled connections on serverless DBs
    engine_kwargs.update({
        "poolclass": NullPool,
    })
else:
    # Regular pooling for local/managed Postgres
    engine_kwargs.update({
        "pool_recycle": 600,  # Recycle connections more aggressively
        "pool_size": 10,
        "max_overflow": 20,
    })

engine = create_engine(
    DATABASE_URL_STR,
    connect_args=connect_args,
    **engine_kwargs,
)

# Ensure ORM resolves unqualified names to 'app' first on Postgres
if DATABASE_URL_STR.startswith("postgres") or ":5432/" in DATABASE_URL_STR or "supabase" in DATABASE_URL_STR:
    @event.listens_for(engine, "connect")
    def _set_search_path(dbapi_conn, conn_record):
        try:
            cur = dbapi_conn.cursor()
            try:
                cur.execute("SET search_path TO app, public")
            finally:
                cur.close()
        except Exception:
            # Ignore if not a Postgres connection
            pass

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a scoped session
Session = scoped_session(SessionLocal)


def get_db():
    """
    Dependency function to get DB session.
    """
    db = Session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Initialize the database.
    """
    # Import models to ensure they are registered on Base
    from app import models  # noqa: F401
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
