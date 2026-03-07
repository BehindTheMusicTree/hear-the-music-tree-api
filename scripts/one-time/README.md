# One-time and maintenance scripts

Scripts here are for one-off or occasional maintenance (e.g. DB renames, data fixes). They are safe to re-run when the condition still applies.

**Organization:** By **domain** (e.g. `db/`, `data/`). Use a subfolder for the kind of change (database schema, data backfills, etc.). Optional: prefix filenames with date (e.g. `2025-03_rename-htmt-api-tables.sql`) for chronology; git history also preserves order.

**How to run (same for all scripts):** Run the runner script (e.g. `run-*.sh`) in the relevant domain folder. Env is loaded automatically (container: orchestrator sets vars; host: `env/.env` if present). If the container has a `.env` mounted elsewhere, use `ENV_FILE=/path/to/.env` before the script.

- **In app container:** `bash /home/app/scripts/one-time/<domain>/<runner>.sh`
- **On host (repo root):** `bash scripts/one-time/<domain>/<runner>.sh`

Scripts that need DB access exit with a clear error if required vars are missing.

## Scripts by domain

### db/

| Script | Description |
|--------|-------------|
| `rename-htmt-api-tables-to-htmt_api.sql` / `run-rename-htmt-api-tables.sh` | Rename tables from `htmt-api_*` to `htmt_api_*`. Run on DBs that still have the old names (e.g. before deploy, or after restore). |
