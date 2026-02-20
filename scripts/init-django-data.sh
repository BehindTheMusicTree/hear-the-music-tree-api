#!/bin/bash

log_with_script_prefixe () {
    log "[Django data initializer] $1"
}

check_script_vars_are_set() {
  log_with_script_prefixe "Loading environment variables..."
  load_app_env_file_if_exists
  local REQUIRED_NON_BOOL_VARS=(
    API_DIR_NAME
    DB_SUPERUSER_NAME
    DB_SUPERUSER_PASSWORD
    DB_APP_DB_NAME
    DB_APP_USERNAME
    DB_APP_USER_PASSWORD
  )
  check_required_vars_are_set ${REQUIRED_NON_BOOL_VARS[@]}
  check_bool_vars_are_set APP_IS_EXPOSED
  export_value_removing_potential_surrounding_quotes DB_SUPERUSER_PASSWORD
  export_value_removing_potential_surrounding_quotes "DB_APP_USER_PASSWORD"
  log_with_script_prefixe "Environment variables loaded successfully."
}

create_initial_migration_if_needed() {
  MIGRATIONS_DIR="${PROJECT_DIR}${API_DIR_NAME}/migrations/"
  MIGRATION_FILES_COUNT=$(find "${MIGRATIONS_DIR}" -name "*.py" -not -name "__init__.py" 2>/dev/null | wc -l | tr -d ' ')
  
  if [ "$MIGRATION_FILES_COUNT" -eq 0 ]; then
    log_with_script_prefixe "No migration files found. Creating initial migrations..."
    output=$(python3 $MANAGE_SCRIPT makemigrations 2>&1)
    exit_code=$?
    log_with_script_prefixe "$output"
    if [ $exit_code -ne 0 ]; then
      if echo "$output" | grep -q "Connection refused"; then
        log_with_script_prefixe "Failed to create migrations due to database connection issue." >&2
        exit 1
      elif echo "$output" | grep -q "password authentication failed"; then
        log_with_script_prefixe "ERROR: Password authentication failed." >&2
        exit 1
      else
        log_with_script_prefixe "ERROR: makemigrations failed with exit code $exit_code" >&2
        exit 1
      fi
    fi
    log_with_script_prefixe "Migrations created successfully."
  else
    log_with_script_prefixe "Migration files already exist in ${MIGRATIONS_DIR} (found $MIGRATION_FILES_COUNT files). Skipping makemigrations."
    log_with_script_prefixe "Migrations should be committed to version control and applied via 'migrate'."
  fi
}

apply_migrations() {
  log_with_script_prefixe "Applying migrations..."
  output=$(python3 $MANAGE_SCRIPT migrate 2>&1)
  exit_code=$?
  log_with_script_prefixe "$output"
  if [ $exit_code -ne 0 ]; then
    log_with_script_prefixe "ERROR: Failed to apply migrations (exit code $exit_code). Abort" >&2
    exit 1
  fi
  log_with_script_prefixe "Migrations applied successfully."
}

load_initial_fixtures() {
  log_with_script_prefixe "Loading initial data."
  fixtures_dir="${PROJECT_DIR}${API_DIR_NAME}/fixtures"

  if [ ! -d "$fixtures_dir" ]; then
    log_with_script_prefixe "No fixtures directory found at $fixtures_dir. Skipping fixture loading."
    return 0
  fi

  for fixture in "$fixtures_dir"/*.json;
  do
    if [ ! -f "$fixture" ]; then
      continue
    fi
    
    if ! python3 -c "import json, sys; data = json.load(open('$fixture')); sys.exit(0 if (isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict) and 'model' in data[0]) else 1)" 2>/dev/null; then
      log_with_script_prefixe "Skipping $fixture (not a Django fixture format)"
      continue
    fi
    
    log_with_script_prefixe "Loading fixture $fixture ..."
    python3 $MANAGE_SCRIPT loaddata $fixture
    if [ $? -ne 0 ]; then
        log_with_script_prefixe "ERROR: Failed to load initial data from $fixture" >&2
        exit 1
    fi
    log_with_script_prefixe "Fixture $fixture loaded."
  done
  log_with_script_prefixe "Initial data loaded successfully."
}

main (){
  SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
  PROJECT_DIR=$(realpath "${SCRIPTS_DIR}..")/
  source ${SCRIPTS_DIR}utils.sh

  log_with_script_prefixe "Initializing Django data..."

  check_script_vars_are_set

  MANAGE_SCRIPT=${PROJECT_DIR}manage.py
  log_with_script_prefixe "MANAGE_SCRIPT: $MANAGE_SCRIPT"

  bash ${SCRIPTS_DIR}init-db-and-role.sh
  if [ $? -ne 0 ]; then
    log_with_script_prefixe "ERROR: Failed to initialize database and role." >&2
    exit 1
  fi

  create_initial_migration_if_needed
  apply_migrations
  load_initial_fixtures

  unset PGPASSWORD

  log_with_script_prefixe "Django data initialized successfully."
}

main "$@"
