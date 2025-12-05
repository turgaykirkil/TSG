from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
import sys

# Model tanımlarını ekleyin
sys.path.append(os.getcwd())
from app.db.base import Base  # Doğru Base objesini import et

# Modellerin Alembic tarafından tanınması için import edilmesi gerekiyor
from app.models.user import User
from app.models.company import Company
from app.models.announcement import Announcement
from app.models.gazette import Gazette, GazetteEntry
from app.models.person import Person
from app.models.relation import CompanyPersonRelation
from app.models.file_upload import FileUpload
from app.models.job_history import JobHistory
from app.models.company_error import CompanyError
from app.models.app_setting import AppSetting
from app.models.ocr_result import OcrResult
from app.models.incoming_email import IncomingEmail
from app.models.daily_usage import DailyUsage
from app.models.user_invite import UserInvite

# Alembic Config yapılandırması
config = context.config

# .env dosyasından veritabanı URL'sini dinamik olarak yükle
from app.core.config import get_settings
settings = get_settings()
config.set_main_option('sqlalchemy.url', str(settings.DATABASE_URL))

# Logging yapılandırması
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadataları al
target_metadata = Base.metadata

def include_object(object, name, type_, reflected, compare_to):
    if type_ == "table":
        if name == "spatial_ref_sys":
            return False
        # Exclude tables that don't have models yet
        if name in [
            "addresses_history", "company_trade_names", 
            "ocr_address_mentions", "ocr_id_mentions", 
            "ocr_person_mentions", "live_stats"
        ]:
            return False
    return True

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=True,
        version_table_schema='app'
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            compare_type=True,
            include_object=include_object,
            include_schemas=True,
            version_table_schema='app'
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()