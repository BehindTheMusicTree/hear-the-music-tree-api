#!/bin/bash
# Check that installed tool versions match pyproject.toml
# This ensures pre-commit uses the same versions as CI

set -e

# If .venv or venv exists and VIRTUAL_ENV is not set, add .../bin to PATH first.
# Handles VS Code / IDE commits where the shell isn't activated (Docker-first dev may still keep one venv for hooks).
if [ -z "$VIRTUAL_ENV" ]; then
    if [ -d ".venv/bin" ] && [ -x ".venv/bin/python" ]; then
        export PATH=".venv/bin:$PATH"
        USING_LOCAL_VENV=true
    elif [ -d "venv/bin" ] && [ -x "venv/bin/python" ]; then
        export PATH="venv/bin:$PATH"
        USING_LOCAL_VENV=true
    fi
fi

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Extract version from pyproject.toml
get_expected_version() {
    local tool=$1
    # Match patterns like: "ruff==0.15.9", "isort==5.13.2", etc.
    grep -E "\"${tool}==" pyproject.toml | sed -E "s/.*${tool}==([0-9.]+).*/\1/" | head -1
}

# Get installed version
get_installed_version() {
    local tool=$1
    case $tool in
        ruff)
            ruff --version 2>/dev/null | awk '{print $2}' || echo "NOT_INSTALLED"
            ;;
        isort)
            isort --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1 || echo "NOT_INSTALLED"
            ;;
        mypy)
            mypy --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' || echo "NOT_INSTALLED"
            ;;
        pydocstringformatter)
            pydocstringformatter --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' || echo "NOT_INSTALLED"
            ;;
    esac
}

# Check if we're in a virtual environment (skip check in CI)
check_venv() {
    # Skip venv check in CI environments
    if [ -n "$CI" ] || [ -n "$GITHUB_ACTIONS" ]; then
        return 0
    fi

    # Opt-out for hosts without an activated venv (e.g. Docker-only workflow); linters must still be on PATH.
    if [ "${PRE_COMMIT_SKIP_VENV_GUARD:-}" = "true" ] || [ "${PRE_COMMIT_SKIP_VENV_GUARD:-}" = "1" ]; then
        echo -e "${YELLOW}Note: PRE_COMMIT_SKIP_VENV_GUARD set — skipping virtualenv detection (tools must match pyproject pins).${NC}"
        return 0
    fi

    # Check if we're using local .venv or venv (PATH adjusted at top of script)
    if [ "$USING_LOCAL_VENV" = "true" ]; then
        echo -e "${YELLOW}Note: Using tools from repo virtualenv without activating the shell (PATH includes .venv/bin or venv/bin).${NC}"
        return 0
    fi

    # Check if VIRTUAL_ENV is set
    if [ -z "$VIRTUAL_ENV" ]; then
        echo -e "${RED}ERROR: No virtual environment detected!${NC}"
        echo -e "${YELLOW}Pre-commit hooks need pinned tools (same as CI). Typical fixes:${NC}"
        echo ""
        echo "  • Activate a venv that has dev deps: source .venv/bin/activate"
        echo "  • Or create one: python3 -m venv .venv && bash scripts/setup-dev-tools.sh"
        echo "  • Docker-only host with tools unavailable here: PRE_COMMIT_SKIP_VENV_GUARD=true git commit ..."
        echo "    (still requires ruff/isort/mypy/pydocstringformatter on PATH at pinned versions)"
        return 1
    fi
    return 0
}

# Main validation
main() {
    echo "Checking tool versions..."

    # Check virtual environment first (unless in CI)
    if ! check_venv; then
        exit 1
    fi

    local has_errors=0
    local tools=("ruff" "isort" "mypy" "pydocstringformatter")

    for tool in "${tools[@]}"; do
        expected=$(get_expected_version "$tool")
        installed=$(get_installed_version "$tool")

        if [ "$installed" = "NOT_INSTALLED" ]; then
            echo -e "${RED}✗ $tool: NOT INSTALLED${NC}"
            has_errors=1
        elif [ "$installed" != "$expected" ]; then
            echo -e "${RED}✗ $tool: version mismatch${NC}"
            echo -e "  Expected: ${YELLOW}$expected${NC} (from pyproject.toml)"
            echo -e "  Installed: ${YELLOW}$installed${NC}"
            has_errors=1
        else
            echo -e "${GREEN}✓ $tool: $installed${NC}"
        fi
    done

    if [ $has_errors -eq 1 ]; then
        echo ""
        echo -e "${RED}ERROR: Tool version mismatch detected!${NC}"
        echo ""
        echo "To fix this (from repo root):"
        echo "  bash scripts/setup-dev-tools.sh"
        echo ""
        echo "That activates ./.venv or ./venv if needed, then runs pip install -e \".[dev]\" (same pins as CI)."
        echo "Manual alternative: activate your venv, then pip install -e \".[dev]\""
        exit 1
    fi

    echo -e "${GREEN}All tool versions match pyproject.toml ✓${NC}"
    exit 0
}

main
