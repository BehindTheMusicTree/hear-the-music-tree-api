#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."

if command -v actionlint >/dev/null 2>&1; then
  exec actionlint -config-file .github/actionlint.yaml
fi

echo "Note: Install actionlint (e.g. brew install actionlint) to use .github/actionlint.yaml and suppress false positives." >&2
exec ./node_modules/.bin/node-actionlint
