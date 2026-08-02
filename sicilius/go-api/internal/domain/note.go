package domain

import (
	"context"
	"time"
)

type CustomerNote struct {
	ID         string    `json:"id"`
	CustomerID string    `json:"customer_id"`
	UserID     *string   `json:"user_id,omitempty"`
	NoteType   string    `json:"note_type"`
	Content    string    `json:"content"`
	CreatedAt  time.Time `json:"created_at"`
}

type CustomerNoteRepository interface {
	GetByCustomerID(ctx context.Context, customerID string) ([]CustomerNote, error)
	Create(ctx context.Context, note *CustomerNote) error
}

type CustomerNoteUsecase interface {
	GetByCustomerID(ctx context.Context, customerID string) ([]CustomerNote, error)
	Create(ctx context.Context, note *CustomerNote) error
}
