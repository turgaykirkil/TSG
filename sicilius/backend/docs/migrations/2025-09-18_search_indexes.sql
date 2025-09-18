-- Enable necessary extensions
create extension if not exists unaccent with schema public;
create extension if not exists pg_trgm;

-- Companies: indexes for case/diacritic-insensitive and typo-tolerant search
-- Use expression indexes to avoid schema changes; fast and backwards compatible.
create index if not exists idx_companies_unvan_unaccent_trgm
  on public.companies using gin ((unaccent(lower(coalesce(unvan, '')))) gin_trgm_ops);

create index if not exists idx_companies_sicil_no_unaccent_trgm
  on public.companies using gin ((unaccent(lower(coalesce(sicil_no, '')))) gin_trgm_ops);

create index if not exists idx_companies_address_unaccent_trgm
  on public.companies using gin ((unaccent(lower(coalesce(address, '')))) gin_trgm_ops);

-- Optional: full-text search surface (can be enabled later if needed)
-- create index if not exists idx_companies_unvan_tsv_gin
--   on public.companies using gin (to_tsvector('simple', unaccent(coalesce(unvan, ''))));

-- Notes:
-- - These indexes accelerate ILIKE/substring similarity searches used by unified search endpoints.
-- - They do not change data; safe to create concurrently in production if needed:
--     CREATE INDEX CONCURRENTLY ... (requires running outside a transaction)
-- - If applying on large tables, prefer off-peak times and CONCURRENTLY variant to avoid long locks.
