package domain

import (
	"context"
	"time"
)

type RedFlag struct {
	Code        string `json:"code"`        // örn. MULTIPLE_LIQUIDATION_RELATIONS, HIGH_FREQUENCY_DIRECTOR_CHANGE
	Severity    string `json:"severity"`    // LOW, MEDIUM, HIGH, CRITICAL
	Description string `json:"description"`
}

type NexusFraudCheckResult struct {
	TargetType     string     `json:"target_type"`     // "company" veya "person"
	TargetID       string     `json:"target_id"`
	TargetName     string     `json:"target_name"`
	RiskScore      int        `json:"risk_score"`      // 0 - 100
	RiskLevel      string     `json:"risk_level"`      // LOW, MEDIUM, HIGH, CRITICAL
	RedFlags       []RedFlag  `json:"red_flags"`
	RelationCount  int        `json:"relation_count"`
	ClosedCoCount  int        `json:"closed_company_count"`
	CheckedAt      time.Time  `json:"checked_at"`
}

type NexusRepository interface {
	CheckCompanyFraud(ctx context.Context, companyID string) (*NexusFraudCheckResult, error)
	CheckPersonFraud(ctx context.Context, personID string) (*NexusFraudCheckResult, error)
}

type NexusUseCase interface {
	AnalyzeCompanyRisk(ctx context.Context, companyID string) (*NexusFraudCheckResult, error)
	AnalyzePersonRisk(ctx context.Context, personID string) (*NexusFraudCheckResult, error)
}
