#!/bin/bash

set -e

WORKTREE_PATH="${1:-$(pwd)}"
SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/"

echo "Setting up worktree at: $WORKTREE_PATH"
cd "$WORKTREE_PATH"

if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment (.venv)..."

    PYTHON_CMD=""
    for version in 3.14 3.13 3.12 3.11 3.10; do
        if command -v "python${version}" >/dev/null 2>&1; then
            PYTHON_CMD="python${version}"
            break
        fi
    done

    if [ -z "$PYTHON_CMD" ]; then
        if command -v python3 >/dev/null 2>&1; then
            PYTHON_CMD="python3"
        else
            echo "Warning: No Python 3 installation found"
            echo "Skipping virtual environment setup"
            exit 0
        fi
    fi

    echo "Using $PYTHON_CMD for virtual environment"
    "$PYTHON_CMD" -m venv .venv
    echo "✓ Virtual environment created at .venv"
else
    echo "Virtual environment already exists at .venv"
fi

if [ -d ".venv" ]; then
    if [ -f .venv/bin/activate ]; then
        # shellcheck source=/dev/null
        source .venv/bin/activate
    elif [ -f .venv/Scripts/activate ]; then
        # shellcheck source=/dev/null
        source .venv/Scripts/activate
    else
        echo "⚠ .venv exists but no activate script found; skipping dev dependency install" >&2
    fi
    if [ -n "${VIRTUAL_ENV:-}" ]; then
        bash "${SCRIPTS_DIR}setup-dev-tools.sh" "$WORKTREE_PATH"
    fi
fi

if [ -f "package.json" ]; then
    echo "Installing npm dependencies..."
    npm install
    echo "✓ npm dependencies installed"
fi

if [ -f "${SCRIPTS_DIR}setup-filesystem.sh" ]; then
    echo "Setting up filesystem..."
    if bash "${SCRIPTS_DIR}setup-filesystem.sh"; then
        echo "✓ Filesystem setup completed"
    else
        echo "⚠ Filesystem setup failed (environment variables may not be configured)"
        echo "  You can run '${SCRIPTS_DIR}setup-filesystem.sh' manually after configuring environment variables"
    fi
fi
