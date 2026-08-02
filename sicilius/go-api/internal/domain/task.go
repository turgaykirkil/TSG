package domain

import (
	"context"
	"time"
)

type Task struct {
	ID           string    `json:"id"`
	Title        string    `json:"title"`
	Description  string    `json:"description"`
	DueDate      time.Time `json:"due_date"`
	Priority     string    `json:"priority"`
	Status       string    `json:"status"`
	Progress     int       `json:"progress"`
	CustomerID   *string   `json:"customer_id,omitempty"`
	CustomerName string    `json:"customer_name,omitempty"`
	AssignedTo   *string   `json:"assigned_to,omitempty"`
	AssigneeName string    `json:"assignee_name,omitempty"`
	CreatedAt    time.Time `json:"created_at"`
	UpdatedAt    time.Time `json:"updated_at"`
}

type TaskRepository interface {
	GetAll(ctx context.Context, status, priority string) ([]Task, error)
	GetByID(ctx context.Context, id string) (*Task, error)
	Create(ctx context.Context, task *Task) error
	Update(ctx context.Context, task *Task) error
	Delete(ctx context.Context, id string) error
}

type TaskUsecase interface {
	GetAll(ctx context.Context, status, priority string) ([]Task, error)
	GetByID(ctx context.Context, id string) (*Task, error)
	Create(ctx context.Context, task *Task) error
	Update(ctx context.Context, task *Task) error
	Delete(ctx context.Context, id string) error
}
