package usecase

import (
	"context"

	"github.com/turgaykirkil/sicilius-go/internal/domain"
)

type signalUseCase struct {
	signalRepo domain.SignalRepository
}

func NewSignalUseCase(signalRepo domain.SignalRepository) domain.SignalUseCase {
	return &signalUseCase{
		signalRepo: signalRepo,
	}
}

func (s *signalUseCase) RegisterSignalRule(ctx context.Context, rule *domain.SignalRule) error {
	return s.signalRepo.CreateRule(ctx, rule)
}

func (s *signalUseCase) GetCustomerRules(ctx context.Context, customerID string) ([]domain.SignalRule, error) {
	return s.signalRepo.GetRulesByCustomer(ctx, customerID)
}

func (s *signalUseCase) RemoveSignalRule(ctx context.Context, ruleID, customerID string) error {
	return s.signalRepo.DeleteRule(ctx, ruleID, customerID)
}

func (s *signalUseCase) DispatchSignal(ctx context.Context, eventType, companyID, companyTitle string, payload map[string]interface{}) error {
	return nil
}
