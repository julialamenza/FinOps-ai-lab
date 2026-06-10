#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

kubectl delete jobs -n staging -l app=backup-sync --ignore-not-found=true
kubectl delete -f "${ROOT}/k8s/anomalies/anomalies.yaml" --ignore-not-found=true

echo "Staging anomaly stopped."
