#!/bin/bash

log_with_script_prefixe () {
    log "[start-server] $1"
}

gunicorn_logs_to_stdout () {
    local v
    v=$(printf '%s' "${GUNICORN_STDOUT_LOGS:-}" | tr '[:upper:]' '[:lower:]')
    [ "$v" = "true" ] || [ "$v" = "1" ] || [ "$v" = "yes" ]
}

check_script_vars_are_set () {
    REQUIRED_NON_BOOL_VARS=(
        PROJECT_DIR
        APP_PORT
        DB_CONTAINER_NAME
        DB_PORT
        DB_CONNECTION_TEST_MAX_ATTEMPTS
        DB_CONNECTION_TEST_SLEEP_INTERVAL
        DB_SUPERUSER_NAME
        DB_SUPERUSER_PASSWORD
        DB_APP_DB_NAME
        DB_APP_USERNAME
        DB_APP_USER_PASSWORD
    )
    if ! gunicorn_logs_to_stdout; then
        REQUIRED_NON_BOOL_VARS+=(
            GUNICORN_LOG_DIR
            GUNICORN_LOG_ERROR_FILENAME
            GUNICORN_LOG_ACCESS_FILENAME
        )
    fi
    check_required_vars_are_set "${REQUIRED_NON_BOOL_VARS[@]}" 2>&1
    if [ $? -ne 0 ]; then
        log_with_script_prefixe "ERROR: Failed to load environment variables." >&2
        exit 1
    fi

    export_value_removing_potential_surrounding_quotes DB_SUPERUSER_PASSWORD 2>&1
    export_value_removing_potential_surrounding_quotes "DB_APP_USER_PASSWORD" 2>&1

    check_bool_vars_are_set DEBUG APP_IS_EXPOSED 2>&1
    if [ $? -ne 0 ]; then
        log_with_script_prefixe "ERROR: Failed to boolean environment variables." >&2
        exit 1
    fi
}

main (){
    SCRIPTS_DIR=${PROJECT_DIR}scripts/
    source ${SCRIPTS_DIR}utils.sh 2>&1

    log_with_script_prefixe "Starting the api container..."

    check_script_vars_are_set 2>&1

    log_with_script_prefixe "Setting up filesystem (for volume mounts)..."
    bash ${SCRIPTS_DIR}setup-filesystem.sh
    if [ $? -ne 0 ]; then
        log_with_script_prefixe "ERROR: Filesystem setup failed." >&2
        exit 1
    fi

    log_with_script_prefixe "Running ${SCRIPTS_DIR}wait-for-postgres-db.sh to wait for the database..."
    bash ${SCRIPTS_DIR}wait-for-postgres-db.sh $DB_CONTAINER_NAME $DB_PORT $DB_CONNECTION_TEST_MAX_ATTEMPTS $DB_CONNECTION_TEST_SLEEP_INTERVAL
    if [ $? -ne 0 ]; then
        log_with_script_prefixe "ERROR: Failed to wait for the database." >&2
        exit 1
    fi
    log_with_script_prefixe "Database is ready"

    log_with_script_prefixe "Running Django system checks..."
    python3 ${PROJECT_DIR}manage.py check
    if [ $? -ne 0 ]; then
        log_with_script_prefixe "ERROR: Django system check failed." >&2
        exit 1
    fi

    if [ -n "${STATIC_FILES:-}" ]; then
        log_with_script_prefixe "Collecting static files into ${STATIC_FILES}..."
        python3 ${PROJECT_DIR}manage.py collectstatic --noinput
        if [ $? -ne 0 ]; then
            log_with_script_prefixe "ERROR: collectstatic failed." >&2
            exit 1
        fi
        log_with_script_prefixe "Static files collected."
    fi

    log_with_script_prefixe "Checking if Django data is initialized..."
    bash ${SCRIPTS_DIR}check-django-initialized.sh
    if [ $? -ne 0 ]; then
        log_with_script_prefixe "Django is not initialized. Initializing (DB/role, migrate)..." >&2
        bash ${SCRIPTS_DIR}init-django-data.sh
        if [ $? -ne 0 ]; then
            log_with_script_prefixe "ERROR: Failed to initialize Django data." >&2
            exit 1
        fi
    else
        log_with_script_prefixe "Django data is already initialized."
    fi

    log_with_script_prefixe "Applying migrations..."
    output=$(python3 ${PROJECT_DIR}manage.py migrate 2>&1)
    exit_code=$?
    log_with_script_prefixe "$output"
    if [ $exit_code -ne 0 ]; then
        log_with_script_prefixe "ERROR: Failed to apply migrations (exit code $exit_code)." >&2
        exit 1
    fi

    log_with_script_prefixe "Starting Gunicorn..."
    if gunicorn_logs_to_stdout; then
        log_with_script_prefixe "Gunicorn access and error logs: stdout/stderr (GUNICORN_STDOUT_LOGS)."
        exec gunicorn api.wsgi:application \
            --bind "0.0.0.0:${APP_PORT}" \
            --access-logfile=- \
            --error-logfile=- \
            --log-level=info 2>&1
    else
        exec gunicorn api.wsgi:application \
            --bind "0.0.0.0:${APP_PORT}" \
            --error-logfile="${GUNICORN_LOG_DIR}${GUNICORN_LOG_ERROR_FILENAME}" \
            --access-logfile="${GUNICORN_LOG_DIR}${GUNICORN_LOG_ACCESS_FILENAME}" \
            --log-level=info 2>&1
    fi
}

main "$@" 2>&1
