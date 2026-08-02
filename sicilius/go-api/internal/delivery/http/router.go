package http

import (
	"github.com/gin-gonic/gin"
	"github.com/turgaykirkil/sicilius-go/internal/delivery/http/handler"
	"github.com/turgaykirkil/sicilius-go/internal/delivery/http/middleware"
	"github.com/turgaykirkil/sicilius-go/internal/domain"
)

func NewRouter(
	companyH *handler.CompanyHandler,
	leadH *handler.LeadHandler,
	personH *handler.PersonHandler,
	nexusH *handler.NexusHandler,
	signalH *handler.SignalHandler,
	authH *handler.AuthHandler,
	gamificationH *handler.GamificationHandler,
	authUseCase domain.AuthUseCase,
) *gin.Engine {
	r := gin.New()
	r.Use(gin.Logger())
	r.Use(gin.Recovery())
	r.Use(middleware.CORSMiddleware())

	// Health Check & SLA Status
	r.GET("/health", func(c *gin.Context) {
		c.JSON(200, gin.H{"status": "ok", "service": "sicilius-go-api", "version": "v2.0.0"})
	})
	r.GET("/api/v2/status", func(c *gin.Context) {
		c.JSON(200, gin.H{
			"status":            "OPERATIONAL",
			"uptime_sla_target": "99.5%",
			"environment":       "production",
		})
	})

	// Legacy / internal v1 API group (Internal Mobile App)
	v1 := r.Group("/api/v1")
	{
		v1.GET("/companies/search", companyH.Search)
		v1.GET("/companies/nearby", companyH.GetNearby)
		v1.GET("/companies/:id", companyH.GetByID)
		v1.GET("/nlp/leads/nearby", leadH.GetNearby)

		// Gamification Endpoints
		gamificationGroup := v1.Group("/gamification")
		{
			gamificationGroup.POST("/check-in", gamificationH.CheckIn)
			gamificationGroup.POST("/self-correct-coordinate", gamificationH.SelfCorrectCoordinate)
			gamificationGroup.GET("/leaderboard", gamificationH.GetLeaderboard)
			gamificationGroup.GET("/daily-quests", gamificationH.GetDailyQuests)
		}
	}

	// Sicilius B2B Enterprise API v2 Group (Protected by Security Layer)
	v2 := r.Group("/api/v2")

	// 0. Public Mobile User Auth Endpoints (No HMAC required for user login/register)
	mobileAuthGroup := v2.Group("/mobile/auth")
	{
		mobileAuthGroup.POST("/register", authH.MobileRegister)
		mobileAuthGroup.POST("/login", authH.MobileLogin)
		mobileAuthGroup.POST("/forgot-password", authH.ForgotPassword)
	}

	// Middlewares for protected API endpoints
	v2.Use(middleware.BusinessHoursMiddleware())
	v2.Use(middleware.SandboxMiddleware())
	v2.Use(middleware.AuditLogMiddleware(authUseCase))

	// 1. Company Endpoints (Scope: companies.read)
	companiesGroup := v2.Group("/companies")
	companiesGroup.Use(middleware.HMACAuthMiddleware(authUseCase, "companies.read"))
	{
		companiesGroup.GET("/search", companyH.Search)
		companiesGroup.GET("/nearby", companyH.GetNearby)
		companiesGroup.GET("/:id", companyH.GetByID)
	}

	// 2. Person & Corporate Relations Endpoints (Scope: persons.read)
	personsGroup := v2.Group("/persons")
	personsGroup.Use(middleware.HMACAuthMiddleware(authUseCase, "persons.read"))
	{
		personsGroup.GET("/search", personH.Search)
		personsGroup.GET("/:id/relations", personH.GetRelations)
	}

	// 3. Nexus Fraud Detection Endpoints (Scope: nexus.fraud)
	nexusGroup := v2.Group("/nexus")
	nexusGroup.Use(middleware.HMACAuthMiddleware(authUseCase, "nexus.fraud"))
	{
		nexusGroup.GET("/company/:id/risk", nexusH.CheckCompanyRisk)
		nexusGroup.GET("/person/:id/risk", nexusH.CheckPersonRisk)
	}

	// 4. Sicilius Signal Engine / Webhooks (Scope: signals.manage)
	signalsGroup := v2.Group("/signals")
	signalsGroup.Use(middleware.HMACAuthMiddleware(authUseCase, "signals.manage"))
	{
		signalsGroup.POST("/rules", signalH.CreateRule)
		signalsGroup.GET("/rules", signalH.GetRules)
		signalsGroup.DELETE("/rules/:id", signalH.DeleteRule)
	}

	// 5. B2B Mobile SDK / Location Services (Scope: mobile.sdk)
	mobileGroup := v2.Group("/mobile")
	mobileGroup.Use(middleware.HMACAuthMiddleware(authUseCase, "mobile.sdk"))
	{
		mobileGroup.GET("/nearby-companies", companyH.GetNearby)
		mobileGroup.GET("/nearby-leads", leadH.GetNearby)
	}

	return r
}
