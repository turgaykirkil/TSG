package domain

import (
	"context"
	"time"
)

type Lead struct {
	ID         string    `json:"id"`
	CompanyID  string    `json:"company_id"`
	TradeName  string    `json:"trade_name"`
	Latitude   float64   `json:"latitude"`
	Longitude  float64   `json:"longitude"`
	ChangeType string    `json:"change_type"`
	ValueChange string   `json:"value_change,omitempty"`
	CreatedAt  time.Time `json:"created_at"`
}

type LeadRepository interface {
	GetNearbyLeads(ctx context.Context, lat, lng float64, radiusInMeters float64) ([]Lead, error)
}

type LeadUseCase interface {
	FindNearby(ctx context.Context, lat, lng float64, radiusInMeters float64) ([]Lead, error)
}
