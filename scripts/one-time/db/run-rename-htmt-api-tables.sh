#!/bin/bash
# One-time: run rename of htmt-api_* tables to htmt_api_*. Requires env (DB_*). Safe to re-run.

SCRIPT_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)
SCRIPTS_DIR=$(dirname "$(dirname "$SCRIPT_DIR")")
source "${SCRIPTS_DIR}/utils.sh"
load_app_env_file_if_exists

export_value_removing_potential_surrounding_quotes DB_SUPERUSER_PASSWORD 2>/dev/null || true
export PGPASSWORD="${DB_SUPERUSER_PASSWORD}"

psql -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_SUPERUSER_NAME}" -d "${DB_APP_DB_NAME}" \
  -f "${SCRIPT_DIR}/rename-htmt-api-tables-to-htmt_api.sql"
