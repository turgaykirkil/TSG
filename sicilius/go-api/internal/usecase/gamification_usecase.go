package usecase

import (
	"context"
	"fmt"
	"math"
	"time"

	"github.com/turgaykirkil/sicilius-go/internal/domain"
)

type gamificationUseCase struct {
	repo domain.GamificationRepository
}

func NewGamificationUseCase(repo domain.GamificationRepository) domain.GamificationUseCase {
	return &gamificationUseCase{repo: repo}
}

func haversineDistanceMeters(lat1, lon1, lat2, lon2 float64) float64 {
	const R = 6371000.0 // Earth radius in meters
	phi1 := lat1 * math.Pi / 180.0
	phi2 := lat2 * math.Pi / 180.0
	deltaPhi := (lat2 - lat1) * math.Pi / 180.0
	deltaLambda := (lon2 - lon1) * math.Pi / 180.0

	a := math.Sin(deltaPhi/2.0)*math.Sin(deltaPhi/2.0) +
		math.Cos(phi1)*math.Cos(phi2)*math.Sin(deltaLambda/2.0)*math.Sin(deltaLambda/2.0)
	c := 2.0 * math.Atan2(math.Sqrt(a), math.Sqrt(1.0-a))
	return R * c
}

func calculateLeague(xp int) string {
	if xp >= 15000 {
		return "Efsane Ligi"
	} else if xp >= 7001 {
		return "Elmas Ligi"
	} else if xp >= 3001 {
		return "Altın Ligi"
	} else if xp >= 1001 {
		return "Gümüş Ligi"
	}
	return "Bronz Ligi"
}

func (u *gamificationUseCase) PerformCheckIn(ctx context.Context, userID string, req domain.CheckInRequest) (*domain.CheckInResponse, error) {
	cLat, cLon, _ := u.repo.GetCustomerCoordinates(ctx, req.CustomerID)
	targetLat := cLat
	targetLon := cLon
	if targetLat == 0.0 {
		targetLat = req.Latitude
		targetLon = req.Longitude
	}

	dist := haversineDistanceMeters(req.Latitude, req.Longitude, targetLat, targetLon)
	if dist > 50.0 && cLat != 0.0 {
		return &domain.CheckInResponse{
			Success:          false,
			Message:          fmt.Sprintf("Check-in yapabilmek için müşteriye en fazla 50m yakın olmalısınız. (Mesafe: %.0f m)", dist),
			XPGained:         0,
			TotalXP:          0,
			StreakDays:       0,
			StreakMultiplier: 1.0,
			DistanceMeters:   math.Round(dist),
		}, nil
	}

	xpGained := 50
	multiplier := 1.0
	streakDays := 1
	now := time.Now()
	todayDate := time.Date(now.Year(), now.Month(), now.Day(), 0, 0, 0, 0, time.UTC)

	stats, err := u.repo.GetUserStats(ctx, userID)
	if err != nil || stats == nil {
		stats = &domain.UserGamificationStats{
			UserID:          userID,
			XPPoints:        xpGained,
			StreakDays:      1,
			LastCheckInDate: &todayDate,
			CurrentLeague:   "Bronz Ligi",
			CurrentLevel:    1,
		}
	} else {
		if stats.LastCheckInDate != nil {
			diffDays := int(todayDate.Sub(*stats.LastCheckInDate).Hours() / 24)
			if diffDays == 1 {
				streakDays = stats.StreakDays + 1
			} else if diffDays == 0 {
				streakDays = stats.StreakDays
			} else {
				streakDays = 1
			}
		}

		if streakDays >= 30 {
			multiplier = 2.0
		} else if streakDays >= 7 {
			multiplier = 1.5
		} else if streakDays >= 3 {
			multiplier = 1.2
		}

		xpGained = int(float64(xpGained) * multiplier)
		if len(req.OCRDataJSON) > 0 {
			xpGained += 35
		}
		if len(req.NoteText) >= 10 {
			xpGained += 25
		}

		stats.XPPoints += xpGained
		stats.StreakDays = streakDays
		stats.LastCheckInDate = &todayDate
		stats.CurrentLeague = calculateLeague(stats.XPPoints)
	}

	_ = u.repo.UpsertUserStats(ctx, stats)
	meta := fmt.Sprintf(`{"customer_id": "%s", "distance": %.1f}`, req.CustomerID, dist)
	_ = u.repo.LogXPAudit(ctx, userID, "check_in", xpGained, meta)

	return &domain.CheckInResponse{
		Success:          true,
		Message:          fmt.Sprintf("Tebrikler! Müşteri ziyareti check-in doğrulandı. +%d XP kazandınız!", xpGained),
		XPGained:         xpGained,
		TotalXP:          stats.XPPoints,
		StreakDays:       streakDays,
		StreakMultiplier: multiplier,
		DistanceMeters:   math.Round(dist),
	}, nil
}

