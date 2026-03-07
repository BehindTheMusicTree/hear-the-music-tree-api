#!/bin/bash
# Usage: ./wait-for-afp.sh <AFP_HOST> <AFP_PORT> [MAX_ATTEMPTS] [SLEEP_INTERVAL]
# Example: ./wait-for-afp.sh localhost 3002 12 5

log_with_script_prefixe () {
    log "[AFP waiter] $1"
}

AFP_HOST=$1
AFP_PORT=$2
MAX_ATTEMPTS=${3:-12}
SLEEP_INTERVAL=${4:-5}

attempts=0
HEALTH_URL="http://${AFP_HOST}:${AFP_PORT}/health/"

SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
PROJECT_DIR=$(realpath "$(dirname "$SCRIPTS_DIR")")/
source "${SCRIPTS_DIR}utils.sh"

log_with_script_prefixe "Waiting for AFP service to start..."
while ! curl -sf -o /dev/null "$HEALTH_URL"; do
  if [ "$attempts" -eq "$MAX_ATTEMPTS" ]; then
    log_with_script_prefixe "ERROR: AFP service did not start within the expected time." >&2
    exit 1
  fi
  log_with_script_prefixe "Waiting for AFP service to start..."
  sleep "$SLEEP_INTERVAL"
  attempts=$((attempts+1))
done

log_with_script_prefixe "AFP service is up and running."
