#!/usr/bin/env bash
set -euo pipefail

echo "Applying namespaces..."
kubectl apply -f k8s/namespaces/namespaces.yaml

echo "Applying workloads..."
kubectl apply -f k8s/workloads/payments-api.yaml
kubectl apply -f k8s/workloads/users-api.yaml
kubectl apply -f k8s/workloads/staging-api.yaml

echo "Lab workloads deployed."
kubectl get deploy -A