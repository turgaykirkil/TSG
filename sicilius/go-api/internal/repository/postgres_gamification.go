package repository

import (
	"context"
	"fmt"
	"math"
	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/turgaykirkil/sicilius-go/internal/domain"
)

type postgresGamificationRepository struct {
	db *pgxpool.Pool
}

func NewPostgresGamificationRepository(db *pgxpool.Pool) domain.GamificationRepository {
	return &postgresGamificationRepository{db: db}
}

func (r *postgresGamificationRepository) GetCustomerCoordinates(ctx context.Context, customerID string) (float64, float64, error) {
	query := `
		SELECT COALESCE(latitude, 0.0), COALESCE(longitude, 0.0)
		FROM app.b2b_customers
		WHERE id::text = $1
	`
	var lat, lon float64
	err := r.db.QueryRow(ctx, query, customerID).Scan(&lat, &lon)
	if err != nil {
		return 0, 0, nil
	}
	return lat, lon, nil
}

func (r *postgresGamificationRepository) GetUserStats(ctx context.Context, userID string) (*domain.UserGamificationStats, error) {
	query := `
		SELECT id::text, user_id::text, xp_points, streak_days, last_checkin_date, current_league, current_level, created_at, updated_at
		FROM app.user_gamification_stats
		WHERE user_id::text = $1
	`
	var s domain.UserGamificationStats
	err := r.db.QueryRow(ctx, query, userID).Scan(
		&s.ID, &s.UserID, &s.XPPoints, &s.StreakDays, &s.LastCheckInDate, &s.CurrentLeague, &s.CurrentLevel, &s.CreatedAt, &s.UpdatedAt,
	)
	if err != nil {
		return nil, err
	}
	return &s, nil
}

func (r *postgresGamificationRepository) UpsertUserStats(ctx context.Context, stats *domain.UserGamificationStats) error {
	query := `
		INSERT INTO app.user_gamification_stats (user_id, xp_points, streak_days, last_checkin_date, current_league, current_level, updated_at)
		VALUES ($1::uuid, $2, $3, $4, $5, $6, NOW())
		ON CONFLICT (user_id) DO UPDATE
		SET xp_points = EXCLUDED.xp_points,
		    streak_days = EXCLUDED.streak_days,
		    last_checkin_date = EXCLUDED.last_checkin_date,
		    current_league = EXCLUDED.current_league,
		    current_level = EXCLUDED.current_level,
		    updated_at = NOW()
	`
	_, err := r.db.Exec(ctx, query, stats.UserID, stats.XPPoints, stats.StreakDays, stats.LastCheckInDate, stats.CurrentLeague, stats.CurrentLevel)
	return err
}

func (r *postgresGamificationRepository) LogXPAudit(ctx context.Context, userID, actionType string, points int, metadata string) error {
	query := `
		INSERT INTO app.xp_audit_logs (user_id, action_type, points_awarded, metadata_json)
		VALUES ($1::uuid, $2, $3, $4::jsonb)
	`
	_, err := r.db.Exec(ctx, query, userID, actionType, points, metadata)
	return err
}

func (r *postgresGamificationRepository) UpdateCompanyCoordinates(ctx context.Context, companyID string, lat, lon float64) error {
	query := `
		UPDATE app.companies
		SET lat = $1, lon = $2, updated_at = NOW()
		WHERE id::text = $3
	`
	_, err := r.db.Exec(ctx, query, lat, lon, companyID)
	return err
}

func (r *postgresGamificationRepository) GetPrivacyLeaderboard(ctx context.Context, userID string) (*domain.PrivacyLeaderboardResponse, error) {
	query := `
		SELECT user_id::text, xp_points, current_league
		FROM app.user_gamification_stats
		ORDER BY xp_points DESC
		LIMIT 50
	`
	rows, err := r.db.Query(ctx, query)
	if err != nil {
		return nil, fmt.Errorf("gamification repo: failed leaderboard query: %w", err)
	}
	defer rows.Close()

	rankings := make([]domain.LeaderboardRankItem, 0)
	myRank := 1
	myXP := 0
	myLeague := "Bronz Ligi"
	idx := 1

	for rows.Next() {
		var uID string
		var xp int
		var league string

		if err := rows.Scan(&uID, &xp, &league); err != nil {
			continue
		}

		isMe := (uID == userID)
		label := fmt.Sprintf("Temsilci #%d", idx*17+3)
		if isMe {
			label = "SEN"
			myRank = idx
			myXP = xp
			myLeague = league
		}

		rankings = append(rankings, domain.LeaderboardRankItem{
			Rank:           idx,
			AnonymousLabel: label,
			XP:             xp,
			IsCurrentUser:  isMe,
		})
		idx++
	}

	percentile := int(math.Max(1, math.Ceil(float64(myRank)/float64(math.Max(float64(len(rankings)), 1))*100)))

	return &domain.PrivacyLeaderboardResponse{
		MyRank:         myRank,
		MyXP:           myXP,
		MyLeague:       myLeague,
		PercentileText: fmt.Sprintf("Top %%%d dilimdesin!", percentile),
		Rankings:       rankings,
	}, nil
}
