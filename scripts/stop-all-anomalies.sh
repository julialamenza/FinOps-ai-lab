#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

"${ROOT}/scripts/stop-anomaly.sh"
"${ROOT}/scripts/stop-staging-anomaly.sh"

echo "All anomaly workloads stopped."
