package domain

import (
	"context"
	"time"
)

type FieldRoute struct {
	ID            string    `json:"id"`
	UserID        *string   `json:"user_id,omitempty"`
	Title         string    `json:"title"`
	TotalDistance float64   `json:"total_distance"`
	TotalDuration int       `json:"total_duration"`
	Status        string    `json:"status"`
	CreatedAt     time.Time `json:"created_at"`
	UpdatedAt     time.Time `json:"updated_at"`
}

type FieldRouteRepository interface {
	GetByUserID(ctx context.Context, userID string) ([]FieldRoute, error)
	Create(ctx context.Context, route *FieldRoute) error
	Update(ctx context.Context, route *FieldRoute) error
}

type FieldRouteUsecase interface {
	GetByUserID(ctx context.Context, userID string) ([]FieldRoute, error)
	Create(ctx context.Context, route *FieldRoute) error
	Update(ctx context.Context, route *FieldRoute) error
}
