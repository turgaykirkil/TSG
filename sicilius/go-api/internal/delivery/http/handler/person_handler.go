package handler

import (
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
	"github.com/turgaykirkil/sicilius-go/internal/domain"
)

type PersonHandler struct {
	personUseCase domain.PersonUseCase
}

func NewPersonHandler(personUseCase domain.PersonUseCase) *PersonHandler {
	return &PersonHandler{
		personUseCase: personUseCase,
	}
}

func (h *PersonHandler) Search(c *gin.Context) {
	query := c.Query("q")
	if query == "" {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": gin.H{
				"code":    "MISSING_QUERY",
				"message": "Query parameter 'q' (name or TCKN) is required",
				"status":  http.StatusBadRequest,
			},
		})
		return
	}

	limit, _ := strconv.Atoi(c.DefaultQuery("limit", "10"))
	if limit > 50 {
		limit = 50
	}

	persons, err := h.personUseCase.SearchPersons(c.Request.Context(), query, limit)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"error": gin.H{
				"code":    "INTERNAL_ERROR",
				"message": "Failed to search persons",
				"status":  http.StatusInternalServerError,
			},
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"data":  persons,
		"count": len(persons),
	})
}

func (h *PersonHandler) GetRelations(c *gin.Context) {
	personID := c.Param("id")
	if personID == "" {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": gin.H{
				"code":    "MISSING_ID",
				"message": "Person ID is required",
				"status":  http.StatusBadRequest,
			},
		})
		return
	}

	relations, err := h.personUseCase.GetPersonRelations(c.Request.Context(), personID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"error": gin.H{
				"code":    "INTERNAL_ERROR",
				"message": "Failed to retrieve corporate relations",
				"status":  http.StatusInternalServerError,
			},
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"person_id": personID,
		"relations": relations,
		"count":     len(relations),
	})
}
