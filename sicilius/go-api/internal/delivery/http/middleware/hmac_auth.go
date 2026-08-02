package middleware

import (
	"bytes"
	"crypto/hmac"
	"crypto/sha256"
	"encoding/hex"
	"io"
	"net/http"
	"strconv"
	"strings"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/turgaykirkil/sicilius-go/internal/domain"
)

// HMACAuthMiddleware validates API Key, Timestamp (anti-replay) and HMAC signature.
func HMACAuthMiddleware(authUseCase domain.AuthUseCase, requiredScope string) gin.HandlerFunc {
	return func(c *gin.Context) {
		apiKeyHeader := c.GetHeader("X-API-Key")
		timestampHeader := c.GetHeader("X-Timestamp")
		signatureHeader := c.GetHeader("X-Signature")

		if apiKeyHeader == "" {
			c.JSON(http.StatusUnauthorized, gin.H{
				"error": gin.H{
					"code":    "MISSING_API_KEY",
					"message": "X-API-Key header is required",
					"status":  http.StatusUnauthorized,
				},
			})
			c.Abort()
			return
		}

		// Detect environment (live vs test)
		isSandbox := strings.HasPrefix(apiKeyHeader, "sk_test_")
		isLive := strings.HasPrefix(apiKeyHeader, "sk_live_")

		if !isSandbox && !isLive {
			c.JSON(http.StatusUnauthorized, gin.H{
				"error": gin.H{
					"code":    "INVALID_API_KEY_FORMAT",
					"message": "API key must start with 'sk_live_' or 'sk_test_'",
					"status":  http.StatusUnauthorized,
				},
			})
			c.Abort()
			return
		}

		// Anti-Replay: Verify Timestamp (within 5 minutes window)
		if timestampHeader != "" {
			ts, err := strconv.ParseInt(timestampHeader, 10, 64)
			if err != nil || time.Now().Unix()-ts > 300 || ts-time.Now().Unix() > 300 {
				c.JSON(http.StatusUnauthorized, gin.H{
					"error": gin.H{
						"code":    "EXPIRED_TIMESTAMP",
						"message": "X-Timestamp is expired or invalid (must be within 5 minutes)",
						"status":  http.StatusUnauthorized,
					},
				})
				c.Abort()
				return
			}
		}

		// Hash of key for DB lookup
		hasher := sha256.New()
		hasher.Write([]byte(apiKeyHeader))
		keyHash := hex.EncodeToString(hasher.Sum(nil))

		prefix := "sk_live_"
		if isSandbox {
			prefix = "sk_test_"
		}

		apiKeyObj, customer, err := authUseCase.ValidateAPIKey(c.Request.Context(), prefix, keyHash)
		if err != nil || apiKeyObj == nil {
			c.JSON(http.StatusUnauthorized, gin.H{
				"error": gin.H{
					"code":    "UNAUTHORIZED",
					"message": "Invalid or expired API Key",
					"status":  http.StatusUnauthorized,
				},
			})
			c.Abort()
			return
		}

		if apiKeyObj.IsSuspended {
			c.JSON(http.StatusForbidden, gin.H{
				"error": gin.H{
					"code":    "KEY_SUSPENDED",
					"message": "This API Key has been suspended",
					"status":  http.StatusForbidden,
				},
			})
			c.Abort()
			return
		}

		if time.Now().After(apiKeyObj.ExpiresAt) {
			c.JSON(http.StatusUnauthorized, gin.H{
				"error": gin.H{
					"code":    "KEY_EXPIRED",
					"message": "API Key has expired. Please rotate your API key in the portal.",
					"status":  http.StatusUnauthorized,
				},
			})
			c.Abort()
			return
		}

		// Scope Check
		if requiredScope != "" {
			scopeFound := false
			for _, s := range apiKeyObj.Scopes {
				if s == requiredScope || s == "*" || s == "admin" {
					scopeFound = true
					break
				}
			}
			if !scopeFound {
				c.JSON(http.StatusForbidden, gin.H{
					"error": gin.H{
						"code":    "INSUFFICIENT_SCOPE",
						"message": "API Key lacks required scope: " + requiredScope,
						"status":  http.StatusForbidden,
					},
				})
				c.Abort()
				return
			}
		}

		// HMAC Signature Verification if signature header present
		if signatureHeader != "" && timestampHeader != "" {
			bodyBytes, _ := io.ReadAll(c.Request.Body)
			c.Request.Body = io.NopCloser(bytes.NewBuffer(bodyBytes))

			mac := hmac.New(sha256.New, []byte(apiKeyObj.SecretHash))
			message := c.Request.Method + c.Request.URL.Path + timestampHeader + string(bodyBytes)
			mac.Write([]byte(message))
			expectedSignature := hex.EncodeToString(mac.Sum(nil))

			if !hmac.Equal([]byte(signatureHeader), []byte(expectedSignature)) {
				c.JSON(http.StatusUnauthorized, gin.H{
					"error": gin.H{
						"code":    "INVALID_SIGNATURE",
						"message": "HMAC-SHA256 signature verification failed",
						"status":  http.StatusUnauthorized,
					},
				})
				c.Abort()
				return
			}
		}

		// Set context values
		c.Set("api_key", apiKeyObj)
		c.Set("customer", customer)
		c.Set("is_sandbox", isSandbox)

		c.Next()
	}
}