func (u *gamificationUseCase) SelfCorrectCoordinate(ctx context.Context, userID string, req domain.CoordinateCorrectionRequest) (*domain.CoordinateCorrectionResponse, error) {
	_ = u.repo.UpdateCompanyCoordinates(ctx, req.CompanyID, req.VerifiedLat, req.VerifiedLon)

	awardXP := 40
	now := time.Now()
	todayDate := time.Date(now.Year(), now.Month(), now.Day(), 0, 0, 0, 0, time.UTC)

	stats, _ := u.repo.GetUserStats(ctx, userID)
	if stats == nil {
		stats = &domain.UserGamificationStats{
			UserID:          userID,
			XPPoints:        awardXP,
			StreakDays:      1,
			LastCheckInDate: &todayDate,
			CurrentLeague:   "Bronz Ligi",
			CurrentLevel:    1,
		}
	} else {
		stats.XPPoints += awardXP
	}

	_ = u.repo.UpsertUserStats(ctx, stats)
	meta := fmt.Sprintf(`{"company_id": "%s", "lat": %.6f, "lon": %.6f}`, req.CompanyID, req.VerifiedLat, req.VerifiedLon)
	_ = u.repo.LogXPAudit(ctx, userID, "coord_correction", awardXP, meta)

	return &domain.CoordinateCorrectionResponse{
		Success:  true,
		Message:  fmt.Sprintf("Teşekkürler! Şirket konumu haritada doğrulandı. +%d XP kazandınız!", awardXP),
		XPGained: awardXP,
		TotalXP:  stats.XPPoints,
	}, nil
}

func (u *gamificationUseCase) GetLeaderboard(ctx context.Context, userID string) (*domain.PrivacyLeaderboardResponse, error) {
	return u.repo.GetPrivacyLeaderboard(ctx, userID)
}

func (u *gamificationUseCase) GetDailyQuests(ctx context.Context, userID string) ([]domain.DailyQuestItem, error) {
	quests := []domain.DailyQuestItem{
		{
			ID:              "quest_1",
			Title:           "5 km yarıçapındaki 2 firmayı ziyaret et",
			QuestType:       "distance",
			TargetCount:     2,
			CurrentProgress: 1,
			XPReward:        80,
			IsCompleted:     false,
		},
		{
			ID:              "quest_2",
			Title:           "Haritada konumu onaylanmamış 2 firmanın yerini doğrula",
			QuestType:       "coord_correction",
			TargetCount:     2,
			CurrentProgress: 0,
			XPReward:        100,
			IsCompleted:     false,
		},
		{
			ID:              "quest_3",
			Title:           "Saat 12:00'den önce 2 müşteri ziyaretini tamamla",
			QuestType:       "time",
			TargetCount:     2,
			CurrentProgress: 1,
			XPReward:        70,
			IsCompleted:     false,
		},
	}
	return quests, nil
}
