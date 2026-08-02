package domain

import (
	"context"
	"time"
)

type Company struct {
	ID               string    `json:"id"`
	Unvan            string    `json:"unvan"`
	TicaretSicilNo   string    `json:"ticaret_sicil_no"`
	MersisNo         string    `json:"mersis_no"`
	SicilMudurluk    string    `json:"sicil_mudurluk"`
	SicilOfficeCode  string    `json:"sicil_office_code"`
	Address          string    `json:"address"`
	Latitude         *float64  `json:"latitude"`
	Longitude        *float64  `json:"longitude"`
	IsScraped        bool      `json:"is_scraped"`
	CreatedAt        time.Time `json:"created_at"`
}

type CompanyRepository interface {
	GetByID(ctx context.Context, id string) (*Company, error)
	Search(ctx context.Context, query string, limit int) ([]Company, error)
	GetNearby(ctx context.Context, lat, lng float64, radiusInMeters float64) ([]Company, error)
}

type CompanyUseCase interface {
	GetByID(ctx context.Context, id string) (*Company, error)
	SearchCompanies(ctx context.Context, query string, limit int) ([]Company, error)
	FindNearbyCompanies(ctx context.Context, lat, lng float64, radiusInMeters float64) ([]Company, error)
}
