#!/usr/bin/env bash
# Install host-side development wiring (Docker-backed git hook).
set -euo pipefail

REPO_ROOT="${1:-}"
if [ -z "$REPO_ROOT" ]; then
    REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
fi
cd "$REPO_ROOT"

if ! command -v git >/dev/null 2>&1; then
    echo "error: git not found on PATH" >&2
    exit 1
fi

if ! command -v docker >/dev/null 2>&1; then
    echo "warning: docker not on PATH; the git hook will run pre-commit on the host unless the api container is up" >&2
fi

HOOK_SOURCE="${REPO_ROOT}/.githooks/pre-commit"
if [ ! -f "$HOOK_SOURCE" ]; then
    echo "error: ${HOOK_SOURCE} not found" >&2
    exit 1
fi

HOOKS_DIR="$(git rev-parse --git-path hooks)"
mkdir -p "$HOOKS_DIR"
install -m 0755 "$HOOK_SOURCE" "${HOOKS_DIR}/pre-commit"
echo "Installed git pre-commit hook: ${HOOKS_DIR}/pre-commit"
echo "✓ Host dev tools setup complete"
