#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WAIT_LOAD="${WAIT_LOAD:-180}"

usage() {
  cat <<EOF
Uso: $(basename "$0") [--wait SEGUNDOS]

Gera metricas no Prometheus/OpenCost apos subir o lab fresco.
Rode depois de deploy-lab.sh (e install-opencost.sh).

  --wait  Segundos de carga antes de abrir dashboards (padrao: 180)

Exemplo:
  $(basename "$0")
  # depois abra Grafana com "Last 15 minutes"
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --wait)
      WAIT_LOAD="${2:?Informe os segundos}"
      shift 2
      ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Opcao desconhecida: $1" >&2; usage; exit 1 ;;
  esac
done

if ! kubectl get namespace payments >/dev/null 2>&1; then
  echo "Namespace 'payments' nao encontrado. Rode ./scripts/deploy-lab.sh primeiro." >&2
  exit 1
fi

echo "Aguardando metrics-server..."
for _ in $(seq 1 30); do
  if kubectl top pods -n payments >/dev/null 2>&1; then
    break
  fi
  sleep 5
done

if ! kubectl top pods -n payments >/dev/null 2>&1; then
  echo "metrics-server ainda indisponivel. Aguarde mais 1-2 min e tente de novo." >&2
  exit 1
fi

echo "Iniciando carga de trafego (business-hours-load)..."
"${ROOT}/scripts/start-business-hours-load.sh" >/dev/null

echo "Coletando metricas por ${WAIT_LOAD}s (~$(( WAIT_LOAD / 60 )) min)..."
sleep "${WAIT_LOAD}"

echo ""
echo "Lab pronto para dashboards e OpenCost."
echo ""
echo "  Grafana  → intervalo: Last 15 minutes (NAO use Last 7 days no lab fresco)"
echo "  OpenCost → janela:   Today ou Last 24h (apos ~3 min de coleta)"
echo ""
kubectl top pods -A 2>/dev/null | head -20
