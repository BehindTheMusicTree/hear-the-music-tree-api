# One-time and maintenance scripts

Scripts here are for one-off or occasional maintenance (e.g. DB renames, data fixes). They are safe to re-run when the condition still applies.

**Organization:** By **domain** (e.g. `db/`, `data/`). Use a subfolder for the kind of change (database schema, data backfills, etc.). Optional: prefix filenames with date (e.g. `2025-03_rename-htmt-api-tables.sql`) for chronology; git history also preserves order.

**How to run:** From repo root, with env loaded (e.g. from `env/.env`). Example:

```bash
bash scripts/one-time/db/run-rename-htmt-api-tables.sh
```

## Scripts by domain

### db/

| Script | Description |
|--------|-------------|
| `rename-htmt-api-tables-to-htmt_api.sql` / `run-rename-htmt-api-tables.sh` | Rename tables from `htmt-api_*` to `htmt_api_*`. Run on DBs that still have the old names (e.g. before deploy, or after restore). |
