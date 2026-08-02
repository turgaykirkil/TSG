package repository

import (
	"context"
	"fmt"
	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/turgaykirkil/sicilius-go/internal/domain"
)

type postgresCompanyRepository struct {
	db *pgxpool.Pool
}

func NewPostgresCompanyRepository(db *pgxpool.Pool) domain.CompanyRepository {
	return &postgresCompanyRepository{db: db}
}

func (r *postgresCompanyRepository) GetByID(ctx context.Context, id string) (*domain.Company, error) {
	query := `
		SELECT id, unvan, COALESCE(sicil_no, ''), COALESCE(mersis_number, ''), 
		       COALESCE(sicil_mudurluk, ''), COALESCE(sicil_office_code, ''), COALESCE(address, ''), 
		       ST_Y(koordinat::geometry) as latitude, ST_X(koordinat::geometry) as longitude,
		       COALESCE(scraped_at IS NOT NULL, false) as is_scraped, created_at
		FROM app.companies
		WHERE id::text = $1
	`
	row := r.db.QueryRow(ctx, query, id)

	var c domain.Company
	err := row.Scan(
		&c.ID, &c.Unvan, &c.TicaretSicilNo, &c.MersisNo,
		&c.SicilMudurluk, &c.SicilOfficeCode, &c.Address,
		&c.Latitude, &c.Longitude, &c.IsScraped, &c.CreatedAt,
	)
	if err != nil {
		return nil, fmt.Errorf("repository: company not found: %w", err)
	}

	return &c, nil
}

func (r *postgresCompanyRepository) Search(ctx context.Context, searchQuery string, limit int) ([]domain.Company, error) {
	query := `
		SELECT id, unvan, COALESCE(sicil_no, ''), COALESCE(mersis_number, ''), 
		       COALESCE(sicil_mudurluk, ''), COALESCE(sicil_office_code, ''), COALESCE(address, ''), 
		       ST_Y(koordinat::geometry) as latitude, ST_X(koordinat::geometry) as longitude,
		       COALESCE(scraped_at IS NOT NULL, false) as is_scraped, created_at
		FROM app.companies
		WHERE unvan ILIKE $1 OR mersis_number ILIKE $1 OR sicil_no ILIKE $1
		ORDER BY created_at DESC
		LIMIT $2
	`
	searchPattern := "%" + searchQuery + "%"
	rows, err := r.db.Query(ctx, query, searchPattern, limit)
	if err != nil {
		return nil, fmt.Errorf("repository: failed to search companies: %w", err)
	}
	defer rows.Close()

	var companies []domain.Company
	for rows.Next() {
		var c domain.Company
		err := rows.Scan(
			&c.ID, &c.Unvan, &c.TicaretSicilNo, &c.MersisNo,
			&c.SicilMudurluk, &c.SicilOfficeCode, &c.Address,
			&c.Latitude, &c.Longitude, &c.IsScraped, &c.CreatedAt,
		)
		if err != nil {
			return nil, fmt.Errorf("repository: failed to scan company row: %w", err)
		}
		companies = append(companies, c)
	}

	return companies, nil
}

func (r *postgresCompanyRepository) GetNearby(ctx context.Context, lat, lng float64, radiusInMeters float64) ([]domain.Company, error) {
	query := `
		SELECT id, unvan, COALESCE(sicil_no, ''), COALESCE(mersis_number, ''), 
		       COALESCE(sicil_mudurluk, ''), COALESCE(sicil_office_code, ''), COALESCE(address, ''), 
		       ST_Y(koordinat::geometry) as latitude, ST_X(koordinat::geometry) as longitude,
		       COALESCE(scraped_at IS NOT NULL, false) as is_scraped, created_at
		FROM app.companies
		WHERE koordinat IS NOT NULL
		  AND ST_DWithin(
			koordinat,
			ST_SetSRID(ST_MakePoint($1, $2), 4326)::geography,
			$3
		  )
		ORDER BY ST_Distance(
			koordinat,
			ST_SetSRID(ST_MakePoint($1, $2), 4326)::geography
		) ASC
		LIMIT 100
	`

	rows, err := r.db.Query(ctx, query, lng, lat, radiusInMeters)
	if err != nil {
		return nil, fmt.Errorf("repository: failed to query nearby companies with PostGIS: %w", err)
	}
	defer rows.Close()

	var companies []domain.Company
	for rows.Next() {
		var c domain.Company
		err := rows.Scan(
			&c.ID, &c.Unvan, &c.TicaretSicilNo, &c.MersisNo,
			&c.SicilMudurluk, &c.SicilOfficeCode, &c.Address,
			&c.Latitude, &c.Longitude, &c.IsScraped, &c.CreatedAt,
		)
		if err != nil {
			return nil, fmt.Errorf("repository: failed to scan nearby company row: %w", err)
		}
		companies = append(companies, c)
	}

	return companies, nil
}
