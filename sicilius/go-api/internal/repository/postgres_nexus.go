package repository

import (
	"context"
	"time"

	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/turgaykirkil/sicilius-go/internal/domain"
)

type postgresNexusRepository struct {
	db *pgxpool.Pool
}

func NewPostgresNexusRepository(db *pgxpool.Pool) domain.NexusRepository {
	return &postgresNexusRepository{
		db: db,
	}
}

func (r *postgresNexusRepository) CheckCompanyFraud(ctx context.Context, companyID string) (*domain.NexusFraudCheckResult, error) {
	return &domain.NexusFraudCheckResult{
		TargetType: "company",
		TargetID:   companyID,
		TargetName: "Örnek Ticaret A.Ş.",
		RiskScore:  15,
		RiskLevel:  "LOW",
		RedFlags: []domain.RedFlag{
			{
				Code:        "RECENT_ADDRESS_CHANGE",
				Severity:    "LOW",
				Description: "Şirket adresi son 6 ay içerisinde değiştirildi.",
			},
		},
		RelationCount: 4,
		ClosedCoCount: 0,
		CheckedAt:     time.Now(),
	}, nil
}

func (r *postgresNexusRepository) CheckPersonFraud(ctx context.Context, personID string) (*domain.NexusFraudCheckResult, error) {
	return &domain.NexusFraudCheckResult{
		TargetType: "person",
		TargetID:   personID,
		TargetName: "Ahmet Yılmaz",
		RiskScore:  45,
		RiskLevel:  "MEDIUM",
		RedFlags: []domain.RedFlag{
			{
				Code:        "MULTIPLE_LIQUIDATION_RELATIONS",
				Severity:    "MEDIUM",
				Description: "Kişinin geçmişte tasfiyeye giren 2 farklı şirkette ortaklığı bulunmaktadır.",
			},
		},
		RelationCount: 5,
		ClosedCoCount: 2,
		CheckedAt:     time.Now(),
	}, nil
}
