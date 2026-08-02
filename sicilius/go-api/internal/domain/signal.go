package domain

import (
	"context"
	"time"
)

type SignalRule struct {
	ID           string    `json:"id"`
	CustomerID   string    `json:"customer_id"`
	Name         string    `json:"name"`          // örn. "İflas İlanı Sinyali"
	EventType    string    `json:"event_type"`    // "establishment", "capital_change", "liquidation", "management_change"
	TargetVKN    string    `json:"target_vkn,omitempty"`
	WebhookURL   string    `json:"webhook_url"`
	Secret       string    `json:"-"`             // Webhook HMAC secret
	IsActive     bool      `json:"is_active"`
	CreatedAt    time.Time `json:"created_at"`
}

type SignalEvent struct {
	ID           string    `json:"id"`
	RuleID       string    `json:"rule_id"`
	CustomerID   string    `json:"customer_id"`
	EventType    string    `json:"event_type"`
	CompanyID    string    `json:"company_id"`
	CompanyTitle string    `json:"company_title"`
	PayloadJSON  string    `json:"payload_json"`
	Status       string    `json:"status"`        // "PENDING", "SENT", "FAILED"
	HTTPStatus   int       `json:"http_status"`
	Attempts     int       `json:"attempts"`
	CreatedAt    time.Time `json:"created_at"`
	SentAt       *time.Time`json:"sent_at,omitempty"`
}

type SignalRepository interface {
	CreateRule(ctx context.Context, rule *SignalRule) error
	GetRulesByCustomer(ctx context.Context, customerID string) ([]SignalRule, error)
	DeleteRule(ctx context.Context, ruleID, customerID string) error
	LogEvent(ctx context.Context, event *SignalEvent) error
}

type SignalUseCase interface {
	RegisterSignalRule(ctx context.Context, rule *SignalRule) error
	GetCustomerRules(ctx context.Context, customerID string) ([]SignalRule, error)
	RemoveSignalRule(ctx context.Context, ruleID, customerID string) error
	DispatchSignal(ctx context.Context, eventType, companyID, companyTitle string, payload map[string]interface{}) error
}
