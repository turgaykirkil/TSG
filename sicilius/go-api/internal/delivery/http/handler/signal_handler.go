package handler

import (
	"net/http"
	"strconv"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/turgaykirkil/sicilius-go/internal/domain"
)

type SignalHandler struct {
	signalUseCase domain.SignalUseCase
}

func NewSignalHandler(signalUseCase domain.SignalUseCase) *SignalHandler {
	return &SignalHandler{
		signalUseCase: signalUseCase,
	}
}

type CreateRuleRequest struct {
	Name       string `json:"name" binding:"required"`
	EventType  string `json:"event_type" binding:"required"`
	TargetVKN  string `json:"target_vkn"`
	WebhookURL string `json:"webhook_url" binding:"required"`
}

func (h *SignalHandler) CreateRule(c *gin.Context) {
	customerVal, exists := c.Get("customer")
	if !exists {
		c.JSON(http.StatusUnauthorized, gin.H{"error": gin.H{"code": "UNAUTHORIZED", "message": "Customer identity missing"}})
		return
	}
	customer := customerVal.(*domain.Customer)

	var req CreateRuleRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": gin.H{
				"code":    "INVALID_BODY",
				"message": "Invalid JSON body or missing required fields (name, event_type, webhook_url)",
				"status":  http.StatusBadRequest,
			},
		})
		return
	}

	rule := &domain.SignalRule{
		ID:         "sig_" + strconv.FormatInt(time.Now().UnixNano(), 10),
		CustomerID: customer.ID,
		Name:       req.Name,
		EventType:  req.EventType,
		TargetVKN:  req.TargetVKN,
		WebhookURL: req.WebhookURL,
		IsActive:   true,
		CreatedAt:  time.Now(),
	}

	if err := h.signalUseCase.RegisterSignalRule(c.Request.Context(), rule); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"error": gin.H{
				"code":    "CREATION_FAILED",
				"message": "Failed to create Signal rule",
				"status":  http.StatusInternalServerError,
			},
		})
		return
	}

	c.JSON(http.StatusCreated, gin.H{
		"message": "Sicilius Signal Engine rule created successfully",
		"rule":    rule,
	})
}

func (h *SignalHandler) GetRules(c *gin.Context) {
	customerVal, exists := c.Get("customer")
	if !exists {
		c.JSON(http.StatusUnauthorized, gin.H{"error": gin.H{"code": "UNAUTHORIZED", "message": "Customer identity missing"}})
		return
	}
	customer := customerVal.(*domain.Customer)

	rules, err := h.signalUseCase.GetCustomerRules(c.Request.Context(), customer.ID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"error": gin.H{"code": "FETCH_FAILED", "message": "Failed to fetch rules"},
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"data":  rules,
		"count": len(rules),
	})
}

func (h *SignalHandler) DeleteRule(c *gin.Context) {
	customerVal, exists := c.Get("customer")
	if !exists {
		c.JSON(http.StatusUnauthorized, gin.H{"error": gin.H{"code": "UNAUTHORIZED", "message": "Customer identity missing"}})
		return
	}
	customer := customerVal.(*domain.Customer)
	ruleID := c.Param("id")

	if err := h.signalUseCase.RemoveSignalRule(c.Request.Context(), ruleID, customer.ID); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"error": gin.H{"code": "DELETE_FAILED", "message": "Failed to delete rule"},
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"message": "Signal rule deleted successfully",
		"id":      ruleID,
	})
}
