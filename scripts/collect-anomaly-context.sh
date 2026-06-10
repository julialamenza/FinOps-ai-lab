#!/usr/bin/env bash
set -euo pipefail

TS_UTC="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

cat <<EOF
# Contexto coletado do FinOps AI Lab — cole no prompt de IA

Timestamp (UTC): ${TS_UTC}

## Namespace payments

### kubectl top pods
EOF

kubectl top pods -n payments 2>/dev/null || echo "(metrics-server indisponível — aguarde ~1 min após subir o cluster)"

cat <<EOF

### Pods
EOF

kubectl get pods -n payments -o wide

cat <<EOF

## Namespace staging (anomalia silenciosa)

### CronJobs e Jobs
EOF

kubectl get cronjobs,jobs -n staging -l app=backup-sync 2>/dev/null || echo "(backup-sync não ativo)"

cat <<EOF

### kubectl top pods
EOF

kubectl top pods -n staging 2>/dev/null || echo "(sem métricas)"

cat <<EOF

## Baseline (users)

### kubectl top pods
EOF

kubectl top pods -n users 2>/dev/null || echo "(sem métricas)"

cat <<EOF

---
Dica: use com os prompts em ai-prompts/aula-03-anomalias.md
EOF
