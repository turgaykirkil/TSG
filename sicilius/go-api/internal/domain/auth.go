package domain

import (
	"context"
	"time"
)

type Customer struct {
	ID           string    `json:"id"`
	Title        string    `json:"title"`        // Firma Ünvanı
	TaxNumber    string    `json:"tax_number"`   // VKN / TCKN
	ContactEmail string    `json:"contact_email"`
	ContactPhone string    `json:"contact_phone"`
	PackageName  string    `json:"package_name"` // Basic, Pro, Enterprise
	MonthlyQuota int       `json:"monthly_quota"`
	IsActive     bool      `json:"is_active"`
	CreatedAt    time.Time `json:"created_at"`
	UpdatedAt    time.Time `json:"updated_at"`
}

type APIKey struct {
	ID           string     `json:"id"`
	CustomerID   string     `json:"customer_id"`
	KeyPrefix    string     `json:"key_prefix"`    // sk_live_ veya sk_test_
	KeyHash      string     `json:"-"`             // SHA-256 hash of API key
	SecretHash   string     `json:"-"`             // HMAC Secret
	Environment  string     `json:"environment"`   // "live" veya "sandbox"
	Scopes       []string   `json:"scopes"`        // e.g. ["companies.read", "nexus.fraud"]
	RateLimitRPS int        `json:"rate_limit_rps"`// Max requests per second
	ExpiresAt    time.Time  `json:"expires_at"`
	IsSuspended  bool       `json:"is_suspended"`
	CreatedAt    time.Time  `json:"created_at"`
	LastUsedAt   *time.Time `json:"last_used_at,omitempty"`
}

type APIUsageLog struct {
	ID             string    `json:"id"`
	CustomerID     string    `json:"customer_id"`
	APIKeyID       string    `json:"api_key_id"`
	Endpoint       string    `json:"endpoint"`
	HTTPMethod     string    `json:"http_method"`
	StatusCode     int       `json:"status_code"`
	ResponseTimeMS int64     `json:"response_time_ms"`
	Timestamp      time.Time `json:"timestamp"`
}

type MobileUser struct {
	ID              string    `json:"id"`
	FullName        string    `json:"full_name"`
	Email           string    `json:"email"`
	PasswordHash    string    `json:"-"`
	CompanyTitle    string    `json:"company_title"`
	Source          string    `json:"source"`            // "mobile" veya "web_invite"
	CanAccessWeb    bool      `json:"can_access_web"`    // false for mobile signup
	CanAccessMobile bool      `json:"can_access_mobile"` // true for all
	IsActive        bool      `json:"is_active"`
	CreatedAt       time.Time `json:"created_at"`
}

type MobileLoginResponse struct {
	Token        string      `json:"token"`
	User         *MobileUser `json:"user"`
	CanAccessWeb bool        `json:"can_access_web"`
}

type AuthRepository interface {
	GetAPIKeyByPrefixAndHash(ctx context.Context, prefix, hash string) (*APIKey, error)
	GetCustomerByID(ctx context.Context, customerID string) (*Customer, error)
	LogAPIUsage(ctx context.Context, log *APIUsageLog) error
	GetMonthlyUsageCount(ctx context.Context, customerID string, year int, month time.Month) (int, error)
	CreateCustomer(ctx context.Context, customer *Customer) error
	CreateAPIKey(ctx context.Context, apiKey *APIKey) error
	UpdateAPIKeyStatus(ctx context.Context, keyID string, isSuspended bool) error
	
	// Mobile User Methods
	CreateMobileUser(ctx context.Context, user *MobileUser) error
	GetMobileUserByEmail(ctx context.Context, email string) (*MobileUser, error)
}

type AuthUseCase interface {
	ValidateAPIKey(ctx context.Context, keyPrefix, keyHash string) (*APIKey, *Customer, error)
	VerifyHMACSignature(secret, method, path, timestamp, body, signature string) bool
	LogRequestUsage(ctx context.Context, log *APIUsageLog) error
	IsWithinBusinessHours(t time.Time) bool

	// Mobile Auth Methods
	RegisterMobileUser(ctx context.Context, fullName, email, password, companyTitle string) (*MobileUser, error)
	LoginMobileUser(ctx context.Context, email, password string) (*MobileLoginResponse, error)
	ForgotPassword(ctx context.Context, email string) error
}
