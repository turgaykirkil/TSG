package handler

import (
	"net/http"
	"github.com/gin-gonic/gin"
	"github.com/turgaykirkil/sicilius-go/internal/domain"
)

type GamificationHandler struct {
	useCase domain.GamificationUseCase
}

func NewGamificationHandler(uc domain.GamificationUseCase) *GamificationHandler {
	return &GamificationHandler{useCase: uc}
}

func (h *GamificationHandler) CheckIn(c *gin.Context) {
	userID := c.GetString("user_id")
	if userID == "" {
		userID = "00000000-0000-0000-0000-000000000001" // Fallback user ID for testing
	}

	var req domain.CheckInRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Geçersiz istek gövdesi: " + err.Error()})
		return
	}

	res, err := h.useCase.PerformCheckIn(c.Request.Context(), userID, req)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, res)
}

func (h *GamificationHandler) SelfCorrectCoordinate(c *gin.Context) {
	userID := c.GetString("user_id")
	if userID == "" {
		userID = "00000000-0000-0000-0000-000000000001"
	}

	var req domain.CoordinateCorrectionRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Geçersiz istek gövdesi: " + err.Error()})
		return
	}

	res, err := h.useCase.SelfCorrectCoordinate(c.Request.Context(), userID, req)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, res)
}

func (h *GamificationHandler) GetLeaderboard(c *gin.Context) {
	userID := c.GetString("user_id")
	if userID == "" {
		userID = "00000000-0000-0000-0000-000000000001"
	}

	res, err := h.useCase.GetLeaderboard(c.Request.Context(), userID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, res)
}

func (h *GamificationHandler) GetDailyQuests(c *gin.Context) {
	userID := c.GetString("user_id")
	if userID == "" {
		userID = "00000000-0000-0000-0000-000000000001"
	}

	res, err := h.useCase.GetDailyQuests(c.Request.Context(), userID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, res)
}
