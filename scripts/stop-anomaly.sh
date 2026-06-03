#!/usr/bin/env bash
set -euo pipefail

kubectl delete -f k8s/workloads/cpu-spike.yaml --ignore-not-found=true

echo "CPU spike stopped."