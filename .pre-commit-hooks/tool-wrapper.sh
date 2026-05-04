#!/bin/bash
# Resolve linter/format tools from PATH (pinned versions via pyproject.toml [project.optional-dependencies] dev).
# Usage: tool-wrapper.sh <tool-name> [tool-args...]

set -e

TOOL_NAME="$1"
shift

if ! command -v "$TOOL_NAME" >/dev/null 2>&1; then
    echo "ERROR: \"$TOOL_NAME\" not found on PATH. Default workflow: Compose api dev image (same pins as CI)." >&2
    echo "  docker compose build api" >&2
    echo "  docker compose exec api <command>" >&2
    exit 1
fi

exec "$TOOL_NAME" "$@"
