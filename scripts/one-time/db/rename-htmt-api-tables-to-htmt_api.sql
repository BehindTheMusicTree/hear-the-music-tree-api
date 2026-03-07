-- One-time: rename tables htmt-api_* → htmt_api_*. Safe to re-run (no-op if already renamed).
-- Run with: psql -U <user> -d <dbname> -f scripts/one-time/db/rename-htmt-api-tables-to-htmt_api.sql

DO $$
DECLARE
    r RECORD;
    new_name text;
BEGIN
    FOR r IN
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
          AND table_name LIKE 'htmt-api_%'
    LOOP
        new_name := replace(r.table_name, 'htmt-api_', 'htmt_api_');
        EXECUTE format('ALTER TABLE public.%I RENAME TO %I', r.table_name, new_name);
        RAISE NOTICE 'Renamed % to %', r.table_name, new_name;
    END LOOP;
END $$;
