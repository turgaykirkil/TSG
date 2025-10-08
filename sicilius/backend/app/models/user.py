from sqlalchemy import Column, String, Boolean, Enum, DateTime, func, Integer, BigInteger
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship

from app.db.base import Base
import enum

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"

class User(Base):
    __tablename__ = "app_users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100))
    is_active = Column(Boolean(), default=True)
    is_banned = Column(Boolean(), default=False)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    last_login = Column(DateTime(timezone=True))
    # Single-session enforcement: store latest accepted token iat (epoch seconds)
    latest_session_iat = Column(BigInteger, nullable=True)
    
    # Relationships
    file_uploads = relationship("FileUpload", back_populates="uploaded_by")
    job_histories = relationship("JobHistory", back_populates="user")
    
    def __repr__(self):
        return f"<User {self.email}>"
    
    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN
    
    @property
    def is_manager(self):
        return self.role in [UserRole.ADMIN, UserRole.MANAGER]
