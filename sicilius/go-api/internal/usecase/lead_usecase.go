package usecase

import (
	"context"
	"github.com/turgaykirkil/sicilius-go/internal/domain"
)

type leadUseCase struct {
	repo domain.LeadRepository
}

func NewLeadUseCase(repo domain.LeadRepository) domain.LeadUseCase {
	return &leadUseCase{repo: repo}
}

func (u *leadUseCase) FindNearby(ctx context.Context, lat, lng float64, radiusInMeters float64) ([]domain.Lead, error) {
	if radiusInMeters <= 0 {
		radiusInMeters = 5000 // Default 5 km
	}
	if radiusInMeters > 50000 {
		radiusInMeters = 50000 // Max 50 km
	}
	return u.repo.GetNearbyLeads(ctx, lat, lng, radiusInMeters)
}
