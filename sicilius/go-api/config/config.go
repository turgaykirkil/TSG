package config

import (
	"os"
)

type Config struct {
	Environment string
	Port        string
	DatabaseURL string
	JWTSecret   string
}

func LoadConfig() *Config {
	env := os.Getenv("ENVIRONMENT")
	if env == "" {
		env = "development"
	}

	port := os.Getenv("GO_PORT")
	if port == "" {
		port = "8080"
	}

	dbURL := os.Getenv("TSG_DATABASE_URL")
	if dbURL == "" {
		dbURL = "postgresql://postgres:postgres@127.0.0.1:5434/sicilius"
	}

	jwtSecret := os.Getenv("TSG_SECRET_KEY")
	if jwtSecret == "" {
		jwtSecret = "Sicilius_Secure_Shield_2026_SecureKey"
	}

	return &Config{
		Environment: env,
		Port:        port,
		DatabaseURL: dbURL,
		JWTSecret:   jwtSecret,
	}
}
