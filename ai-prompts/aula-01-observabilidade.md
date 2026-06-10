# Aula 1 — Observabilidade de custos e comportamento operacional

## Objetivo dos prompts

Apoiar a análise de consumo por namespace, identificar desperdícios operacionais, explicar padrões de uso e sugerir métricas essenciais para SRE e Platform Engineering no laboratório FinOps AI Lab.

## Como usar na gravação

O lab é montado na hora — não precisa de histórico de 24h.

1. Rode `./scripts/start-business-hours-load.sh` e aguarde 2–3 min (tráfego realista)
2. Abra `finops-ai-lab.json` com intervalo **Last 15 minutes**
3. Rode `./scripts/collect-lab-context.sh` e cole a saída no prompt (substitui os números de exemplo)
4. Use a resposta para comentar slides ou conectar teoria com a demo ao vivo

---

## Prompt 1 — Panorama de consumo por namespace

```
Você é um SRE especialista em FinOps e Kubernetes. Analise o consumo operacional do cluster abaixo e identifique onde há desperdício, subutilização ou risco de saturação.

Dados do ambiente (últimas 24h):

| Namespace | Workload      | Réplicas | CPU request | CPU uso médio | CPU P95 | Mem request | Mem uso médio | Mem P95 |
|-----------|---------------|----------|-------------|---------------|---------|-------------|---------------|---------|
| payments  | payments-api  | 2        | 1000m       | 72m           | 95m     | 1 Gi        | 88 Mi         | 110 Mi  |
| users     | users-api     | 2        | 100m        | 48m           | 62m     | 128 Mi      | 76 Mi         | 92 Mi   |
| staging   | staging-api   | 1        | 500m        | 28m           | 35m     | 512 Mi      | 58 Mi         | 72 Mi   |

Contexto:
- Cluster Minikube local com Prometheus, Grafana e OpenCost.
- payments e users são produção; staging é ambiente de homologação.
- Objetivo: entender comportamento operacional antes de falar em custo.

Responda em português do Brasil:
1. Qual namespace merece atenção primeiro e por quê?
2. Onde há gap entre request e uso real?
3. Quais métricas você monitoraria continuamente (nome da métrica Prometheus, se souber)?
4. Que perguntas você faria ao time dono de cada workload?
```

---

## Prompt 2 — Desperdícios operacionais em ambientes distribuídos

```
Analise este cenário de cloud Kubernetes com múltiplos namespaces e explique onde podem surgir desperdícios operacionais — mesmo sem fatura AWS visível ainda.

Namespaces e labels:
- payments: team=payments, environment=prod, cost-center=product
- users: team=users, environment=prod, cost-center=product
- staging: team=platform, environment=staging, cost-center=engineering

Workloads:
- payments-api: nginx estável, 2 réplicas, requests altos (1 CPU, 1 Gi RAM por pod)
- users-api: nginx estável, 2 réplicas, requests moderados (100m CPU, 128 Mi RAM)
- staging-api: nginx estável, 1 réplica, requests médios (500m CPU, 512 Mi RAM)

Responda em português do Brasil, em linguagem para SRE/DevOps:
1. Liste os tipos de desperdício possíveis (over-provisioning, idle resources, ambientes sempre ligados, etc.).
2. Para cada namespace, indique o padrão de risco mais provável.
3. Sugira 3 sinais no Grafana/Prometheus que confirmariam cada hipótese.
4. Proponha um checklist semanal de revisão operacional.
```

---

## Prompt 3 — Padrões de uso e sazonalidade

```
Atue como Platform Engineer. Com base nas séries abaixo, explique os padrões de uso e o que isso implica para planejamento de capacidade e custo.

Consumo CPU médio por namespace (mCPU, janela 7 dias):
- payments: seg-sex 65–80, sáb-dom 40–50 (carga estável, leve queda no fim de semana)
- users: seg-sex 45–55, sáb-dom 35–42 (padrão saudável, uso próximo ao request)
- staging: seg-sex 25–30, sáb-dom 5–10 (quase idle fora do horário comercial)

Memória:
- payments: uso estável ~85 Mi por pod, request 1 Gi
- users: uso estável ~75 Mi por pod, request 128 Mi
- staging: uso ~55 Mi, request 512 Mi

Responda em português do Brasil:
1. Classifique cada namespace: saudável, overprovisionado ou subdimensionado.
2. Há indício de workload que deveria escalar (HPA) ou desligar fora de horário?
3. Como você apresentaria esses padrões para um gestor de produto (sem jargão excessivo)?
4. Que alertas configuraria para evitar surpresa operacional?
```

---

## Prompt 4 — Métricas essenciais para FinOps em Kubernetes

```
Sou Cloud Engineer montando observabilidade FinOps em um cluster Kubernetes (Prometheus + Grafana + OpenCost). Os namespaces são payments, users e staging.

Quero uma lista prática de métricas e painéis, não teoria genérica.

Responda em português do Brasil:
1. Quais 8 métricas Prometheus são indispensáveis para correlacionar uso, requests/limits e custo?
2. Para cada métrica, diga o que ela revela e um exemplo de query ou nome de série. 
3. Como organizar dashboards por persona: SRE (operação), FinOps (custo), Engineering Manager (produtividade)?
4. Que dados do OpenCost devo cruzar com métricas de utilização do kube-state-metrics/cAdvisor?
5. Sugira um painel mínimo viável para a primeira demo do curso.
```

---

## Prompt 5 — Narrativa para abertura da aula (sem dados técnicos)

```
Estou gravando a aula 1 de um curso "FinOps com IA" para público de SRE, DevOps e Platform Engineers.

Contexto do lab: Minikube com workloads simulados (payments-api overprovisionado, users-api saudável, staging-api subutilizado).

Escreva em português do Brasil:
1. Um parágrafo de abertura (30–40 segundos de fala) sobre por que observabilidade operacional precede otimização de custo.
2. Três analogias simples para explicar a diferença entre "custo na fatura" e "comportamento de consumo".
3. Uma pergunta provocativa para engajar a audiência antes da primeira demo com kubectl/Grafana.
```
