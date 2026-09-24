#!/bin/bash
set -euo pipefail

apt update && apt install -y shellcheck

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
bash "${script_dir}/install-actionlint.sh"
