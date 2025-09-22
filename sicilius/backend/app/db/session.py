"""
Database session management
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from app.core.config import settings
from app.db.base import Base  # Use the unified Base for all models

# Create database engine
# Convert PostgresDsn to string for SQLite check
DATABASE_URL_STR = str(settings.DATABASE_URL)

engine = create_engine(
    DATABASE_URL_STR,
    pool_pre_ping=True,
    pool_recycle=1800,  # Recycle connections every 30 minutes
    pool_size=10,         # Default is 5
    max_overflow=20,      # Default is 10
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL_STR else {}
)

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
