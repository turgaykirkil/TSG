package handler

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/turgaykirkil/sicilius-go/internal/domain"
)

type AuthHandler struct {
	authUseCase domain.AuthUseCase
}

func NewAuthHandler(authUseCase domain.AuthUseCase) *AuthHandler {
	return &AuthHandler{
		authUseCase: authUseCase,
	}
}

type MobileRegisterRequest struct {
	FullName     string `json:"full_name" binding:"required"`
	Email        string `json:"email" binding:"required"`
	Password     string `json:"password" binding:"required"`
	CompanyTitle string `json:"company_title"`
}

func (h *AuthHandler) MobileRegister(c *gin.Context) {
	var req MobileRegisterRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": gin.H{
				"code":    "INVALID_INPUT",
				"message": "Full name, email and password are required",
				"status":  http.StatusBadRequest,
			},
		})
		return
	}

	user, err := h.authUseCase.RegisterMobileUser(c.Request.Context(), req.FullName, req.Email, req.Password, req.CompanyTitle)
	if err != nil {
		if err.Error() == "EMAIL_ALREADY_EXISTS" {
			c.JSON(http.StatusConflict, gin.H{
				"error": gin.H{
					"code":    "EMAIL_EXISTS",
					"message": "This email address is already registered",
					"status":  http.StatusConflict,
				},
			})
			return
		}

		c.JSON(http.StatusInternalServerError, gin.H{
			"error": gin.H{
				"code":    "REGISTRATION_FAILED",
				"message": "Failed to create mobile user account",
				"status":  http.StatusInternalServerError,
			},
		})
		return
	}

	c.JSON(http.StatusCreated, gin.H{
		"message":        "Mobile user account created successfully",
		"user":           user,
		"can_access_web": user.CanAccessWeb,
		"notice":         "Mobile accounts can only access the mobile application. Web platform access requires an invitation.",
	})
}

type MobileLoginRequest struct {
	Email    string `json:"email" binding:"required"`
	Password string `json:"password" binding:"required"`
}

func (h *AuthHandler) MobileLogin(c *gin.Context) {
	var req MobileLoginRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": gin.H{
				"code":    "INVALID_INPUT",
				"message": "Email and password are required",
				"status":  http.StatusBadRequest,
			},
		})
		return
	}

	resp, err := h.authUseCase.LoginMobileUser(c.Request.Context(), req.Email, req.Password)
	if err != nil {
		c.JSON(http.StatusUnauthorized, gin.H{
			"error": gin.H{
				"code":    "INVALID_CREDENTIALS",
				"message": "Invalid email or password",
				"status":  http.StatusUnauthorized,
			},
		})
		return
	}

	c.JSON(http.StatusOK, resp)
}

type ForgotPasswordRequest struct {
	Email string `json:"email" binding:"required"`
}

func (h *AuthHandler) ForgotPassword(c *gin.Context) {
	var req ForgotPasswordRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": gin.H{
				"code":    "INVALID_INPUT",
				"message": "Email is required",
				"status":  http.StatusBadRequest,
			},
		})
		return
	}

	_ = h.authUseCase.ForgotPassword(c.Request.Context(), req.Email)

	c.JSON(http.StatusOK, gin.H{
		"message": "Password reset instructions have been sent to your email address if an account exists.",
	})
}
