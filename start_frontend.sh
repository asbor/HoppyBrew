#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRONTEND_DIR="${SCRIPT_DIR}/services/nuxt3-shadcn"

cd "${FRONTEND_DIR}"

PORT="${FRONTEND_PORT:-3000}"
npm run dev -- --host 0.0.0.0 --port "${PORT}"
