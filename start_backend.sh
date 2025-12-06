#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="${SCRIPT_DIR}/services/backend"

cd "${BACKEND_DIR}"

# Activate virtual environment if present
if [ -d "venv" ]; then
  # shellcheck disable=SC1091
  source venv/bin/activate
elif [ -d ".venv" ]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
else
  echo "[WARN] No virtual environment found in ${BACKEND_DIR}. Continuing without activation." >&2
fi

PORT="${API_PORT:-8000}"
python -m uvicorn main:app --host 0.0.0.0 --port "${PORT}" --reload
