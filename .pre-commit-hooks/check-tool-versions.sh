#!/bin/bash
# Check that installed tool versions match pyproject.toml (tools resolved from PATH).

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

get_expected_version() {
    local tool=$1
    grep -E "\"${tool}==" pyproject.toml | sed -E "s/.*${tool}==([0-9.]+).*/\1/" | head -1
}

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

main() {
    echo "Checking tool versions..."

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
        echo "Install pinned dev tools into your active Python environment:"
        echo "  python -m pip install -e \".[dev]\""
        exit 1
    fi

    echo -e "${GREEN}All tool versions match pyproject.toml ✓${NC}"
    exit 0
}

main
