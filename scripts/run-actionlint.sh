#!/usr/bin/env bash
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if command -v actionlint >/dev/null 2>&1; then
  CONFIG="$ROOT/.github/actionlint.yaml"
  if [ -f "$CONFIG" ]; then
    exec actionlint -config-file "$CONFIG"
  else
    exec actionlint
  fi
fi

echo "Note: Install actionlint (e.g. brew install actionlint) to use .github/actionlint.yaml and suppress false positives." >&2
exec ./node_modules/.bin/node-actionlint
