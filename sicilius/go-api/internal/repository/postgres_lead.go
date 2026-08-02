package repository

import (
	"context"
	"fmt"
	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/turgaykirkil/sicilius-go/internal/domain"
)

type postgresLeadRepository struct {
	db *pgxpool.Pool
}

func NewPostgresLeadRepository(db *pgxpool.Pool) domain.LeadRepository {
	return &postgresLeadRepository{db: db}
}

func (r *postgresLeadRepository) GetNearbyLeads(ctx context.Context, lat, lng float64, radiusInMeters float64) ([]domain.Lead, error) {
	query := `
		SELECT c.id, c.id as company_id, c.unvan as trade_name, 
		       ST_Y(c.koordinat::geometry) as latitude, 
		       ST_X(c.koordinat::geometry) as longitude, 
		       COALESCE(o.status, 'established') as change_type,
		       c.created_at
		FROM app.companies c
		LEFT JOIN app.ocr_results o ON o.company_id = c.id
		WHERE c.koordinat IS NOT NULL
		  AND ST_DWithin(
			c.koordinat,
			ST_SetSRID(ST_MakePoint($1, $2), 4326)::geography,
			$3
		  )
		ORDER BY c.created_at DESC
		LIMIT 100
	`

	rows, err := r.db.Query(ctx, query, lng, lat, radiusInMeters)
	if err != nil {
		return nil, fmt.Errorf("repository: failed to query nearby leads: %w", err)
	}
	defer rows.Close()

	var leads []domain.Lead
	for rows.Next() {
		var l domain.Lead
		err := rows.Scan(
			&l.ID, &l.CompanyID, &l.TradeName,
			&l.Latitude, &l.Longitude, &l.ChangeType,
			&l.CreatedAt,
		)
		if err != nil {
			return nil, fmt.Errorf("repository: failed to scan lead row: %w", err)
		}
		leads = append(leads, l)
	}

	return leads, nil
}
