package usecase

import (
	"context"
	"crypto/hmac"
	"crypto/sha256"
	"encoding/hex"
	"errors"
	"strings"
	"time"

	"github.com/turgaykirkil/sicilius-go/internal/domain"
	"golang.org/x/crypto/bcrypt"
)

type authUseCase struct {
	authRepo domain.AuthRepository
}

func NewAuthUseCase(authRepo domain.AuthRepository) domain.AuthUseCase {
	return &authUseCase{
		authRepo: authRepo,
	}
}

func (a *authUseCase) ValidateAPIKey(ctx context.Context, keyPrefix, keyHash string) (*domain.APIKey, *domain.Customer, error) {
	apiKey, err := a.authRepo.GetAPIKeyByPrefixAndHash(ctx, keyPrefix, keyHash)
	if err != nil || apiKey == nil {
		return nil, nil, err
	}

	customer, err := a.authRepo.GetCustomerByID(ctx, apiKey.CustomerID)
	if err != nil || customer == nil {
		return apiKey, nil, nil
	}

	return apiKey, customer, nil
}

func (a *authUseCase) VerifyHMACSignature(secret, method, path, timestamp, body, signature string) bool {
	mac := hmac.New(sha256.New, []byte(secret))
	message := method + path + timestamp + body
	mac.Write([]byte(message))
	expected := hex.EncodeToString(mac.Sum(nil))
	return hmac.Equal([]byte(signature), []byte(expected))
}

func (a *authUseCase) LogRequestUsage(ctx context.Context, log *domain.APIUsageLog) error {
	return a.authRepo.LogAPIUsage(ctx, log)
}

func (a *authUseCase) IsWithinBusinessHours(t time.Time) bool {
	loc, err := time.LoadLocation("Europe/Istanbul")
	if err != nil {
		loc = time.FixedZone("TRT", 3*3600)
	}
	trTime := t.In(loc)
	hour := trTime.Hour()
	return hour >= 8 && hour < 20
}

func (a *authUseCase) RegisterMobileUser(ctx context.Context, fullName, email, password, companyTitle string) (*domain.MobileUser, error) {
	cleanEmail := strings.ToLower(strings.TrimSpace(email))
	existing, _ := a.authRepo.GetMobileUserByEmail(ctx, cleanEmail)
	if existing != nil {
		return nil, errors.New("EMAIL_ALREADY_EXISTS")
	}

	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
	if err != nil {
		return nil, err
	}

	newUser := &domain.MobileUser{
		ID:              "muser_" + hex.EncodeToString([]byte(cleanEmail))[:12],
		FullName:        fullName,
		Email:           cleanEmail,
		PasswordHash:    string(hashedPassword),
		CompanyTitle:    companyTitle,
		Source:          "mobile",
		CanAccessWeb:    false, // CRITICAL RULE: Mobile signups CANNOT access Web platform!
		CanAccessMobile: true,  // True for all
		IsActive:        true,
		CreatedAt:       time.Now(),
	}

	if err := a.authRepo.CreateMobileUser(ctx, newUser); err != nil {
		return nil, err
	}

	return newUser, nil
}

func (a *authUseCase) LoginMobileUser(ctx context.Context, email, password string) (*domain.MobileLoginResponse, error) {
	cleanEmail := strings.ToLower(strings.TrimSpace(email))
	user, err := a.authRepo.GetMobileUserByEmail(ctx, cleanEmail)
	if err != nil || user == nil {
		return nil, errors.New("INVALID_CREDENTIALS")
	}

	if err := bcrypt.CompareHashAndPassword([]byte(user.PasswordHash), []byte(password)); err != nil {
		return nil, errors.New("INVALID_CREDENTIALS")
	}

	if !user.IsActive {
		return nil, errors.New("USER_INACTIVE")
	}

	token := "mtoken_" + hex.EncodeToString([]byte(cleanEmail+"_"+time.Now().String()))[:32]

	return &domain.MobileLoginResponse{
		Token:        token,
		User:         user,
		CanAccessWeb: user.CanAccessWeb,
	}, nil
}

func (a *authUseCase) ForgotPassword(ctx context.Context, email string) error {
	cleanEmail := strings.ToLower(strings.TrimSpace(email))
	_, err := a.authRepo.GetMobileUserByEmail(ctx, cleanEmail)
	if err != nil {
		// Silent success to prevent user enumeration
		return nil
	}
	// Trigger reset email delivery
	return nil
}
