#!/usr/bin/env bash
# Install pinned actionlint to /usr/local/bin (Linux amd64/arm64). Used by Dockerfile and CI.
set -euo pipefail

readonly VERSION=1.7.12
machine="$(uname -m)"
case "$machine" in
x86_64) arch=amd64 ;;
aarch64 | arm64) arch=arm64 ;;
*)
    echo "install-actionlint.sh: unsupported uname -m: ${machine} (need Linux amd64 or arm64)" >&2
    exit 1
    ;;
esac

tmp="$(mktemp -d)"
cleanup() {
    rm -rf "$tmp"
}
trap cleanup EXIT

url="https://github.com/rhysd/actionlint/releases/download/v${VERSION}/actionlint_${VERSION}_linux_${arch}.tar.gz"
curl -fsSL "$url" -o "${tmp}/actionlint.tgz"
tar -xzf "${tmp}/actionlint.tgz" -C "$tmp"

dest=/usr/local/bin/actionlint
if [ -w "$(dirname "$dest")" ]; then
    install -m 0755 "${tmp}/actionlint" "$dest"
else
    sudo install -m 0755 "${tmp}/actionlint" "$dest"
fi

actionlint -version
