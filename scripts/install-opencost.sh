#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

helm upgrade --install opencost opencost/opencost \
  --namespace opencost \
  --create-namespace \
  -f "${ROOT}/helm/opencost-values.yaml"

kubectl rollout status deployment/opencost -n opencost --timeout=120s

echo "OpenCost installed."
echo "  Aguarde ~2-3 min apos o warmup para dados de custo aparecerem."
echo "  UI: use janela 'Today' ou 'Last 24h' — o lab nao tem historico de 7 dias."
