#!/usr/bin/env bash
set -e
for key in "$@"; do
  eval "val=\$$key"
  if [ -z "$val" ]; then
    echo "Missing or empty: $key"
    exit 1
  fi
done
echo "All required vars and secrets are set."
