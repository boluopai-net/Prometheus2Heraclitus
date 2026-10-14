#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "${PY_BIN:-python3}" "$SCRIPT_DIR/setup_guard.py" "$@"
