#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MANIFEST="${ROOT}/k8s/workloads/cpu-spike.yaml"
DURATION=300

usage() {
  cat <<EOF
Uso: $(basename "$0") [--duration SEGUNDOS]

  --duration  Duração do spike de CPU (padrão: 300 = 5 min)

Exemplo para gravação (spike visível em ~30s):
  $(basename "$0") --duration 300
  ./scripts/collect-anomaly-context.sh   # dados para colar no prompt de IA

Fluxo recomendado (baseline realista + spike):
  ./scripts/start-business-hours-load.sh
  sleep 120
  $(basename "$0")

Para parar:
  ./scripts/stop-anomaly.sh
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --duration)
      DURATION="${2:?Informe os segundos}"
      shift 2
      ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Opção desconhecida: $1" >&2; usage; exit 1 ;;
  esac
done

if ! kubectl get namespace payments >/dev/null 2>&1; then
  echo "Namespace 'payments' não encontrado. Rode ./scripts/deploy-lab.sh primeiro." >&2
  exit 1
fi

kubectl apply -f "${MANIFEST}"
kubectl set env deployment/cpu-spike -n payments "STRESS_TIMEOUT=${DURATION}s"
kubectl rollout status deployment/cpu-spike -n payments --timeout=90s

echo "CPU spike started (duration: ${DURATION}s)."
echo ""
echo "O spike deve aparecer no Grafana em ~30–60s."
echo "  Dashboard: finops-ai-anomalies.json"
echo "  Intervalo: Last 15 minutes"
echo ""
echo "Coletar dados para prompt de IA:"
echo "  ./scripts/collect-anomaly-context.sh"
echo ""
kubectl get pods -n payments -l app=cpu-spike
