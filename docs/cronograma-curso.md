# FinOps com IA — Cronograma do Curso

## Status Geral

| Aula | Tema | Slides | Demo | Prompts IA | Status |
|---|---|---|---|---|---|
| Aula 1 | Observabilidade de custos e comportamento operacional | ✅ | ✅ | ⬜ | Pronta para roteiro |
| Aula 2 | Rightsizing e eficiência operacional automatizada | ✅ | ✅ | ⬜ | Pronta para roteiro |
| Aula 3 | Anomalias de custo e capacity planning operacional | ⬜ | ✅ | ⬜ | Pronta para roteiro |
| Aula 4 | Governança operacional e visibilidade de custos | ⬜ | ✅ parcial | ⬜ | Pendente |
| Aula 5 | Operações cloud orientadas por eficiência | ⬜ | ✅ parcial | ⬜ | Pendente |

## Laboratório

Componentes:

- Minikube
- Prometheus
- Grafana
- OpenCost

Namespaces:

- payments
- users
- staging

Workloads:

- payments-api: workload overprovisionado
- users-api: workload saudável
- staging-api: workload para scheduling / scale down
- cpu-spike: anomalia de CPU (sob demanda)
- backup-sync: CronJob em staging — anomalia silenciosa de custo
- business-hours-load: tráfego HTTP por horário comercial