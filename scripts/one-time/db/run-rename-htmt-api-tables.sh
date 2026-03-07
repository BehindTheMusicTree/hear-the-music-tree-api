#!/bin/bash
# One-time: run rename of htmt-api_* tables to htmt_api_*. Requires env (DB_*). Safe to re-run.
# Usage: [ENV_FILE=/path/to/.env] bash run-rename-htmt-api-tables.sh
#   On host: env/.env is loaded if present. In app container: DB_* must be set by orchestrator or pass ENV_FILE.

SCRIPT_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)
SCRIPTS_DIR=$(dirname "$(dirname "$SCRIPT_DIR")")
source "${SCRIPTS_DIR}/utils.sh"

if [ -n "${ENV_FILE}" ] && [ -f "${ENV_FILE}" ]; then
    set -a
    while IFS='=' read -r key value; do
        key="${key#"${key%%[![:space:]]*}"}"
        key="${key%"${key##*[![:space:]]}"}"
        [ -z "$key" ] || [ "${key#\#}" != "$key" ] && continue
        export "$key=$value"
    done < "${ENV_FILE}"
    set +a
else
    load_app_env_file_if_exists
fi

determine_db_host_if_not_set

for var in DB_HOST DB_PORT DB_SUPERUSER_NAME DB_APP_DB_NAME DB_SUPERUSER_PASSWORD; do
    if [ -z "${!var}" ]; then
        echo "ERROR: $var is not set. On host use env/.env. In app container set DB_* (or ENV_FILE=/path/to/.env)." >&2
        exit 1
    fi
done

export_value_removing_potential_surrounding_quotes DB_SUPERUSER_PASSWORD 2>/dev/null || true
export PGPASSWORD="${DB_SUPERUSER_PASSWORD}"

psql -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_SUPERUSER_NAME}" -d "${DB_APP_DB_NAME}" \
  -f "${SCRIPT_DIR}/rename-htmt-api-tables-to-htmt_api.sql"
