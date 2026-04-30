#!/usr/bin/env bash
# Build and verify Docker-side development tools for api service.
set -euo pipefail

REPO_ROOT="${1:-}"
if [ -z "$REPO_ROOT" ]; then
    REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
fi
cd "$REPO_ROOT"

if ! command -v docker >/dev/null 2>&1; then
    echo "error: docker not found on PATH" >&2
    exit 1
fi

echo "Building api image with development tooling..."
docker compose build api

echo "Starting api service..."
docker compose up -d api

echo "Verifying toolchain in api container..."
docker compose exec -T api pre-commit --version >/dev/null
docker compose exec -T api shellcheck --version >/dev/null
docker compose exec -T api ruff --version >/dev/null

echo "✓ Docker dev tools setup complete"
