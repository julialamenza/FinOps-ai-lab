#!/usr/bin/env bash
set -euo pipefail

helm upgrade --install opencost opencost/opencost \
  --namespace opencost \
  --create-namespace

kubectl set env deployment/opencost -n opencost \
  PROMETHEUS_SERVER_ENDPOINT=http://monitoring-kube-prometheus-prometheus.monitoring.svc.cluster.local:9090

kubectl rollout restart deployment/opencost -n opencost
kubectl rollout status deployment/opencost -n opencost
