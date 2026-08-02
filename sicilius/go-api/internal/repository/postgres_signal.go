package repository

import (
	"context"
	"sync"

	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/turgaykirkil/sicilius-go/internal/domain"
)

type postgresSignalRepository struct {
	db    *pgxpool.Pool
	mu    sync.RWMutex
	rules map[string][]domain.SignalRule
}

func NewPostgresSignalRepository(db *pgxpool.Pool) domain.SignalRepository {
	return &postgresSignalRepository{
		db:    db,
		rules: make(map[string][]domain.SignalRule),
	}
}

func (r *postgresSignalRepository) CreateRule(ctx context.Context, rule *domain.SignalRule) error {
	r.mu.Lock()
	defer r.mu.Unlock()
	r.rules[rule.CustomerID] = append(r.rules[rule.CustomerID], *rule)
	return nil
}

func (r *postgresSignalRepository) GetRulesByCustomer(ctx context.Context, customerID string) ([]domain.SignalRule, error) {
	r.mu.RLock()
	defer r.mu.RUnlock()
	return r.rules[customerID], nil
}

func (r *postgresSignalRepository) DeleteRule(ctx context.Context, ruleID, customerID string) error {
	r.mu.Lock()
	defer r.mu.Unlock()
	list := r.rules[customerID]
	newList := make([]domain.SignalRule, 0)
	for _, item := range list {
		if item.ID != ruleID {
			newList = append(newList, item)
		}
	}
	r.rules[customerID] = newList
	return nil
}

func (r *postgresSignalRepository) LogEvent(ctx context.Context, event *domain.SignalEvent) error {
	return nil
}
