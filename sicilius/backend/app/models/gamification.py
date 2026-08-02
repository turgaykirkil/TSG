import uuid
from datetime import datetime, date
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Float, Date, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.db.session import Base

class UserGamificationStats(Base):
    __tablename__ = "user_gamification_stats"
    __table_args__ = {"schema": "app"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), index=True, nullable=False, unique=True)
    xp_points = Column(Integer, default=0, nullable=False)
    streak_days = Column(Integer, default=0, nullable=False)
    last_checkin_date = Column(Date, nullable=True)
    current_league = Column(String(50), default="Bronz Ligi", nullable=False)
    current_level = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class XPAuditLog(Base):
    __tablename__ = "xp_audit_logs"
    __table_args__ = {"schema": "app"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), index=True, nullable=False)
    action_type = Column(String(100), nullable=False)
    points_awarded = Column(Integer, nullable=False)
    metadata_json = Column(JSONB, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Badge(Base):
    __tablename__ = "badges"
    __table_args__ = {"schema": "app"}

    code = Column(String(50), primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)
    icon = Column(String(10), nullable=False)
    category = Column(String(50), nullable=False)
    threshold_count = Column(Integer, default=1)

class UserBadge(Base):
    __tablename__ = "user_badges"
    __table_args__ = {"schema": "app"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), index=True, nullable=False)
    badge_code = Column(String(50), ForeignKey("app.badges.code"), nullable=False)
    unlocked_at = Column(DateTime, default=datetime.utcnow)

class UserDailyQuest(Base):
    __tablename__ = "user_daily_quests"
    __table_args__ = {"schema": "app"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), index=True, nullable=False)
    quest_title = Column(String(255), nullable=False)
    quest_type = Column(String(50), nullable=False)
    target_count = Column(Integer, default=1, nullable=False)
    current_progress = Column(Integer, default=0, nullable=False)
    xp_reward = Column(Integer, default=50, nullable=False)
    is_completed = Column(Boolean, default=False, nullable=False)
    assigned_date = Column(Date, default=date.today, nullable=False)
