from typing import Optional, List, Dict, Any
from datetime import datetime, date
from pydantic import BaseModel, Field

class CheckInRequest(BaseModel):
    customer_id: str = Field(description="Ziyaret edilen müşteri ID'si")
    latitude: float = Field(description="Temsilcinin anlık GPS enlemi")
    longitude: float = Field(description="Temsilcinin anlık GPS boylamı")
    note_text: Optional[str] = Field(None, description="Metinsel ziyaret özeti")
    ocr_data_json: Optional[Dict[str, Any]] = Field(None, description="Cihazda OCR ile okunan metinsel veriler (VKN, unvan vb.)")

class CheckInResponse(BaseModel):
    success: bool
    message: str
    xp_gained: int
    total_xp: int
    streak_days: int
    streak_multiplier: float
    distance_meters: float
    badges_unlocked: List[str] = []

class CoordinateCorrectionRequest(BaseModel):
    company_id: str = Field(description="Konumu düzeltilecek şirket ID'si")
    verified_lat: float = Field(description="Doğrulanan enlem")
    verified_lon: float = Field(description="Doğrulanan boylam")

class CoordinateCorrectionResponse(BaseModel):
    success: bool
    message: str
    xp_gained: int
    total_xp: int

class LeaderboardRankItem(BaseModel):
    rank: int
    anonymous_label: str
    xp: int
    is_current_user: bool = False

class PrivacyLeaderboardResponse(BaseModel):
    my_rank: int
    my_xp: int
    my_league: str
    percentile_text: str
    rankings: List[LeaderboardRankItem]

class BadgeItem(BaseModel):
    code: str
    title: str
    description: str
    icon: str
    category: str
    is_unlocked: bool
    unlocked_at: Optional[str] = None

class DailyQuestItem(BaseModel):
    id: str
    title: str
    quest_type: str
    target_count: int
    current_progress: int
    xp_reward: int
    is_completed: bool

class UserGamificationProfile(BaseModel):
    xp_points: int
    current_level: int
    current_league: str
    streak_days: int
    next_level_xp: int
    badges_count: int
    quests_completed_today: int
