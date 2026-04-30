#!/bin/bash

set -e

WORKTREE_PATH="${1:-$(pwd)}"
SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/"

echo "Setting up worktree at: $WORKTREE_PATH"
cd "$WORKTREE_PATH"

echo "Installing host dev tools (Docker-backed Git pre-commit hook)..."
bash "${SCRIPTS_DIR}setup-host-dev-tools.sh" "$WORKTREE_PATH"

echo "Installing Docker dev tools (api container toolchain)..."
bash "${SCRIPTS_DIR}setup-docker-dev-tools.sh" "$WORKTREE_PATH"

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
        echo "⚠ Filesystem setup failed (environment variables may not be configured)" >&2
        echo "  You can run '${SCRIPTS_DIR}setup-filesystem.sh' manually after configuring environment variables"
    fi
fi
