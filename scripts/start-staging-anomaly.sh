#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MANIFEST="${ROOT}/k8s/anomalies/anomalies.yaml"

usage() {
  cat <<EOF
Uso: $(basename "$0")

Ativa o CronJob backup-sync em staging — anomalia silenciosa de custo (Aula 3, vídeo 3.4).

O job roda a cada 2 minutos no lab (em produção seria ~15 min).
Um job é disparado imediatamente para a demo não depender de espera longa.

Para parar:
  ./scripts/stop-staging-anomaly.sh
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help) usage; exit 0 ;;
    *) echo "Opção desconhecida: $1" >&2; usage; exit 1 ;;
  esac
done

if ! kubectl get namespace staging >/dev/null 2>&1; then
  echo "Namespace 'staging' não encontrado. Rode ./scripts/deploy-lab.sh primeiro." >&2
  exit 1
fi

kubectl apply -f "${MANIFEST}"

JOB_NAME="backup-sync-manual-$(date +%s)"
kubectl create job "${JOB_NAME}" -n staging --from=cronjob/backup-sync

echo "Staging anomaly started (CronJob backup-sync)."
echo ""
echo "Anomalia silenciosa — CPU de staging sobe em rajadas sem afetar disponibilidade."
echo "  Dashboard: finops-ai-anomalies.json (painéis de staging / jobs)"
echo "  Intervalo: Last 15 minutes"
echo ""
echo "Verificar:"
echo "  kubectl get cronjobs,jobs -n staging -l app=backup-sync"
echo "  kubectl top pods -n staging"
echo ""
kubectl get cronjobs,jobs -n staging -l app=backup-sync
