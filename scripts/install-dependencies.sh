#!/bin/bash
set -euo pipefail

apt update && apt install -y curl flac ffmpeg libchromaprint-tools jq postgresql-client shellcheck

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
bash "${script_dir}/install-actionlint.sh"
