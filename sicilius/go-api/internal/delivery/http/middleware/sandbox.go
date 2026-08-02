package middleware

import (
	"github.com/gin-gonic/gin"
)

// SandboxMiddleware sets response headers indicating sandbox execution mode.
func SandboxMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		if c.GetBool("is_sandbox") {
			c.Header("X-Sicilius-Environment", "sandbox")
			c.Header("X-Sicilius-Notice", "This response is generated from the isolated Sandbox environment (test-api.sicilius.com.tr). No live production database was queried.")
		} else {
			c.Header("X-Sicilius-Environment", "live")
		}
		c.Next()
	}
}
