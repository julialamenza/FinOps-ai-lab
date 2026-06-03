#!/usr/bin/env bash
set -euo pipefail

kubectl delete -f k8s/workloads/cpu-spike.yaml --ignore-not-found=true
kubectl delete -f k8s/workloads/staging-api.yaml --ignore-not-found=true
kubectl delete -f k8s/workloads/users-api.yaml --ignore-not-found=true
kubectl delete -f k8s/workloads/payments-api.yaml --ignore-not-found=true
kubectl delete -f k8s/namespaces/namespaces.yaml --ignore-not-found=true

echo "Lab removed."