package handler

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/turgaykirkil/sicilius-go/internal/domain"
)

type NexusHandler struct {
	nexusUseCase domain.NexusUseCase
}

func NewNexusHandler(nexusUseCase domain.NexusUseCase) *NexusHandler {
	return &NexusHandler{
		nexusUseCase: nexusUseCase,
	}
}

func (h *NexusHandler) CheckCompanyRisk(c *gin.Context) {
	companyID := c.Param("id")
	if companyID == "" {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": gin.H{
				"code":    "MISSING_COMPANY_ID",
				"message": "Company ID is required for Nexus Risk Analysis",
				"status":  http.StatusBadRequest,
			},
		})
		return
	}

	result, err := h.nexusUseCase.AnalyzeCompanyRisk(c.Request.Context(), companyID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"error": gin.H{
				"code":    "ANALYSIS_FAILED",
				"message": "Nexus Fraud Analysis failed to process",
				"status":  http.StatusInternalServerError,
			},
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"data": result,
	})
}

func (h *NexusHandler) CheckPersonRisk(c *gin.Context) {
	personID := c.Param("id")
	if personID == "" {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": gin.H{
				"code":    "MISSING_PERSON_ID",
				"message": "Person ID is required for Nexus Risk Analysis",
				"status":  http.StatusBadRequest,
			},
		})
		return
	}

	result, err := h.nexusUseCase.AnalyzePersonRisk(c.Request.Context(), personID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"error": gin.H{
				"code":    "ANALYSIS_FAILED",
				"message": "Nexus Fraud Analysis failed to process",
				"status":  http.StatusInternalServerError,
			},
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"data": result,
	})
}
