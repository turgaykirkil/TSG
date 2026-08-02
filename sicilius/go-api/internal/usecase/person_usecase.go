package usecase

import (
	"context"

	"github.com/turgaykirkil/sicilius-go/internal/domain"
)

type personUseCase struct {
	personRepo domain.PersonRepository
}

func NewPersonUseCase(personRepo domain.PersonRepository) domain.PersonUseCase {
	return &personUseCase{
		personRepo: personRepo,
	}
}

func (p *personUseCase) SearchPersons(ctx context.Context, query string, limit int) ([]domain.Person, error) {
	return p.personRepo.SearchByNameOrTCKN(ctx, query, limit)
}

func (p *personUseCase) GetPersonRelations(ctx context.Context, personID string) ([]domain.PersonCompanyRelation, error) {
	return p.personRepo.GetCompanyRelations(ctx, personID)
}
