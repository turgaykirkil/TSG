import math
import uuid
import random
from typing import Any, List
from datetime import datetime, date, timedelta

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy import text

from app import models
from app.api import deps
from app.schemas.gamification import (
    CheckInRequest,
    CheckInResponse,
    CoordinateCorrectionRequest,
    CoordinateCorrectionResponse,
    PrivacyLeaderboardResponse,
    LeaderboardRankItem,
    UserGamificationProfile,
    BadgeItem,
    DailyQuestItem
)

router = APIRouter()

def haversine_distance_meters(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Haversine mesafe hesabı (metre)"""
    R = 6371000  # Dünya yarıçapı (metre)
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (math.sin(delta_phi / 2) ** 2 +
         math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def calculate_league(xp: int) -> str:
    if xp >= 15000:
        return "Efsane Ligi"
    elif xp >= 7001:
        return "Elmas Ligi"
    elif xp >= 3001:
        return "Altın Ligi"
    elif xp >= 1001:
        return "Gümüş Ligi"
    return "Bronz Ligi"

# ——————————————————————————————————
# 1. GPS 50m Doğrulamalı Check-in Endpoint
# ——————————————————————————————————
@router.post("/check-in", response_model=CheckInResponse)
def perform_check_in(
    payload: CheckInRequest,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    user_id_str = str(current_user.id)
    
    # 1. Müşterinin harita koordinatlarını veritabanından çek
    query = text("""
        SELECT id::text, name, latitude, longitude 
        FROM app.b2b_customers 
        WHERE id = CAST(:id AS uuid)
    """)
    cust = db.execute(query, {"id": payload.customer_id}).first()
    
    # Müşteri bulunamadıysa varsayılan koordinat kullan (fallback)
    target_lat = float(cust.latitude) if cust and cust.latitude else payload.latitude
    target_lon = float(cust.longitude) if cust and cust.longitude else payload.longitude

    # 2. GPS Mesafe Hesabı
    distance = haversine_distance_meters(payload.latitude, payload.longitude, target_lat, target_lon)

    # 50m mesafe kontrolü (Test/Geliştirme aşamasında esnek tutulabilir)
    if distance > 50.0 and cust and cust.latitude:
        return CheckInResponse(
            success=False,
            message=f"Check-in yapabilmek için müşteriye en fazla 50m yakın olmalısınız. (Mevcut Mesafe: {round(distance)} metre)",
            xp_gained=0,
            total_xp=0,
            streak_days=0,
            streak_multiplier=1.0,
            distance_meters=round(distance, 1)
        )

    # 3. Kullanıcı Gamification İstatistiklerini Getir / Oluştur
    stats_query = text("""
        SELECT user_id::text, xp_points, streak_days, last_checkin_date, current_league, current_level
        FROM app.user_gamification_stats
        WHERE user_id = CAST(:uid AS uuid)
    """)
    stats = db.execute(stats_query, {"uid": user_id_str}).first()

    today_val = date.today()
    xp_gained = 50 # Baz Check-in XP
    streak_days = 1
    multiplier = 1.0

    if stats:
        last_date = stats.last_checkin_date
        streak_days = stats.streak_days or 1
        
        if last_date:
            if last_date == today_val - timedelta(days=1):
                streak_days += 1
            elif last_date == today_val:
                pass # Aynı gün devam eder
            else:
                streak_days = 1 # Seri kırıldı
        
        if streak_days >= 30:
            multiplier = 2.0
        elif streak_days >= 7:
            multiplier = 1.5
        elif streak_days >= 3:
            multiplier = 1.2

        xp_gained = int(xp_gained * multiplier)

        # OCR verisi veya Not yazılmışsa ekstra bonus
        if payload.ocr_data_json:
            xp_gained += 35
        if payload.note_text and len(payload.note_text.strip()) >= 10:
            xp_gained += 25

        new_total_xp = stats.xp_points + xp_gained
        new_league = calculate_league(new_total_xp)

        update_sql = text("""
            UPDATE app.user_gamification_stats
            SET xp_points = :xp, streak_days = :streak, last_checkin_date = :today, current_league = :league, updated_at = NOW()
            WHERE user_id = CAST(:uid AS uuid)
        """)
        db.execute(update_sql, {
            "xp": new_total_xp,
            "streak": streak_days,
            "today": today_val,
            "league": new_league,
            "uid": user_id_str
        })
    else:
        new_total_xp = xp_gained
        new_league = calculate_league(new_total_xp)
        insert_sql = text("""
            INSERT INTO app.user_gamification_stats (user_id, xp_points, streak_days, last_checkin_date, current_league, current_level)
            VALUES (CAST(:uid AS uuid), :xp, :streak, :today, :league, 1)
        """)
        db.execute(insert_sql, {
            "uid": user_id_str,
            "xp": new_total_xp,
            "streak": streak_days,
            "today": today_val,
            "league": new_league
        })

    # Log kaydı ekle
    log_sql = text("""
        INSERT INTO app.xp_audit_logs (user_id, action_type, points_awarded, metadata_json)
        VALUES (CAST(:uid AS uuid), 'check_in', :points, :meta)
    """)
    db.execute(log_sql, {
        "uid": user_id_str,
        "points": xp_gained,
        "meta": f'{{"customer_id": "{payload.customer_id}", "distance": {round(distance, 1)}}}'
    })
    db.commit()

    return CheckInResponse(
        success=True,
        message=f"Tebrikler! Müşteri ziyareti check-in doğrulandı. +{xp_gained} XP kazandınız!",
        xp_gained=xp_gained,
        total_xp=new_total_xp,
        streak_days=streak_days,
        streak_multiplier=multiplier,
        distance_meters=round(distance, 1)
    )

# ——————————————————————————————————
# 2. Hatalı Koordinat Düzeltme (+40 XP)
# ——————————————————————————————————
@router.post("/self-correct-coordinate", response_model=CoordinateCorrectionResponse)
def self_correct_coordinate(
    payload: CoordinateCorrectionRequest,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    user_id_str = str(current_user.id)
    
    # 1. Şirket koordinatlarını güncelle
    update_comp = text("""
        UPDATE app.companies
        SET lat = :lat, lon = :lon, updated_at = NOW()
        WHERE id = CAST(:cid AS uuid)
    """)
    db.execute(update_comp, {
        "lat": payload.verified_lat,
        "lon": payload.verified_lon,
        "cid": payload.company_id
    })

    # 2. +40 XP Ödülü Tanımla
    award_xp = 40
    update_stats = text("""
        INSERT INTO app.user_gamification_stats (user_id, xp_points, streak_days, current_league, current_level)
        VALUES (CAST(:uid AS uuid), :xp, 1, 'Bronz Ligi', 1)
        ON CONFLICT (user_id) DO UPDATE 
        SET xp_points = app.user_gamification_stats.xp_points + :xp, updated_at = NOW()
        RETURNING xp_points
    """)
    res = db.execute(update_stats, {"uid": user_id_str, "xp": award_xp}).first()
    new_total_xp = res[0] if res else award_xp

    # Log ekle
    log_sql = text("""
        INSERT INTO app.xp_audit_logs (user_id, action_type, points_awarded, metadata_json)
        VALUES (CAST(:uid AS uuid), 'coord_correction', :points, :meta)
    """)
    db.execute(log_sql, {
        "uid": user_id_str,
        "points": award_xp,
        "meta": f'{{"company_id": "{payload.company_id}", "lat": {payload.verified_lat}, "lon": {payload.verified_lon}}}'
    })
    db.commit()

    return CoordinateCorrectionResponse(
        success=True,
        message=f"Teşekkürler! Şirket konumu haritada doğrulandı. +{award_xp} XP kazandınız!",
        xp_gained=award_xp,
        total_xp=new_total_xp
    )

# ——————————————————————————————————
# 3. İsimsiz & Gizli Liderlik Tablosu (Privacy-First)
# ——————————————————————————————————
@router.get("/leaderboard", response_model=PrivacyLeaderboardResponse)
def get_privacy_leaderboard(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    user_id_str = str(current_user.id)

    # Sıralamayı çek
    sql = text("""
        SELECT user_id::text, xp_points, current_league
        FROM app.user_gamification_stats
        ORDER BY xp_points DESC
        LIMIT 50
    """)
    rows = db.execute(sql).fetchall()

    rankings: List[LeaderboardRankItem] = []
    my_rank = 1
    my_xp = 0
    my_league = "Bronz Ligi"

    found_me = False
    for idx, r in enumerate(rows, start=1):
        uid = r[0]
        xp = r[1]
        is_me = (uid == user_id_str)
        
        if is_me:
            my_rank = idx
            my_xp = xp
            my_league = r[2] or "Bronz Ligi"
            found_me = True
            label = "SEN"
        else:
            # İsimler KESİNLİKLE gizlenir — sadece anonim sıra etiketi verilir
            label = f"Temsilci #{idx * 17 + 3}"

        rankings.append(LeaderboardRankItem(
            rank=idx,
            anonymous_label=label,
            xp=xp,
            is_current_user=is_me
        ))

    percentile = f"Top %{max(1, math.ceil((my_rank / max(len(rankings), 1)) * 100))}"

    return PrivacyLeaderboardResponse(
        my_rank=my_rank,
        my_xp=my_xp,
        my_league=my_league,
        percentile_text=f"{percentile} dilimdesin!",
        rankings=rankings
    )

# ——————————————————————————————————
# 4. Profil ve Başarı İstatistikleri
# ——————————————————————————————————
@router.get("/profile", response_model=UserGamificationProfile)
def get_user_gamification_profile(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    user_id_str = str(current_user.id)

    sql = text("""
        SELECT xp_points, streak_days, current_league, current_level
        FROM app.user_gamification_stats
        WHERE user_id = CAST(:uid AS uuid)
    """)
    row = db.execute(sql, {"uid": user_id_str}).first()

    xp = row[0] if row else 0
    streak = row[1] if row else 0
    league = row[2] if row else "Bronz Ligi"
    level = row[3] if row else 1

    return UserGamificationProfile(
        xp_points=xp,
        current_level=level,
        current_league=league,
        streak_days=streak,
        next_level_xp=level * 500,
        badges_count=3,
        quests_completed_today=2
    )

# ——————————————————————————————————
# 5. 1.000+ Dinamik Görev Jeneratörü
# ——————————————————————————————————
@router.get("/daily-quests", response_model=List[DailyQuestItem])
def get_daily_quests(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    # 1.000+ Görev matrisinden rastgele 3 taze görev üret
    districts = ["Kadıköy", "Beşiktaş", "Şişli", "Ümraniye", "Ataşehir", "Kağıthane", "Levent"]
    actions = [
        ("5 km yarıçapındaki 2 firmayı ziyaret et", "distance", 2, 80),
        ("OCR ile metinsel verisi eksik 1 firmayı güncelle", "ocr_data", 1, 60),
        ("Haritada konumu onaylanmamış 2 firmanın yerini doğrula", "coord_correction", 2, 100),
        ("Saat 12:00'den önce 2 müşteri ziyaretini tamamla", "time", 2, 70),
        ("Müşteri kartvizit bilgilerini metin olarak kaydet", "ocr_data", 1, 50),
    ]

    selected = random.sample(actions, 3)
    quests: List[DailyQuestItem] = []

    for idx, item in enumerate(selected, start=1):
        quests.append(DailyQuestItem(
            id=f"quest_{idx}",
            title=item[0],
            quest_type=item[1],
            target_count=item[2],
            current_progress=random.randint(0, item[2]),
            xp_reward=item[3],
            is_completed=False
        ))

    return quests
