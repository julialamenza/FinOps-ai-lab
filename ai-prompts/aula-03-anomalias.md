# Aula 3 — Anomalias de custo e capacity planning operacional

## Objetivo dos prompts

Detectar anomalias de consumo, explicar causas prováveis, correlacionar spikes com deploys/workloads (como `cpu-spike`) e projetar necessidade futura de capacidade no cluster.

## Como usar na gravação

1. Rode `./scripts/start-anomaly.sh` antes da demo para ativar o `cpu-spike` no namespace payments.
2. Abra o dashboard Grafana e capture o spike de CPU em payments.
3. Cole o prompt com os dados atualizados (horário do spike, valor de CPU, workload envolvido).
4. Encerre com `./scripts/stop-anomaly.sh` e mostre o retorno ao baseline.

---

## Prompt 1 — Detecção de anomalia de CPU

```
Você é um SRE investigando um spike de CPU no namespace payments.

Timeline (UTC):
- 14:00 — CPU payments: ~140 mCPU total (baseline)
- 14:05 — deploy manual do workload cpu-spike (1 réplica)
- 14:06 — CPU payments: ~2100 mCPU total (+1400% vs. baseline)
- 14:06 — payments-api estável em ~145 mCPU (2 pods)
- 14:20 — sem novos deploys em users ou staging

Workloads no namespace payments:
- payments-api: 2 réplicas, nginx, requests 1000m CPU
- cpu-spike: 1 réplica, stress --cpu 2, requests 500m, limits 2000m

Responda em português do Brasil:
1. A anomalia é legítima (carga real) ou provável misconfiguration/teste esquecido?
2. Passos de triagem em ordem (kubectl, métricas, logs, change calendar).
3. Impacto no cluster Minikube (4 CPUs): risco de contenção com outros namespaces?
4. Ação imediata recomendada e ação preventiva (alerta, quota, policy).
5. Como documentar o incidente em um postmortem leve (template 5 linhas).
```

---

## Prompt 2 — Correlação custo × comportamento operacional

```
Correlacione anomalia operacional com impacto de custo alocável.

Dados OpenCost (estimativa didática, namespace payments, janela do incidente):
- Custo horário baseline: R$ 4,20 / hora
- Custo horário durante cpu-spike (1h): R$ 18,60 / hora
- users e staging: sem variação significativa

Métricas:
- container_cpu_usage_seconds_total{namespace="payments"}: pico 2.1 cores por 55 min
- kube_pod_status_phase{namespace="payments"}: todos Running

Responda em português do Brasil:
1. Explique a diferença entre "custo na fatura" e "custo alocado no OpenCost" neste cenário.
2. O spike de cpu-spike afeta custo de payments-api mesmo sem mudar requests do payments-api?
3. Que visualização no Grafana/OpenCost melhor comunica o incidente para FinOps?
4. Sugira 2 alertas: um técnico (SRE) e um de custo (FinOps).
5. Estimativa de custo evitável se o cpu-spike tivesse sido detectado em 10 minutos.
```

---

## Prompt 3 — Capacity planning após incidente

```
Após o incidente com cpu-spike no namespace payments, projete capacidade do cluster para os próximos 90 dias.

Estado atual do cluster (Minikube, 4 CPU / 8 Gi RAM):
- Alocação por requests: payments ~2200m, users ~200m, staging ~500m, sistema ~800m
- Uso real médio: payments ~200m, users ~100m, staging ~30m
- Crescimento esperado: users-api +30% tráfego em 90 dias; payments estável; staging pode ganhar novo workload de testes

Responda em português do Brasil:
1. O cluster tem headroom suficiente hoje? Quantifique em CPU e memória.
2. Em que cenário um novo spike como cpu-spike derruba scheduling (Pending pods)?
3. Projeção de uso em 90 dias (tabela por namespace).
4. Recomendações: expandir cluster, quotas por namespace, limitRange, PriorityClass?
5. Quando escalar horizontalmente o node pool vs. rightsizing primeiro?
```

---

## Prompt 4 — Anomalia silenciosa em staging

```
O namespace staging não teve spike de CPU, mas o custo alocado subiu 22% na última semana sem deploy novo visível.

Dados:
- staging-api: 1 réplica, requests 500m CPU / 512 Mi, uso médio 28m CPU
- Novo CronJob detectado: backup-sync (executa a cada 15 min, pico 400m CPU por 3 min)
- Labels: team=platform, environment=staging, cost-center=engineering
- Nenhuma mudança em payments ou users

Responda em português do Brasil:
1. Por que este é um caso de "anomalia de custo" e não de "incidente de disponibilidade"?
2. Como correlacionar CronJobs/Jobs com custo no OpenCost e no Prometheus?
3. O staging-api ainda deve ser rightsized ou o problema é o CronJob?
4. Políticas de governança que evitariam CronJobs órfãos em staging.
5. Mensagem para o time platform: tom colaborativo, foco em eficiência.
```

---

## Prompt 5 — Runbook de resposta a anomalias

```
Crie um runbook operacional para anomalias de custo/consumo no FinOps AI Lab.

Ambiente: Kubernetes, Prometheus, Grafana, OpenCost, namespaces payments/users/staging, script start-anomaly.sh dispara cpu-spike.

Responda em português do Brasil, formato runbook para SRE on-call:
1. Sintomas (o que o alerta ou dashboard mostra).
2. Diagnóstico em 10 minutos (comandos kubectl e queries Prometheus sugeridas).
3. Mitigação imediata (scale down, delete pod, isolate namespace).
4. Comunicação (quem acionar: payments, platform, FinOps).
5. Encerramento e follow-up (ticket, ajuste de alerta, lição aprendida).
6. Seção "Quando NÃO agir" — falsos positivos comuns.
```
