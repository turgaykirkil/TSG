from sqlalchemy import Column, String, Boolean, Enum, DateTime, func
from sqlalchemy.orm import relationship

from app.models.base import Base
import enum

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"

class User(Base):
    __tablename__ = "users"
    
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100))
    is_active = Column(Boolean(), default=True)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    last_login = Column(DateTime(timezone=True))
    
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
