package usecase

import (
	"context"
	"testing"

	"github.com/turgaykirkil/sicilius-go/internal/domain"
)

type mockGamificationRepo struct {
	stats map[string]*domain.UserGamificationStats
}

func newMockRepo() *mockGamificationRepo {
	return &mockGamificationRepo{
		stats: make(map[string]*domain.UserGamificationStats),
	}
}

func (m *mockGamificationRepo) GetCustomerCoordinates(ctx context.Context, customerID string) (float64, float64, error) {
	if customerID == "cust_near" {
		return 41.0082, 28.9784, nil // Istanbul Sultanahmet
	}
	if customerID == "cust_far" {
		return 39.9334, 32.8597, nil // Ankara Kızılay
	}
	return 0, 0, nil
}

func (m *mockGamificationRepo) GetUserStats(ctx context.Context, userID string) (*domain.UserGamificationStats, error) {
	s, ok := m.stats[userID]
	if !ok {
		return nil, nil
	}
	return s, nil
}

func (m *mockGamificationRepo) UpsertUserStats(ctx context.Context, stats *domain.UserGamificationStats) error {
	m.stats[stats.UserID] = stats
	return nil
}

func (m *mockGamificationRepo) LogXPAudit(ctx context.Context, userID, actionType string, points int, metadata string) error {
	return nil
}

func (m *mockGamificationRepo) UpdateCompanyCoordinates(ctx context.Context, companyID string, lat, lon float64) error {
	return nil
}

func (m *mockGamificationRepo) GetPrivacyLeaderboard(ctx context.Context, userID string) (*domain.PrivacyLeaderboardResponse, error) {
	return &domain.PrivacyLeaderboardResponse{
		MyRank:         1,
		MyXP:           500,
		MyLeague:       "Bronz Ligi",
		PercentileText: "Top %10 dilimdesin!",
		Rankings: []domain.LeaderboardRankItem{
			{Rank: 1, AnonymousLabel: "SEN", XP: 500, IsCurrentUser: true},
			{Rank: 2, AnonymousLabel: "Temsilci #37", XP: 450, IsCurrentUser: false},
		},
	}, nil
}

func TestGamificationUseCase_CheckIn_FarDistance(t *testing.T) {
	repo := newMockRepo()
	uc := NewGamificationUseCase(repo)

	// User at Istanbul trying to check-in at Ankara customer (> 50m)
	req := domain.CheckInRequest{
		CustomerID: "cust_far",
		Latitude:   41.0082,
		Longitude:  28.9784,
	}

	res, err := uc.PerformCheckIn(context.Background(), "user_1", req)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}

	if res.Success {
		t.Errorf("Expected check-in to fail due to > 50m distance, but got success")
	}
}

func TestGamificationUseCase_CheckIn_Success(t *testing.T) {
	repo := newMockRepo()
	uc := NewGamificationUseCase(repo)

	// User at exact customer location
	req := domain.CheckInRequest{
		CustomerID: "cust_near",
		Latitude:   41.0082,
		Longitude:  28.9784,
		NoteText:   "Ziyaret tamamlandı, kartvizit alındı.",
	}

	res, err := uc.PerformCheckIn(context.Background(), "user_1", req)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}

	if !res.Success {
		t.Errorf("Expected check-in success within 50m distance, but failed: %s", res.Message)
	}

	if res.XPGained < 50 {
		t.Errorf("Expected at least 50 XP gained, got %d", res.XPGained)
	}
}

func TestGamificationUseCase_SelfCorrectCoordinate(t *testing.T) {
	repo := newMockRepo()
	uc := NewGamificationUseCase(repo)

	req := domain.CoordinateCorrectionRequest{
		CompanyID:   "comp_101",
		VerifiedLat: 41.0150,
		VerifiedLon: 28.9800,
	}

	res, err := uc.SelfCorrectCoordinate(context.Background(), "user_1", req)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}

	if !res.Success {
		t.Errorf("Expected coordinate correction success, got failure")
	}

	if res.XPGained != 40 {
		t.Errorf("Expected exactly +40 XP for coordinate correction, got %d", res.XPGained)
	}
}
