#!/usr/bin/env bash
# Install editable dev dependencies and pre-commit Git hooks.
# Expects repo root (or pass REPO_ROOT as first argument). When no venv is active, activates
# ./.venv first (same layout as .pre-commit-hooks/tool-wrapper.sh), then ./venv.
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

if [ -z "${VIRTUAL_ENV:-}" ]; then
    if [ -f .venv/bin/activate ]; then
        # shellcheck source=/dev/null
        . .venv/bin/activate
    elif [ -f venv/bin/activate ]; then
        # shellcheck source=/dev/null
        . venv/bin/activate
    elif [ -f .venv/Scripts/activate ]; then
        # shellcheck source=/dev/null
        . .venv/Scripts/activate
    elif [ -f venv/Scripts/activate ]; then
        # shellcheck source=/dev/null
        . venv/Scripts/activate
    else
        echo "error: no active virtualenv and no ./.venv or ./venv" >&2
        echo "  Create one (pre-commit hooks use .venv): python3 -m venv .venv" >&2
        echo "  Or: python3 -m venv venv" >&2
        exit 1
    fi
fi

echo "Installing Python dev dependencies..."
python -m pip install --upgrade pip
pip install -e ".[dev]"

if [ -f .pre-commit-config.yaml ] && command -v pre-commit >/dev/null 2>&1; then
    echo "Installing pre-commit Git hooks..."
    pre-commit install
else
    if [ ! -f .pre-commit-config.yaml ]; then
        echo "warning: .pre-commit-config.yaml not found; skipping pre-commit install" >&2
    fi
fi

echo "✓ Dev tools setup complete (pip dev extras + pre-commit hooks when configured)"
