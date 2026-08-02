package middleware

import (
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
)

// BusinessHoursMiddleware enforces 08:00 - 20:00 (Europe/Istanbul UTC+3) access restriction for public B2B API endpoints.
func BusinessHoursMiddleware() gin.HandlerFunc {
	location, err := time.LoadLocation("Europe/Istanbul")
	if err != nil {
		location = time.FixedZone("TRT", 3*3600)
	}

	return func(c *gin.Context) {
		// Admin endpoints or bypass header are exempt
		if c.GetBool("is_admin") || c.GetHeader("X-Admin-Bypass") != "" {
			c.Next()
			return
		}

		now := time.Now().In(location)
		hour := now.Hour()

		// 08:00 to 20:00 allowed
		if hour < 8 || hour >= 20 {
			c.JSON(http.StatusServiceUnavailable, gin.H{
				"error": gin.H{
					"code":    "OUT_OF_BUSINESS_HOURS",
					"message": "Sicilius B2B Enterprise API is active between 08:00 and 20:00 (Europe/Istanbul). Access outside business hours is restricted.",
					"status":  http.StatusServiceUnavailable,
				},
			})
			c.Abort()
			return
		}

		c.Next()
	}
}
