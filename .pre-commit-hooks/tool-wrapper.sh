#!/bin/bash
# Resolve linter/format tools from PATH (pinned versions via pyproject.toml [project.optional-dependencies] dev).
# Usage: tool-wrapper.sh <tool-name> [tool-args...]

set -e

TOOL_NAME="$1"
shift

if ! command -v "$TOOL_NAME" >/dev/null 2>&1; then
    echo "ERROR: \"$TOOL_NAME\" not found on PATH. Install dev dependencies (same pins as CI):" >&2
    echo "  python -m pip install -e \".[dev]\"" >&2
    exit 1
fi

exec "$TOOL_NAME" "$@"
