#!/usr/bin/env bash
set -euo pipefail

TS_UTC="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

cat <<EOF
# Contexto coletado do FinOps AI Lab — cole no prompt de IA

Timestamp (UTC): ${TS_UTC}

## Deployments
EOF

kubectl get deploy -A

cat <<EOF

## Consumo por pod (kubectl top)
EOF

kubectl top pods -A 2>/dev/null || echo "(metrics-server indisponível — aguarde ~1 min após subir o cluster)"

cat <<EOF

## Namespaces e labels
EOF

kubectl get ns --show-labels

cat <<EOF

## Resources — payments-api
EOF

kubectl get deployment payments-api -n payments \
  -o custom-columns='WORKLOAD:.metadata.name,CPU_REQ:.spec.template.spec.containers[0].resources.requests.cpu,CPU_LIM:.spec.template.spec.containers[0].resources.limits.cpu,MEM_REQ:.spec.template.spec.containers[0].resources.requests.memory,MEM_LIM:.spec.template.spec.containers[0].resources.limits.memory' 2>/dev/null

cat <<EOF

## Resources — users-api
EOF

kubectl get deployment users-api -n users \
  -o custom-columns='WORKLOAD:.metadata.name,CPU_REQ:.spec.template.spec.containers[0].resources.requests.cpu,CPU_LIM:.spec.template.spec.containers[0].resources.limits.cpu,MEM_REQ:.spec.template.spec.containers[0].resources.requests.memory,MEM_LIM:.spec.template.spec.containers[0].resources.limits.memory' 2>/dev/null

cat <<EOF

## Resources — staging-api
EOF

kubectl get deployment staging-api -n staging \
  -o custom-columns='WORKLOAD:.metadata.name,CPU_REQ:.spec.template.spec.containers[0].resources.requests.cpu,CPU_LIM:.spec.template.spec.containers[0].resources.limits.cpu,MEM_REQ:.spec.template.spec.containers[0].resources.requests.memory,MEM_LIM:.spec.template.spec.containers[0].resources.limits.memory' 2>/dev/null

cat <<EOF

---
Dica: substitua os valores de exemplo nos prompts de ai-prompts/ por estes dados ao vivo.
EOF
