package main

import (
	"context"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/joho/godotenv"

	"github.com/turgaykirkil/sicilius-go/config"
	deliveryHTTP "github.com/turgaykirkil/sicilius-go/internal/delivery/http"
	"github.com/turgaykirkil/sicilius-go/internal/delivery/http/handler"
	"github.com/turgaykirkil/sicilius-go/internal/repository"
	"github.com/turgaykirkil/sicilius-go/internal/usecase"
)

func main() {
	// Load .env if present
	_ = godotenv.Load("../backend/.env", ".env")

	cfg := config.LoadConfig()

	log.Printf("🚀 Starting Sicilius Go API on port %s...", cfg.Port)

	// Context for database initialization
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	// Initialize pgxpool connection
	dbPool, err := pgxpool.New(ctx, cfg.DatabaseURL)
	if err != nil {
		log.Fatalf("❌ Unable to connect to database: %v\n", err)
	}
	defer dbPool.Close()

	// Ping database to ensure connectivity
	if err := dbPool.Ping(ctx); err != nil {
		log.Printf("⚠️ Warning: Database ping failed (Tunnel might be starting): %v\n", err)
	} else {
		log.Println("✅ Database connection pool (pgx v5) successfully initialized!")
	}

	// Clean Architecture Dependency Injection
	companyRepo := repository.NewPostgresCompanyRepository(dbPool)
	leadRepo := repository.NewPostgresLeadRepository(dbPool)
	authRepo := repository.NewPostgresAuthRepository(dbPool)
	personRepo := repository.NewPostgresPersonRepository(dbPool)
	nexusRepo := repository.NewPostgresNexusRepository(dbPool)
	signalRepo := repository.NewPostgresSignalRepository(dbPool)
	gamificationRepo := repository.NewPostgresGamificationRepository(dbPool)

	companyUC := usecase.NewCompanyUseCase(companyRepo)
	leadUC := usecase.NewLeadUseCase(leadRepo)
	authUC := usecase.NewAuthUseCase(authRepo)
	personUC := usecase.NewPersonUseCase(personRepo)
	nexusUC := usecase.NewNexusUseCase(nexusRepo)
	signalUC := usecase.NewSignalUseCase(signalRepo)
	gamificationUC := usecase.NewGamificationUseCase(gamificationRepo)

	companyH := handler.NewCompanyHandler(companyUC)
	leadH := handler.NewLeadHandler(leadUC)
	personH := handler.NewPersonHandler(personUC)
	nexusH := handler.NewNexusHandler(nexusUC)
	signalH := handler.NewSignalHandler(signalUC)
	authH := handler.NewAuthHandler(authUC)
	gamificationH := handler.NewGamificationHandler(gamificationUC)

	// Router setup with Security Layer & Enterprise Endpoints
	router := deliveryHTTP.NewRouter(companyH, leadH, personH, nexusH, signalH, authH, gamificationH, authUC)

	server := &http.Server{
		Addr:         ":" + cfg.Port,
		Handler:      router,
		ReadTimeout:  15 * time.Second,
		WriteTimeout: 15 * time.Second,
		IdleTimeout:  60 * time.Second,
	}

	// Start server in background goroutine
	go func() {
		if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("❌ Server error: %v\n", err)
		}
	}()

	log.Printf("✅ Go API server is listening at http://localhost:%s\n", cfg.Port)

	// Graceful Shutdown Listener
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit

	log.Println("🛑 Shutdown signal received, gracefully stopping Go API server...")

	shutdownCtx, shutdownCancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer shutdownCancel()

	if err := server.Shutdown(shutdownCtx); err != nil {
		log.Fatalf("❌ Server forced to shutdown: %v\n", err)
	}

	log.Println("👋 Go API server stopped cleanly.")
}
