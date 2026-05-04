#!/usr/bin/env bash
# Ensure actionlint exists (Docker image may predate install-actionlint.sh); then lint workflow YAML.
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
config="${repo_root}/.github/actionlint.yaml"

if ! command -v actionlint >/dev/null 2>&1; then
    if [ "$(uname -s)" = Linux ]; then
        bash "${repo_root}/scripts/install-actionlint.sh"
    else
        echo "error: actionlint not on PATH (rebuild the api image after Dockerfile/install script changes," >&2
        echo "error: or install actionlint on the host, e.g. brew install actionlint)." >&2
        exit 1
    fi
fi

exec actionlint -config-file "$config" "$@"
