#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

kubectl delete -f "${ROOT}/k8s/workloads/cpu-spike.yaml" --ignore-not-found=true

echo "CPU spike stopped."
