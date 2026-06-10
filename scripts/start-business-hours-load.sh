#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MANIFEST="${ROOT}/k8s/workloads/business-hours-load.yaml"
PROFILE="demo"

usage() {
  cat <<EOF
Uso: $(basename "$0") [--demo | --real]

  --demo  (padrão) Simula um dia inteiro em ~12 minutos — ideal para o lab local
  --real          Usa horário real (seg-sex 09h–18h, America/Sao_Paulo)

Exemplo para demo/gravação:
  $(basename "$0")
  # aguarde ~12 min e abra o Grafana com intervalo "Last 15 minutes"

Para parar:
  ./scripts/stop-business-hours-load.sh
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --demo) PROFILE="demo" ;;
    --real) PROFILE="real" ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Opção desconhecida: $1" >&2; usage; exit 1 ;;
  esac
  shift
done

for ns in payments users staging; do
  if ! kubectl get namespace "$ns" >/dev/null 2>&1; then
    echo "Namespace '${ns}' não encontrado. Rode ./scripts/deploy-lab.sh primeiro." >&2
    exit 1
  fi
done

kubectl apply -f "${MANIFEST}"
kubectl set env deployment/payments-business-load -n payments "LOAD_PROFILE=${PROFILE}"
kubectl rollout status deployment/payments-business-load -n payments --timeout=90s

echo "Business hours load started (profile: ${PROFILE})."
echo ""

if [ "${PROFILE}" = "demo" ]; then
  echo "Modo DEMO — ciclo acelerado (~12 min, repete automaticamente):"
  echo "  0–6 min   → horário comercial (payments alto)"
  echo "  6–9 min   → fora do pico (payments médio)"
  echo "  9–12 min  → noite/fim de semana (payments baixo)"
  echo ""
  echo "Para ver a tendência no Grafana:"
  echo "  Gravação (lab montado na hora): aguarde 2–3 min, use 'Last 15 minutes'"
  echo "  Demo completa: aguarde ~12 min para ver o ciclo inteiro"
  echo "  Dashboard: finops-ai-lab.json"
  echo "  Compare: payments oscila | users estável | staging quase flat"
else
  echo "Modo REAL — segue o relógio (America/Sao_Paulo):"
  echo "  payments → alto seg-sex 09h–18h, menor à noite e no fim de semana"
fi

echo ""
echo "  users    → tráfego estável o dia todo"
echo "  staging  → quase ocioso (1 requisição/min)"
echo ""
kubectl get pods -n payments -l app=payments-business-load
kubectl get pods -n users -l app=users-steady-load
kubectl get pods -n staging -l app=staging-idle-load
