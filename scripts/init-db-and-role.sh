#!/bin/bash

log_with_script_prefixe () {
	log "[DB Initializer] $1"
}

create_database_if_not_exists () {
	log_with_script_prefixe "Checking if database $DB_NAME exists..."
	output=$(psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -tAc \
		"SELECT 1 FROM pg_database WHERE datname = '$DB_NAME';" 2>&1)
	if [ $? -ne 0 ] || echo "$output" | grep -i "error" > /dev/null; then
		log_with_script_prefixe "ERROR: Failed to check if the database exists: $output" >&2
		exit 1
	fi
	if [ ! "$output" = "1" ]; then
		log_with_script_prefixe "Database $DB_NAME does not exist. Creating it..."
		output=$(psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -tAc \
		"CREATE DATABASE $DB_NAME;" 2>&1)
		if [ $? -ne 0 ] || echo "$output" | grep -i "error" > /dev/null; then
			log_with_script_prefixe "ERROR: failed to create the database: $output" >&2
			exit 1
		fi
		log_with_script_prefixe "Database $DB_NAME created successfully."
	else
		log_with_script_prefixe "Database $DB_NAME already exists."
	fi
}

main (){
	SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
	source ${SCRIPTS_DIR}utils.sh

	load_app_env_file_if_exists
	parse_database_url
	create_database_if_not_exists

	log_with_script_prefixe "Database initialization complete."
}

main "$@"
