package domain

import (
	"context"
	"time"
)

type Person struct {
	ID        string    `json:"id"`
	FullName  string    `json:"full_name"`
	TCKN      string    `json:"tckn,omitempty"`
	CreatedAt time.Time `json:"created_at"`
}

type PersonCompanyRelation struct {
	PersonID      string    `json:"person_id"`
	FullName      string    `json:"full_name"`
	CompanyID     string    `json:"company_id"`
	CompanyTitle  string    `json:"company_title"`
	Role          string    `json:"role"` // Kurucu, Yönetim Kurulu Üyesi, Müdür, vb.
	ShareRatio    *float64  `json:"share_ratio,omitempty"`
	StartDate     *time.Time`json:"start_date,omitempty"`
	EndDate       *time.Time`json:"end_date,omitempty"`
	IsActive      bool      `json:"is_active"`
}

type PersonRepository interface {
	SearchByNameOrTCKN(ctx context.Context, query string, limit int) ([]Person, error)
	GetCompanyRelations(ctx context.Context, personID string) ([]PersonCompanyRelation, error)
}

type PersonUseCase interface {
	SearchPersons(ctx context.Context, query string, limit int) ([]Person, error)
	GetPersonRelations(ctx context.Context, personID string) ([]PersonCompanyRelation, error)
}
