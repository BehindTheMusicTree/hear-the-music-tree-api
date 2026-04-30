#!/bin/bash

log_with_script_prefixe () {
    log "[Filesystem setter] $1"
}

check_script_vars_are_set () {
    log_with_script_prefixe "Loading environment variables for the filesystem setup..."
    load_app_env_file_if_exists
    check_required_vars_are_set ENV
    check_bool_vars_are_set APP_IS_EXPOSED
    if [ "$ENV" = "collect_static" ]; then
        check_required_vars_are_set STATIC_FILES
    else
        check_required_vars_are_set MEDIA_DIR LIBRARIES_DIR TMP_UPLOADED_FILES
    fi
    log_with_script_prefixe "Environment variables loaded for the filesystem setup."
}

setup_static_files_for_collection() {
    local static_files_dir="${STATIC_FILES}"
    log_with_script_prefixe "ENV is set to collect_static. Setting up the filesystem..."
    create_directory_if_not_exists_or_exit "$static_files_dir"
    log_with_script_prefixe "Checking if files exist in $static_files_dir..."
    if [ -z "$(ls -A $static_files_dir)" ]; then
        log_with_script_prefixe "No files found in $static_files_dir."
    else
        log_with_script_prefixe "Files found in $static_files_dir. Removing them..."
        output=$(rm -rf "$static_files_dir"/*)
        if [ $? -ne 0 ]; then
            log_with_script_prefixe "ERROR: Failed to remove files from $static_files_dir: $output" >&2
            exit 1
        fi
        log_with_script_prefixe "Files removed from $static_files_dir."
    fi
}

setup_static_files_for_serving() {
    if [ -z "${STATIC_FILES:-}" ]; then
        log_with_script_prefixe "ENV is not set to collect_static and STATIC_FILES is not set. Static files are not needed."
        return
    fi
    log_with_script_prefixe "STATIC_FILES is set to $STATIC_FILES. Ensuring runtime static directory exists..."
    create_directory_if_not_exists_or_exit "$STATIC_FILES"
    set_read_write_permissions_and_owner_or_exit "$STATIC_FILES"
    log_with_script_prefixe "Runtime static directory is set up."
}
setup_django_log () {
    if [ -n "$DJANGO_LOG_DIR" ]; then
        log_with_script_prefixe "DJANGO_LOG_DIR is set. Setting Django logs dirextories and files."
        create_directory_if_not_exists_or_exit "$DJANGO_LOG_DIR"

        local LOG_FILENAMES=(
            DJANGO_LOG_GENERAL_FILENAME
            DJANGO_LOG_INFO_FILENAME
            DJANGO_LOG_REQUESTS_FILENAME
            DJANGO_LOG_REQUESTS_DEBUG_FILENAME
            DJANGO_LOG_EXCEPTIONS_FILENAME
            DJANGO_LOG_DJANGO_FILENAME
            DJANGO_LOG_APP_FILENAME
        )
        for log_filename in "${LOG_FILENAMES[@]}"; do
            check_required_vars_are_set "$log_filename"
            touch_file_or_exit "${DJANGO_LOG_DIR%/}/${!log_filename}"
        done
        set_read_write_permissions_and_owner_or_exit "$DJANGO_LOG_DIR"
    else
        log_with_script_prefixe "DJANGO_LOG_DIR is not set. Django logs are not needed."
    fi
}

setup_gunicorn_log () {
    if [ "$APP_IS_EXPOSED" = "true" ]; then
        log_with_script_prefixe "App is exposed. Setting up Gunicorn logs."
        REQUIRED_NON_BOOL_VARS=(
            GUNICORN_LOG_DIR
            GUNICORN_LOG_ERROR_FILENAME
            GUNICORN_LOG_ACCESS_FILENAME
        )
        for var_name in "${REQUIRED_NON_BOOL_VARS[@]}"; do
            check_required_vars_are_set "$var_name"
        done

        GUNICORN_LOG_ERROR_FILE="${GUNICORN_LOG_DIR%/}/${GUNICORN_LOG_ERROR_FILENAME}"
        GUNICORN_LOG_ACCESS_FILE="${GUNICORN_LOG_DIR%/}/${GUNICORN_LOG_ACCESS_FILENAME}"
        create_directory_if_not_exists_or_exit "$GUNICORN_LOG_DIR"
        touch_file_or_exit "$GUNICORN_LOG_ERROR_FILE"
        touch_file_or_exit "$GUNICORN_LOG_ACCESS_FILE"
        set_read_write_permissions_and_owner_or_exit "$GUNICORN_LOG_DIR"
        log_with_script_prefixe "Gunicorn logs are set up."
    else
        log_with_script_prefixe "APP_IS_EXPOSED is set to false. Gunicorn logs are not needed."
    fi
}

setup_media_dirs () {
    # Match settings.py: FILE_UPLOAD_ENABLED must be set (true or false); no defaults.
    if [ -z "${FILE_UPLOAD_ENABLED:-}" ]; then
        log_with_script_prefixe "ERROR: FILE_UPLOAD_ENABLED must be set to 'true' or 'false'." >&2
        exit 1
    fi
    _fue=$(printf '%s' "$FILE_UPLOAD_ENABLED" | tr '[:upper:]' '[:lower:]')
    case "$_fue" in
        false)
            log_with_script_prefixe "FILE_UPLOAD_ENABLED is false. Skipping media directories."
            return
            ;;
        true) ;;
        *)
            log_with_script_prefixe "ERROR: FILE_UPLOAD_ENABLED must be 'true' or 'false' (got: ${FILE_UPLOAD_ENABLED})." >&2
            exit 1
            ;;
    esac
    if [ -z "${TMP_UPLOADED_FILES:-}" ]; then
        log_with_script_prefixe "ERROR: TMP_UPLOADED_FILES must be set when FILE_UPLOAD_ENABLED is true." >&2
        exit 1
    fi
    log_with_script_prefixe "Setting up temp uploaded files directory and media directories..."
    create_directory_if_not_exists_or_exit "$TMP_UPLOADED_FILES"
    set_read_write_permissions_and_owner_or_exit "$TMP_UPLOADED_FILES"
    chmod a+rwx "$TMP_UPLOADED_FILES"
    log_with_script_prefixe "Temp uploaded files directory is set up (world-writable so AFP container and runner can both write)."

    if [ -n "${METADATA_SESSION_DIR:-}" ]; then
        create_directory_if_not_exists_or_exit "$METADATA_SESSION_DIR"
        set_read_write_permissions_and_owner_or_exit "$METADATA_SESSION_DIR"
        chmod a+rwx "$METADATA_SESSION_DIR"
        log_with_script_prefixe "Metadata session directory is set up."
    fi

    log_with_script_prefixe "Setting up media directory..."
    create_directory_if_not_exists_or_exit "$MEDIA_DIR"
    create_directory_if_not_exists_or_exit "$LIBRARIES_DIR"
    set_read_write_permissions_and_owner_or_exit "$MEDIA_DIR"
    log_with_script_prefixe "Media directories are set up."
}

main (){
    SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
    PROJECT_DIR=$(realpath "$(dirname "$SCRIPTS_DIR")")/
    source "${SCRIPTS_DIR}utils.sh"

    log_with_script_prefixe "Setting up filesystem..."

    check_script_vars_are_set
    check_required_vars_are_set ENV

    if [ $ENV = "collect_static" ]; then
        setup_static_files_for_collection
    else
        setup_static_files_for_serving
    fi

    log_with_script_prefixe "Static files are set up."
    setup_django_log
    setup_gunicorn_log
    setup_media_dirs

    log_with_script_prefixe "Making all scripts in $SCRIPTS_DIR executable..."
    for script in "${SCRIPTS_DIR}"*; do
        if [ -f "$script" ]; then
            output=$(chmod +x "$script")
            if [ $? -ne 0 ]; then
                log_with_script_prefixe "ERROR: Failed to make $script executable: $output" >&2
                exit 1
            fi
        fi
    done
    log_with_script_prefixe "All scripts in $SCRIPTS_DIR are now executable."

    log_with_script_prefixe "The filesystem is set up."
}

main "$@"
