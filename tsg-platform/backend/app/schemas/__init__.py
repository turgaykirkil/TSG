"""
TSG Araştırma Platformu - Şemalar
"""

# Bu dosya, tüm şema sınıflarını içe aktarır.
# Bu sayede diğer modüllerden kolayca erişilebilir.

from .token import Token, TokenPayload
from .user import User, UserCreate, UserInDB, UserUpdate
from .company import Company, CompanyCreate, CompanyUpdate, CompanyInDB
from .gazette import Gazette, GazetteCreate, GazetteUpdate, GazetteInDB
from .gazette_entry import GazetteEntry, GazetteEntryCreate, GazetteEntryUpdate, GazetteEntryInDB
from .person import Person, PersonCreate, PersonUpdate, PersonInDB
from .relation import CompanyPersonRelation, CompanyPersonRelationCreate, CompanyPersonRelationUpdate, CompanyPersonRelationInDB
from .file_upload import FileUpload, FileUploadCreate, FileUploadUpdate, FileUploadInDB
from .job_history import JobHistory, JobHistoryCreate, JobHistoryUpdate, JobHistoryInDB
from .company_scrape import (
    CompanyScrape, CompanyScrapeCreate, CompanyScrapeUpdate, CompanyScrapeInDB,
)

from .job_history_process import (
    JobResultSummary,
    JobProgressUpdate,
    JobStartRequest,
    JobUpdateRequest,
    JobFilter,
    JobStats,
    JobStatusResponse
)
from .msg import Msg

__all__ = [
    'Token', 'TokenPayload',
    'User', 'UserCreate', 'UserInDB', 'UserUpdate',
    'Company', 'CompanyCreate', 'CompanyUpdate', 'CompanyInDB',
    'Gazette', 'GazetteCreate', 'GazetteUpdate', 'GazetteInDB',
    'GazetteEntry', 'GazetteEntryCreate', 'GazetteEntryUpdate', 'GazetteEntryInDB',
    'Person', 'PersonCreate', 'PersonUpdate', 'PersonInDB',
    'CompanyPersonRelation', 'CompanyPersonRelationCreate', 'CompanyPersonRelationUpdate', 'CompanyPersonRelationInDB',
    'FileUpload', 'FileUploadCreate', 'FileUploadUpdate', 'FileUploadInDB',
    'JobHistory', 'JobHistoryCreate', 'JobHistoryUpdate', 'JobHistoryInDB',
    'CompanyScrape', 'CompanyScrapeCreate', 'CompanyScrapeUpdate', 'CompanyScrapeInDB',
    'JobResultSummary', 'JobProgressUpdate', 'JobStartRequest', 'JobUpdateRequest',
    'JobFilter', 'JobStats', 'JobStatusResponse',
    'Msg',
]
