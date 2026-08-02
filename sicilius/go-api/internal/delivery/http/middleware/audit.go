package middleware

import (
	"time"

	"github.com/gin-gonic/gin"
	"github.com/turgaykirkil/sicilius-go/internal/domain"
)

// AuditLogMiddleware records API usage logs after response completion.
func AuditLogMiddleware(authUseCase domain.AuthUseCase) gin.HandlerFunc {
	return func(c *gin.Context) {
		startTime := time.Now()

		c.Next()

		duration := time.Since(startTime).Milliseconds()

		apiKeyVal, exists := c.Get("api_key")
		if !exists {
			return
		}

		apiKeyObj, ok := apiKeyVal.(*domain.APIKey)
		if !ok || apiKeyObj == nil {
			return
		}

		customerVal, _ := c.Get("customer")
		customerObj, _ := customerVal.(*domain.Customer)

		customerID := ""
		if customerObj != nil {
			customerID = customerObj.ID
		}

		logEntry := &domain.APIUsageLog{
			CustomerID:     customerID,
			APIKeyID:       apiKeyObj.ID,
			Endpoint:       c.Request.URL.Path,
			HTTPMethod:     c.Request.Method,
			StatusCode:     c.Writer.Status(),
			ResponseTimeMS: duration,
			Timestamp:      startTime,
		}

		// Asynchronous log save
		go func(log *domain.APIUsageLog) {
			_ = authUseCase.LogRequestUsage(c.Request.Context(), log)
		}(logEntry)
	}
}
