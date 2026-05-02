#!/bin/bash

log_with_script_prefixe () {
    log "[AFP and DB runner] $1"
}

log_pull_debug () {
    local image_label="$1"
    local debug_timeout=10
    log_with_script_prefixe "--- debug: $image_label pull failed ---"
    log_with_script_prefixe "docker version (timeout ${debug_timeout}s):"
    timeout $debug_timeout docker version 2>&1 | sed 's/^/[AFP and DB runner]   /' || log_with_script_prefixe "   (timed out or failed)"
    hub_code=$(curl -sS --connect-timeout 5 -o /dev/null -w "%{http_code}" https://registry-1.docker.io/v2/ 2>/dev/null) || hub_code="failed"
    log_with_script_prefixe "Docker registry-1.docker.io: HTTP $hub_code"
    ghcr_code=$(curl -sS --connect-timeout 5 -o /dev/null -w "%{http_code}" https://ghcr.io/v2/ 2>/dev/null) || ghcr_code="failed"
    log_with_script_prefixe "GHCR (ghcr.io/v2/): HTTP $ghcr_code"
    log_with_script_prefixe "docker info excerpt (timeout ${debug_timeout}s):"
    timeout $debug_timeout docker info 2>&1 | grep -E "^(Server Version|Operating System|Docker Root Dir|HTTP Proxy|HTTPS Proxy|No Proxy)" | sed 's/^/[AFP and DB runner]   /' || log_with_script_prefixe "   (timed out or no match)"
    log_with_script_prefixe "--- end debug ---"
}

check_script_vars_are_set () {
    load_app_env_file_if_exists

    local REQUIRED_NON_BOOL_VARS=(
        ENV
        GHCR_IMAGE_NAMESPACE
        TMP_UPLOADED_FILES
        DB_CONTAINER_NAME
        DB_IMAGE_REPO
        DB_VERSION
        DB_DATA_DIR
        DB_SUPERUSER_NAME
        DB_SUPERUSER_PASSWORD
        DB_APP_DB_NAME
        DB_APP_USERNAME
        DB_APP_USER_PASSWORD
        DB_PORT
        AFP_CONTAINER_NAME
        AFP_IMAGE_REPO
        AFP_VERSION
        AFP_POOL_DIR_EXTERNAL
        AFP_PORT
    )
    check_required_vars_are_set "${REQUIRED_NON_BOOL_VARS[@]}"
    check_bool_vars_are_set DEBUG APP_IS_EXPOSED DB_DATA_MUST_PERSIST
    export_value_removing_potential_surrounding_quotes DB_SUPERUSER_PASSWORD
    export_value_removing_potential_surrounding_quotes "DB_APP_USER_PASSWORD"
    log_with_script_prefixe "Environment variables loaded successfully."
}

main() {
    SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
    PROJECT_DIR=$(realpath $(dirname "$SCRIPTS_DIR"))/
    APP_ENV_FILE="${ENV_FILE:-}"
    if [ -z "$APP_ENV_FILE" ]; then
        APP_ENV_FILE="${PROJECT_DIR}.env"
    fi
    source "${SCRIPTS_DIR}utils.sh"

    if [ -n "$APP_ENV_FILE" ] && [ -f "$APP_ENV_FILE" ]; then
        set -a
        . "$APP_ENV_FILE"
        set +a
        log_with_script_prefixe "Loaded env from $APP_ENV_FILE"
    fi

    log_with_script_prefixe "Running the database and audio fingerprinter containers..."

    check_script_vars_are_set

    if ! docker info &>/dev/null; then
        log_with_script_prefixe "ERROR: Cannot connect to the Docker daemon. Is Docker running? Start Docker Desktop (or the Docker daemon) and try again." >&2
        exit 1
    fi

    DOCKER_PULL_TIMEOUT=200
    log_with_script_prefixe "Pulling images (timeout ${DOCKER_PULL_TIMEOUT}s each)..."

    db_image=$(docker_image_ref_from_repo_tag "$DB_IMAGE_REPO" "$DB_VERSION")
    log_with_script_prefixe "Pulling DB image: $db_image"
    timeout $DOCKER_PULL_TIMEOUT docker pull "$db_image"
    pull_exit=$?
    if [ $pull_exit -ne 0 ]; then
        if [ $pull_exit -eq 124 ]; then
            log_with_script_prefixe "ERROR: DB image pull timed out after ${DOCKER_PULL_TIMEOUT}s." >&2
        else
            log_with_script_prefixe "ERROR: DB image pull failed (exit $pull_exit). Check: docker login ghcr.io (if private), network, image $db_image." >&2
        fi
        log_pull_debug "DB"
        exit 1
    fi
    log_with_script_prefixe "DB image pulled."

    afp_image=$(docker_image_ref_from_repo_tag "$AFP_IMAGE_REPO" "$AFP_VERSION")
    log_with_script_prefixe "Pulling AFP image: $afp_image"
    timeout $DOCKER_PULL_TIMEOUT docker pull "$afp_image"
    pull_exit=$?
    if [ $pull_exit -ne 0 ]; then
        if [ $pull_exit -eq 124 ]; then
            log_with_script_prefixe "ERROR: AFP image pull timed out after ${DOCKER_PULL_TIMEOUT}s." >&2
        else
            log_with_script_prefixe "ERROR: AFP image pull failed (exit $pull_exit). Check: docker login ghcr.io (if private), network, image $afp_image." >&2
        fi
        log_pull_debug "AFP"
        exit 1
    fi
    log_with_script_prefixe "AFP image pulled."

    log_with_script_prefixe "Images pulled successfully."

    if timeout 10 docker ps -a --format '{{.Names}}' | grep -q "^${DB_CONTAINER_NAME}$"; then
        log_with_script_prefixe "Removing existing database container: $DB_CONTAINER_NAME"
        timeout 30 docker rm -f $DB_CONTAINER_NAME
        if [ $? -ne 0 ]; then
            log_with_script_prefixe "ERROR: Failed to remove database container (timeout or error)." >&2
            exit 1
        fi
        log_with_script_prefixe "Database container removed successfully."
    else
        log_with_script_prefixe "No existing database container to remove."
    fi

    if timeout 10 docker ps -a --format '{{.Names}}' | grep -q "^${AFP_CONTAINER_NAME}$"; then
        log_with_script_prefixe "Removing existing AFP container: $AFP_CONTAINER_NAME"
        timeout 30 docker rm -f $AFP_CONTAINER_NAME
        if [ $? -ne 0 ]; then
            log_with_script_prefixe "ERROR: Failed to remove AFP container (timeout or error)." >&2
            exit 1
        fi
        log_with_script_prefixe "AFP container removed successfully."
    else
        log_with_script_prefixe "No existing AFP container to remove."
    fi

    log_with_script_prefixe "Running the database container..."
    if [ "$DB_DATA_MUST_PERSIST" = true ]; then
        timeout 60 docker run \
            --name=$DB_CONTAINER_NAME \
            --volume=db-data:$DB_DATA_DIR \
            -p $DB_PORT:$DB_PORT \
            -e ENV=$ENV \
            -e POSTGRES_DB=$DB_APP_DB_NAME \
            -e POSTGRES_USER=$DB_SUPERUSER_NAME \
            -e POSTGRES_PASSWORD=$DB_SUPERUSER_PASSWORD \
            -e POSTGRES_PORT=$DB_PORT \
            -d "$db_image"
    else
        timeout 60 docker run \
            --name=$DB_CONTAINER_NAME \
            -p $DB_PORT:$DB_PORT \
            -e ENV=$ENV \
            -e POSTGRES_DB=$DB_APP_DB_NAME \
            -e POSTGRES_USER=$DB_SUPERUSER_NAME \
            -e POSTGRES_PASSWORD=$DB_SUPERUSER_PASSWORD \
            -e POSTGRES_PORT=$DB_PORT \
            -d "$db_image"
    fi
    if [ $? -ne 0 ]; then
        log_with_script_prefixe "ERROR: Failed to run database container (timeout or error)." >&2
        exit 1
    fi
    log_with_script_prefixe "Database container running successfully."

    log_with_script_prefixe "Running the audio fingerprinter container..."
    AFP_RUN_ARGS=(
        --name="$AFP_CONTAINER_NAME"
        --volume="$TMP_UPLOADED_FILES:$AFP_POOL_DIR_EXTERNAL"
        -p "$AFP_PORT:$AFP_PORT"
        -e "ENV=$ENV"
        -e "DEBUG=$DEBUG"
        -e "APP_PORT=$AFP_PORT"
        -e "POOL_DIR_EXTERNAL=$AFP_POOL_DIR_EXTERNAL"
        -e "FLASK_LOG_DIR_EXTERNAL=${AFP_FLASK_LOG_DIR_EXTERNAL:-/app/log/flask/}"
        -e "GUNICORN_LOG_DIR=${AFP_GUNICORN_LOG_DIR_EXTERNAL:-/app/log/gunicorn/}"
        -d "$afp_image"
    )
    if [ "${RUN_AFP_AS_HOST_USER:-false}" = true ]; then
        # Run as host user so the shared pool volume is writable by both AFP and the host (CI runner / local dev).
        # Requires AFP image that supports non-root; point log dirs to container paths that are writable by any UID.
        AFP_RUN_ARGS=(
            --user "$(id -u):$(id -g)"
            "${AFP_RUN_ARGS[@]}"
        )
    fi
    timeout 60 docker run "${AFP_RUN_ARGS[@]}"
    if [ $? -ne 0 ]; then
        log_with_script_prefixe "ERROR: Failed to run audio fingerprinter container (timeout or error)." >&2
        exit 1
    fi
    log_with_script_prefixe "Audio fingerprinter container running successfully."

    DB_HEALTH_MAX_ATTEMPTS=${DB_HEALTH_MAX_ATTEMPTS:-24}
    DB_HEALTH_SLEEP=${DB_HEALTH_SLEEP:-2}
    log_with_script_prefixe "Waiting for DB to be ready (max ${DB_HEALTH_MAX_ATTEMPTS} attempts, ${DB_HEALTH_SLEEP}s apart)..."
    db_attempts=0
    while ! timeout 5 docker exec "$DB_CONTAINER_NAME" pg_isready -h localhost -p "$DB_PORT" -U "$DB_SUPERUSER_NAME" &>/dev/null; do
        if [ "$db_attempts" -ge "$DB_HEALTH_MAX_ATTEMPTS" ]; then
            log_with_script_prefixe "ERROR: DB did not become ready within the expected time." >&2
            log_with_script_prefixe "--- DB container logs ---" >&2
            docker logs "$DB_CONTAINER_NAME" 2>&1 | sed 's/^/[AFP and DB runner]   /' >&2
            exit 1
        fi
        sleep "$DB_HEALTH_SLEEP"
        db_attempts=$((db_attempts + 1))
    done
    log_with_script_prefixe "DB is ready."

    AFP_HEALTH_MAX_ATTEMPTS=${AFP_HEALTH_MAX_ATTEMPTS:-24}
    AFP_HEALTH_SLEEP=${AFP_HEALTH_SLEEP:-2}
    AFP_HEALTH_URL="http://localhost:${AFP_PORT}/health/"
    log_with_script_prefixe "Waiting for AFP to be ready (max ${AFP_HEALTH_MAX_ATTEMPTS} attempts, ${AFP_HEALTH_SLEEP}s apart)..."
    afp_attempts=0
    while ! curl -sf -o /dev/null --connect-timeout 3 "$AFP_HEALTH_URL"; do
        if [ "$afp_attempts" -ge "$AFP_HEALTH_MAX_ATTEMPTS" ]; then
            log_with_script_prefixe "ERROR: AFP did not become ready within the expected time." >&2
            log_with_script_prefixe "--- AFP container logs ---" >&2
            docker logs "$AFP_CONTAINER_NAME" 2>&1 | sed 's/^/[AFP and DB runner]   /' >&2
            exit 1
        fi
        sleep "$AFP_HEALTH_SLEEP"
        afp_attempts=$((afp_attempts + 1))
    done
    log_with_script_prefixe "AFP is ready."

    log_with_script_prefixe "Containers running successfully."

    log_with_script_prefixe "Removing unused Docker images..."
    timeout 30 docker image prune -f
    if [ $? -ne 0 ]; then
        log_with_script_prefixe "ERROR: Failed to remove unused Docker images (timeout or error)." >&2
        exit 1
    fi
    log_with_script_prefixe "Unused Docker images removed successfully."
}

main "$@"
