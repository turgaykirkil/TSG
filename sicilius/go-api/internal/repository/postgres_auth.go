package repository

import (
	"context"
	"sync"
	"time"

	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/turgaykirkil/sicilius-go/internal/domain"
	"golang.org/x/crypto/bcrypt"
)

type postgresAuthRepository struct {
	db          *pgxpool.Pool
	mu          sync.RWMutex
	memoryKeys  map[string]*domain.APIKey
	customers   map[string]*domain.Customer
	mobileUsers map[string]*domain.MobileUser
	usageLogs   []*domain.APIUsageLog
}

func NewPostgresAuthRepository(db *pgxpool.Pool) domain.AuthRepository {
	repo := &postgresAuthRepository{
		db:          db,
		memoryKeys:  make(map[string]*domain.APIKey),
		customers:   make(map[string]*domain.Customer),
		mobileUsers: make(map[string]*domain.MobileUser),
		usageLogs:   make([]*domain.APIUsageLog, 0),
	}

	repo.seedDemoKeys()
	return repo
}

func (r *postgresAuthRepository) seedDemoKeys() {
	demoCustomer := &domain.Customer{
		ID:           "cust_demo_100",
		Title:        "Sicilius Test Kurumu A.Ş.",
		TaxNumber:    "1234567890",
		ContactEmail: "test-api@sicilius.com.tr",
		ContactPhone: "+902125550000",
		PackageName:  "Enterprise",
		MonthlyQuota: 50000,
		IsActive:     true,
		CreatedAt:    time.Now(),
		UpdatedAt:    time.Now(),
	}
	r.customers[demoCustomer.ID] = demoCustomer

	// Seed Demo Mobile User
	passHash, _ := bcrypt.GenerateFromPassword([]byte("123456"), bcrypt.DefaultCost)
	demoUser := &domain.MobileUser{
		ID:              "muser_demo101",
		FullName:        "Ahmet Yılmaz",
		Email:           "saha@sicilius.com.tr",
		PasswordHash:    string(passHash),
		CompanyTitle:    "Sicilius B2B Saha",
		Source:          "mobile",
		CanAccessWeb:    false,
		CanAccessMobile: true,
		IsActive:        true,
		CreatedAt:       time.Now(),
	}
	r.mobileUsers[demoUser.Email] = demoUser

	// Test Key: sk_test_demo123
	testKey := &domain.APIKey{
		ID:           "key_test_1",
		CustomerID:   demoCustomer.ID,
		KeyPrefix:    "sk_test_",
		KeyHash:      "55e71616ed6a484ca6c3dd79fa7efef9d3cb5019d651c6b16e4dbdb216a69ef4",
		SecretHash:   "secret_test_key_123",
		Environment:  "sandbox",
		Scopes:       []string{"companies.read", "persons.read", "nexus.fraud", "signals.manage"},
		RateLimitRPS: 10,
		ExpiresAt:    time.Now().AddDate(1, 0, 0),
		IsSuspended:  false,
		CreatedAt:    time.Now(),
	}
	r.memoryKeys["sk_test_:55e71616ed6a484ca6c3dd79fa7efef9d3cb5019d651c6b16e4dbdb216a69ef4"] = testKey

	// Live Key: sk_live_demo123
	liveKey := &domain.APIKey{
		ID:           "key_live_1",
		CustomerID:   demoCustomer.ID,
		KeyPrefix:    "sk_live_",
		KeyHash:      "f7cd20a597a7a5840d2446a6fbfbcf52ec77f1fa023e3e0ef861c8a164b38d38",
		SecretHash:   "secret_live_key_123",
		Environment:  "live",
		Scopes:       []string{"companies.read", "persons.read", "nexus.fraud", "signals.manage"},
		RateLimitRPS: 20,
		ExpiresAt:    time.Now().AddDate(0, 3, 0),
		IsSuspended:  false,
		CreatedAt:    time.Now(),
	}
	r.memoryKeys["sk_live_:f7cd20a597a7a5840d2446a6fbfbcf52ec77f1fa023e3e0ef861c8a164b38d38"] = liveKey
}

func (r *postgresAuthRepository) GetAPIKeyByPrefixAndHash(ctx context.Context, prefix, hash string) (*domain.APIKey, error) {
	r.mu.RLock()
	defer r.mu.RUnlock()

	lookupKey := prefix + ":" + hash
	key, exists := r.memoryKeys[lookupKey]
	if !exists {
		return nil, nil
	}
	return key, nil
}

func (r *postgresAuthRepository) GetCustomerByID(ctx context.Context, customerID string) (*domain.Customer, error) {
	r.mu.RLock()
	defer r.mu.RUnlock()

	cust, exists := r.customers[customerID]
	if !exists {
		return nil, nil
	}
	return cust, nil
}

func (r *postgresAuthRepository) LogAPIUsage(ctx context.Context, log *domain.APIUsageLog) error {
	r.mu.Lock()
	defer r.mu.Unlock()
	r.usageLogs = append(r.usageLogs, log)
	return nil
}

func (r *postgresAuthRepository) GetMonthlyUsageCount(ctx context.Context, customerID string, year int, month time.Month) (int, error) {
	r.mu.RLock()
	defer r.mu.RUnlock()
	count := 0
	for _, l := range r.usageLogs {
		if l.CustomerID == customerID && l.Timestamp.Year() == year && l.Timestamp.Month() == month {
			count++
		}
	}
	return count, nil
}

func (r *postgresAuthRepository) CreateCustomer(ctx context.Context, customer *domain.Customer) error {
	r.mu.Lock()
	defer r.mu.Unlock()
	r.customers[customer.ID] = customer
	return nil
}

func (r *postgresAuthRepository) CreateAPIKey(ctx context.Context, apiKey *domain.APIKey) error {
	r.mu.Lock()
	defer r.mu.Unlock()
	lookupKey := apiKey.KeyPrefix + ":" + apiKey.KeyHash
	r.memoryKeys[lookupKey] = apiKey
	return nil
}

func (r *postgresAuthRepository) UpdateAPIKeyStatus(ctx context.Context, keyID string, isSuspended bool) error {
	r.mu.Lock()
	defer r.mu.Unlock()
	for _, k := range r.memoryKeys {
		if k.ID == keyID {
			k.IsSuspended = isSuspended
			break
		}
	}
	return nil
}

func (r *postgresAuthRepository) CreateMobileUser(ctx context.Context, user *domain.MobileUser) error {
	r.mu.Lock()
	defer r.mu.Unlock()
	r.mobileUsers[user.Email] = user
	return nil
}

func (r *postgresAuthRepository) GetMobileUserByEmail(ctx context.Context, email string) (*domain.MobileUser, error) {
	r.mu.RLock()
	defer r.mu.RUnlock()
	user, exists := r.mobileUsers[email]
	if !exists {
		return nil, nil
	}
	return user, nil
}
