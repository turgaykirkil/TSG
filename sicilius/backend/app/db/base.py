from sqlalchemy import create_engine, Column, Integer, DateTime, func, MetaData
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
import os

from app.core.config import settings

# Create database engine
SQLALCHEMY_DATABASE_URL = str(settings.DATABASE_URL)  # PostgresDsn'yi string'e çevir

# SQLite için özel bağlantı argümanları
if "sqlite" in SQLALCHEMY_DATABASE_URL:
    connect_args = {"check_same_thread": False}
else:
    connect_args = {}

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a scoped session factory
Session = scoped_session(SessionLocal)

# Base class for all models
class CustomBase:
    # Tablo adını otomatik olarak sınıf adının çoğul hali yapar (örn: User -> users)
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + "s"


    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

# Ana Base'imizi, ortak sütunları içeren CustomBase'den türetiyoruz
Base = declarative_base(cls=CustomBase, metadata=MetaData(schema="app"))

def get_db():
    """Dependency for getting database session"""
    db = Session()
    try:
        yield db
    finally:
        db.close()

@contextmanager
def get_db_session():
    """Context manager for database sessions"""
    db = Session()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def init_db():
    """Initialize the database"""
    # Import all models here to ensure they are registered with SQLAlchemy
    from app.models import (
        User, Company, Gazette, GazetteEntry, Person, 
        CompanyPersonRelation, FileUpload, JobHistory, Announcement, CompanyError,
        ContactMessage
    )
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    print("Database initialized successfully")

# For testing
def get_test_db():
    """Get a test database session"""
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    
    TEST_SQLALCHEMY_DATABASE_URL = settings.TEST_DATABASE_URL
    test_engine = create_engine(
        TEST_SQLALCHEMY_DATABASE_URL, 
        connect_args={"check_same_thread": False} if "sqlite" in TEST_SQLALCHEMY_DATABASE_URL else {}
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    
    # Create all tables for testing
    Base.metadata.create_all(bind=test_engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Clean up test database after tests
        Base.metadata.drop_all(bind=test_engine)
