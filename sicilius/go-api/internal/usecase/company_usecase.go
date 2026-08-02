package usecase

import (
	"context"
	"fmt"
	"github.com/turgaykirkil/sicilius-go/internal/domain"
)

type companyUseCase struct {
	repo domain.CompanyRepository
}

func NewCompanyUseCase(repo domain.CompanyRepository) domain.CompanyUseCase {
	return &companyUseCase{repo: repo}
}

func (u *companyUseCase) GetByID(ctx context.Context, id string) (*domain.Company, error) {
	if id == "" {
		return nil, fmt.Errorf("usecase: company ID cannot be empty")
	}
	return u.repo.GetByID(ctx, id)
}

func (u *companyUseCase) SearchCompanies(ctx context.Context, query string, limit int) ([]domain.Company, error) {
	if limit <= 0 {
		limit = 20
	}
	if limit > 100 {
		limit = 100
	}
	return u.repo.Search(ctx, query, limit)
}

func (u *companyUseCase) FindNearbyCompanies(ctx context.Context, lat, lng float64, radiusInMeters float64) ([]domain.Company, error) {
	if radiusInMeters <= 0 {
		radiusInMeters = 5000 // Default 5 km
	}
	if radiusInMeters > 50000 {
		radiusInMeters = 50000 // Max 50 km
	}
	return u.repo.GetNearby(ctx, lat, lng, radiusInMeters)
}
