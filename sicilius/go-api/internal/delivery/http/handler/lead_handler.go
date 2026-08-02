package handler

import (
	"net/http"
	"strconv"
	"github.com/gin-gonic/gin"
	"github.com/turgaykirkil/sicilius-go/internal/domain"
)

type LeadHandler struct {
	useCase domain.LeadUseCase
}

func NewLeadHandler(uc domain.LeadUseCase) *LeadHandler {
	return &LeadHandler{useCase: uc}
}

func (h *LeadHandler) GetNearby(c *gin.Context) {
	latStr := c.Query("lat")
	lngStr := c.Query("lng")
	radStr := c.Query("radius")

	lat, err1 := strconv.ParseFloat(latStr, 64)
	lng, err2 := strconv.ParseFloat(lngStr, 64)
	radius, err3 := strconv.ParseFloat(radStr, 64)

	if err1 != nil || err2 != nil || err3 != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Geçersiz koordinat veya yarıçap parametresi"})
		return
	}

	leads, err := h.useCase.FindNearby(c.Request.Context(), lat, lng, radius)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, leads)
}
