package domain

import (
	"context"
	"time"
)

type UserGamificationStats struct {
	ID              string     `json:"id"`
	UserID          string     `json:"user_id"`
	XPPoints        int        `json:"xp_points"`
	StreakDays      int        `json:"streak_days"`
	LastCheckInDate *time.Time `json:"last_checkin_date"`
	CurrentLeague   string     `json:"current_league"`
	CurrentLevel    int        `json:"current_level"`
	CreatedAt       time.Time  `json:"created_at"`
	UpdatedAt       time.Time  `json:"updated_at"`
}

type CheckInRequest struct {
	CustomerID   string                 `json:"customer_id"`
	Latitude     float64                `json:"latitude"`
	Longitude    float64                `json:"longitude"`
	NoteText     string                 `json:"note_text,omitempty"`
	OCRDataJSON  map[string]interface{} `json:"ocr_data_json,omitempty"`
}

type CheckInResponse struct {
	Success          bool     `json:"success"`
	Message          string   `json:"message"`
	XPGained         int      `json:"xp_gained"`
	TotalXP          int      `json:"total_xp"`
	StreakDays       int      `json:"streak_days"`
	StreakMultiplier float64  `json:"streak_multiplier"`
	DistanceMeters   float64  `json:"distance_meters"`
	BadgesUnlocked   []string `json:"badges_unlocked"`
}

type CoordinateCorrectionRequest struct {
	CompanyID   string  `json:"company_id"`
	VerifiedLat float64 `json:"verified_lat"`
	VerifiedLon float64 `json:"verified_lon"`
}

type CoordinateCorrectionResponse struct {
	Success bool   `json:"success"`
	Message string `json:"message"`
	XPGained int   `json:"xp_gained"`
	TotalXP  int   `json:"total_xp"`
}

type LeaderboardRankItem struct {
	Rank           int    `json:"rank"`
	AnonymousLabel string `json:"anonymous_label"`
	XP             int    `json:"xp"`
	IsCurrentUser  bool   `json:"is_current_user"`
}

type PrivacyLeaderboardResponse struct {
	MyRank         int                   `json:"my_rank"`
	MyXP           int                   `json:"my_xp"`
	MyLeague       string                `json:"my_league"`
	PercentileText string                `json:"percentile_text"`
	Rankings       []LeaderboardRankItem `json:"rankings"`
}

type BadgeItem struct {
	Code        string `json:"code"`
	Title       string `json:"title"`
	Description string `json:"description"`
	Icon        string `json:"icon"`
	Category    string `json:"category"`
	IsUnlocked  bool   `json:"is_unlocked"`
}

type DailyQuestItem struct {
	ID              string `json:"id"`
	Title           string `json:"title"`
	QuestType       string `json:"quest_type"`
	TargetCount     int    `json:"target_count"`
	CurrentProgress int    `json:"current_progress"`
	XPReward        int    `json:"xp_reward"`
	IsCompleted     bool   `json:"is_completed"`
}

type GamificationRepository interface {
	GetUserStats(ctx context.Context, userID string) (*UserGamificationStats, error)
	UpsertUserStats(ctx context.Context, stats *UserGamificationStats) error
	LogXPAudit(ctx context.Context, userID, actionType string, points int, metadata string) error
	UpdateCompanyCoordinates(ctx context.Context, companyID string, lat, lon float64) error
	GetPrivacyLeaderboard(ctx context.Context, userID string) (*PrivacyLeaderboardResponse, error)
	GetCustomerCoordinates(ctx context.Context, customerID string) (float64, float64, error)
}

type GamificationUseCase interface {
	PerformCheckIn(ctx context.Context, userID string, req CheckInRequest) (*CheckInResponse, error)
	SelfCorrectCoordinate(ctx context.Context, userID string, req CoordinateCorrectionRequest) (*CoordinateCorrectionResponse, error)
	GetLeaderboard(ctx context.Context, userID string) (*PrivacyLeaderboardResponse, error)
	GetDailyQuests(ctx context.Context, userID string) ([]DailyQuestItem, error)
}
