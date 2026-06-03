#!/usr/bin/env bash
set -euo pipefail

kubectl apply -f k8s/workloads/cpu-spike.yaml

echo "CPU spike started."
kubectl get pods -n payments