#!/usr/bin/env bash
# Remove local and remote git tags that are prerelease/dev for the given version
# (e.g. v2.2.1-staging, v2.2.1-dev.15, v2.2.1-rc). Use after the release version bump when tagging.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
VERSION_FILE="$REPO_ROOT/VERSION"

version="${1:-}"
if [ -z "$version" ]; then
  [ -f "$VERSION_FILE" ] || { echo "VERSION file not found and no version given." >&2; exit 1; }
  version=$(tr -d '[:space:]' < "$VERSION_FILE")
fi

pattern="v${version}-*"
tags=$(git tag -l "$pattern" || true)
if [ -z "$tags" ]; then
  echo "No prerelease tags matching $pattern"
  exit 0
fi

echo "Removing prerelease tags for $version (local and remote):"
echo "$tags"
echo "$tags" | xargs -n 1 git tag -d 2>/dev/null || true
while read -r t; do
  [ -n "$t" ] && git push origin --delete "$t" 2>/dev/null || true
done <<< "$tags"
echo "Done."
