package usecase

import (
	"context"

	"github.com/turgaykirkil/sicilius-go/internal/domain"
)

type nexusUseCase struct {
	nexusRepo domain.NexusRepository
}

func NewNexusUseCase(nexusRepo domain.NexusRepository) domain.NexusUseCase {
	return &nexusUseCase{
		nexusRepo: nexusRepo,
	}
}

func (n *nexusUseCase) AnalyzeCompanyRisk(ctx context.Context, companyID string) (*domain.NexusFraudCheckResult, error) {
	return n.nexusRepo.CheckCompanyFraud(ctx, companyID)
}

func (n *nexusUseCase) AnalyzePersonRisk(ctx context.Context, personID string) (*domain.NexusFraudCheckResult, error) {
	return n.nexusRepo.CheckPersonFraud(ctx, personID)
}
