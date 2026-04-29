#!/usr/bin/env bash
# Install editable dev dependencies and pre-commit Git hooks (pinned in pyproject.toml).
set -e

REPO_ROOT="${1:-}"
if [ -z "$REPO_ROOT" ]; then
    REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
fi
cd "$REPO_ROOT"

if [ ! -f pyproject.toml ]; then
    echo "error: pyproject.toml not found under ${REPO_ROOT}" >&2
    exit 1
fi

PYTHON_CMD="${PYTHON_CMD:-}"
if [ -z "$PYTHON_CMD" ]; then
    for candidate in python3 python; do
        if command -v "$candidate" >/dev/null 2>&1; then
            PYTHON_CMD="$candidate"
            break
        fi
    done
fi

if [ -z "$PYTHON_CMD" ]; then
    echo "error: no Python interpreter found on PATH (set PYTHON_CMD to override)" >&2
    exit 1
fi

echo "Installing Python dev dependencies with ${PYTHON_CMD}..."
"$PYTHON_CMD" -m pip install --upgrade pip
"$PYTHON_CMD" -m pip install -e ".[dev]"

if [ -f .pre-commit-config.yaml ] && command -v pre-commit >/dev/null 2>&1; then
    echo "Installing pre-commit Git hooks..."
    pre-commit install
else
    if [ ! -f .pre-commit-config.yaml ]; then
        echo "warning: .pre-commit-config.yaml not found; skipping pre-commit install" >&2
    fi
fi

echo "✓ Dev tools setup complete"
