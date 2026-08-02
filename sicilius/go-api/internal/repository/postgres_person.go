package repository

import (
	"context"

	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/turgaykirkil/sicilius-go/internal/domain"
)

type postgresPersonRepository struct {
	db *pgxpool.Pool
}

func NewPostgresPersonRepository(db *pgxpool.Pool) domain.PersonRepository {
	return &postgresPersonRepository{
		db: db,
	}
}

func (r *postgresPersonRepository) SearchByNameOrTCKN(ctx context.Context, query string, limit int) ([]domain.Person, error) {
	persons := []domain.Person{
		{
			ID:       "per_101",
			FullName: "Ahmet Yılmaz",
			TCKN:     "100******88",
		},
		{
			ID:       "per_102",
			FullName: "Fatma Özdemir",
			TCKN:     "245******12",
		},
	}
	return persons, nil
}

func (r *postgresPersonRepository) GetCompanyRelations(ctx context.Context, personID string) ([]domain.PersonCompanyRelation, error) {
	relations := []domain.PersonCompanyRelation{
		{
			PersonID:     personID,
			FullName:     "Ahmet Yılmaz",
			CompanyID:    "comp_201",
			CompanyTitle: "Yılmaz Dış Ticaret A.Ş.",
			Role:         "Yönetim Kurulu Başkanı",
			IsActive:     true,
		},
		{
			PersonID:     personID,
			FullName:     "Ahmet Yılmaz",
			CompanyID:    "comp_202",
			CompanyTitle: "Yılmaz Lojistik Ltd. Şti.",
			Role:         "Kurucu Ortak",
			IsActive:     true,
		},
	}
	return relations, nil
}
