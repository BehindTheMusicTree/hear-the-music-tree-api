#!/bin/bash
set -euo pipefail

apt update && apt install -y curl flac ffmpeg libchromaprint-tools jq postgresql-client
