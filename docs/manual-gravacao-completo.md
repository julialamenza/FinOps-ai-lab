---
title: FinOps com IA — Manual Completo de Gravação
subtitle: Setup, roteiro, comandos, prompts e checklist dos 25 vídeos
lang: pt-BR
geometry: margin=2cm
fontsize: 11pt
documentclass: article
toc: true
toc-depth: 2
---

# FinOps com IA — Manual Completo de Gravação

Documento **único** para gravação do curso: setup, slides, o que mostrar, comandos, prompts e checklist.

> **Exportar PDF (opcional):** `./scripts/export-manual-gravacao-pdf.sh`

> **Regenerar este arquivo** após editar `scripts/recording_data.py` ou prompts: `./scripts/generate-manual-gravacao.sh`

> O lab é montado **na hora**. Use **Last 15 minutes** em todos os dashboards Grafana.

---

## Parte 1 — Preparação e setup

### Setup global (início de cada dia)

```bash
minikube start --cpus=4 --memory=8192
./scripts/deploy-lab.sh
./scripts/install-opencost.sh
./scripts/stop-all-anomalies.sh
./scripts/warmup-lab-metrics.sh
```

### Port-forwards

| Serviço | Comando | URL |
|---------|---------|-----|
| Grafana | `kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80` | http://localhost:3000 |
| Prometheus | `kubectl port-forward -n monitoring svc/monitoring-kube-prometheus-prometheus 9090:9090` | http://localhost:9090 |
| OpenCost | `kubectl port-forward -n opencost svc/opencost 9003:9090` | http://localhost:9003 |

### Referência rápida por aula

| Aula | Dashboard | Port-forwards |
|------|-----------|---------------|
| 1 | `grafana/dashboards/finops-ai-lab.json` | Grafana (vídeos 1.3+) |
| 2 | `grafana/dashboards/finops-ai-rightsizing.json` | Grafana (vídeos 2.2, 2.5) |
| 3 | `grafana/dashboards/finops-ai-anomalies.json` | Grafana (todos) |
| 4 | `grafana/dashboards/finops-ai-governance.json` | Grafana (4.2+) + OpenCost (4.3, 4.5) |
| 5 | `Todos os dashboards anteriores` | Grafana (5.1, 5.5) + OpenCost (5.5) |

### Legenda de tipos

| Tipo | Significado |
|------|-------------|
| **T** | Teoria — slides + prompt IA, sem lab |
| **T+** | Teoria + demo leve — kubectl ou dashboard estático |
| **T++** | Teoria + demo ativa — scripts, spikes, jobs |
| **H** | Hands-on — demo completa (vídeo X.5) |

---

## Parte 2 — Roteiro e prompts por vídeo

## Aula 1 — Observabilidade de custos e comportamento operacional

**Dashboard:** `grafana/dashboards/finops-ai-lab.json` | **Port-forwards:** Grafana (vídeos 1.3+)

### Vídeo 1.1 — O desafio da eficiência operacional em cloud

| Campo | Valor |
|-------|-------|
| Tipo | **T** |
| Tempo | 8–10 min |
| Dashboard | `grafana/dashboards/finops-ai-lab.json` |
| Prompt | `ai-prompts/aula-01/1.1-narrativa-abertura.md` |

**Objetivo:** Explicar por que ambientes distribuídos aumentam complexidade operacional e dificultam controle de custos.

**Slides:**
- Slide 1: Introdução
- Slide 2: O desafio da eficiência operacional em cloud
- Slide 3: Crescimento da complexidade

**O que mostrar:**
- Apresentação (slides 1–3) — sem terminal, sem Grafana.

**Comandos:** Nenhum.

**Antes de colar o prompt:**
Sem demo. Prompt curto — não precisa de dados do cluster.

**Prompt IA — copiar e colar:**

```
Estou gravando a aula 1 de um curso "FinOps com IA" para público de SRE, DevOps e Platform Engineers.

Contexto do lab: Minikube com workloads simulados (payments-api overprovisionado, users-api saudável, staging-api subutilizado).

Escreva em português do Brasil:
1. Um parágrafo de abertura (30–40 segundos de fala) sobre por que observabilidade operacional precede otimização de custo.
2. Três analogias simples para explicar a diferença entre "custo na fatura" e "comportamento de consumo".
3. Uma pergunta provocativa para engajar a audiência antes da primeira demo com kubectl/Grafana.
```

\newpage

### Vídeo 1.2 — Entendendo comportamento de consumo em cloud

| Campo | Valor |
|-------|-------|
| Tipo | **T+** |
| Tempo | 10–12 min |
| Dashboard | `grafana/dashboards/finops-ai-lab.json` |
| Prompt | `ai-prompts/aula-01/1.2-desperdicios-operacionais.md` *(opcional)* |

**Objetivo:** Explicar como workloads, escalabilidade, ambientes e pipelines influenciam padrões de utilização e custo.

**Slides:**
- Slide 4: Observabilidade + FinOps
- Slide 5: Workloads, requests, limits, HPA/VPA e namespaces
- Slide 6: Desperdícios operacionais

**O que mostrar:**
- Slides 4–6.
- Terminal: namespaces com labels (payments, users, staging).
- Terminal: deployments do lab (payments-api, users-api, staging-api).

**Comandos:**

```bash
kubectl get ns --show-labels
kubectl get deploy -A
```

**Antes de colar o prompt:**
Opcional. Complementa slides + `kubectl get ns --show-labels` e `kubectl get deploy -A`.

**Prompt IA — copiar e colar:**

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

\newpage

### Vídeo 1.3 — Identificando tendências de crescimento operacional

| Campo | Valor |
|-------|-------|
| Tipo | **T+** |
| Tempo | 10–12 min |
| Dashboard | `grafana/dashboards/finops-ai-lab.json` |
| Prompt | `ai-prompts/aula-01/1.3-padroes-sazonalidade.md` |

**Objetivo:** Mostrar como identificar tendências de consumo e crescimento operacional usando métricas de observabilidade.

**Slides:**
- Slide 7: Padrões de consumo e sazonalidade
- Slide 8: Tendências de crescimento operacional
- Slide 9: Leitura de tendências no Grafana (exemplo)

**O que mostrar:**
- Slides 7–9.
- Grafana → `finops-ai-lab.json` → **Last 15 minutes**.
- Comentar gauges de CPU/memória por namespace.
- Opcional: iniciar business-hours-load 2 min antes para padrão de uso.

**Comandos:**

```bash
./scripts/start-business-hours-load.sh
# aguarde 2–3 min
# Grafana → finops-ai-lab.json → Last 15 minutes
```

**Antes de colar o prompt:**
Slides + Grafana (`finops-ai-lab.json`, Last 15 minutes). Rode `./scripts/start-business-hours-load.sh` 2 min antes e comente no vídeo o que os gráficos mostram. Os números abaixo são **ilustrativos**, alinhados ao comportamento dos geradores de carga do lab — em produção você usaria 7–30 dias de histórico.

**Prompt IA — copiar e colar:**

```
Atue como Platform Engineer. Com base nos padrões abaixo, explique o comportamento de uso e o que isso implica para planejamento de capacidade e custo.

Contexto do ambiente:
- Cluster Kubernetes local (Minikube) com Prometheus/Grafana.
- Gerador de carga em modo demo: comprime um dia inteiro em ~12 minutos (comercial → fora do pico → noite/fim de semana).
- Em produção, a mesma análise usaria 7–30 dias para capturar sazonalidade real (seg–sex vs fim de semana).

Consumo CPU por namespace (mCPU, soma dos pods — leitura do Grafana, Last 15 minutes):
- payments: oscila entre ~30 na fase baixa e ~120+ na fase comercial (padrão variável, candidato a HPA)
- users: ~45–55 estável o tempo todo (carga constante, sem sazonalidade)
- staging: ~15–25 quase flat (quase idle o tempo todo)

Memória (uso por pod vs request configurado):
- payments: uso estável ~85 Mi por pod, request 1 Gi (grande folga)
- users: uso estável ~75 Mi por pod, request 128 Mi (uso próximo ao request de memória)
- staging: uso ~55 Mi por pod, request 512 Mi (subutilização persistente)

Responda em português do Brasil:
1. Classifique cada namespace: saudável, overprovisionado ou subdimensionado.
2. Há indício de workload que deveria escalar (HPA) ou desligar fora de horário?
3. Como você apresentaria esses padrões para um gestor de produto (sem jargão excessivo)?
4. Que alertas configuraria para evitar surpresa operacional?
```

\newpage

### Vídeo 1.4 — Alertas e visibilidade de custo orientados por contexto

| Campo | Valor |
|-------|-------|
| Tipo | **T+** |
| Tempo | 10–12 min |
| Dashboard | `grafana/dashboards/finops-ai-lab.json` |
| Prompt | `ai-prompts/aula-01/1.4-metricas-essenciais.md` |

**Objetivo:** Explicar como alertas contextualizados conectam observabilidade técnica com visibilidade de custo.

**Slides:**
- Slide 10: Alertas contextualizados para FinOps
- Slide 11: SLIs, SLOs e indicadores de custo
- Slide 12: Visibilidade de custo orientada por contexto

**O que mostrar:**
- Slides 10–12.
- Grafana → painéis do `finops-ai-lab.json`.
- Mencionar Prometheus (`localhost:9090`) — opcional.
- Gráficos do slide = exemplo conceitual; compare com Grafana ao vivo.

**Comandos:**

```bash
# Terminal B (opcional):
kubectl port-forward -n monitoring svc/monitoring-kube-prometheus-prometheus 9090:9090
# http://localhost:9090
```

**Antes de colar o prompt:**
Slides + menção Prometheus/Grafana. Gráficos de slide como exemplo conceitual.

**Prompt IA — copiar e colar:**

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

\newpage

### Vídeo 1.5 — Hands-on — análise operacional de consumo em cloud

| Campo | Valor |
|-------|-------|
| Tipo | **H** |
| Tempo | 12–15 min |
| Dashboard | `grafana/dashboards/finops-ai-lab.json` |
| Prompt | `ai-prompts/aula-01/1.5-panorama-consumo.md` |

**Objetivo:** Demonstrar análise operacional completa usando Grafana, kubectl e IA.

**Slides:**
Nenhum *(hands-on — apenas lab + dashboard + IA)*

**O que mostrar:**
- Sem slides (ou 1 slide de resumo).
- Grafana → `finops-ai-lab.json` → **Last 15 minutes**.
- Gauges por namespace + Top CPU/Memory Consumers.
- Comparar dados reais com exemplos dos slides anteriores.
- Colar saída de `collect-lab-context.sh` no prompt e comentar resposta da IA.

**Comandos:**

```bash
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
./scripts/start-business-hours-load.sh
sleep 120
./scripts/collect-lab-context.sh
kubectl get ns --show-labels
kubectl get deploy -A
kubectl top pods -A
```

**Antes de colar o prompt:**
Hands-on. Rode `./scripts/collect-lab-context.sh` e cole a saída no lugar dos dados de exemplo.

**Prompt IA — copiar e colar:**

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

\newpage

## Aula 2 — Rightsizing e eficiência operacional automatizada

**Dashboard:** `grafana/dashboards/finops-ai-rightsizing.json` | **Port-forwards:** Grafana (vídeos 2.2, 2.5)

### Vídeo 2.1 — O impacto do over-provisioning em ambientes modernos

| Campo | Valor |
|-------|-------|
| Tipo | **T** |
| Tempo | 8–10 min |
| Dashboard | `grafana/dashboards/finops-ai-rightsizing.json` |
| Prompt | `ai-prompts/aula-02/2.1-business-case-em.md` |

**Objetivo:** Explicar consequências de over-provisioning em custo, capacidade e operação.

**Slides:**
- Slide 1: Introdução — rightsizing operacional
- Slide 2: O impacto do over-provisioning
- Slide 3: Desperdício em ambientes modernos

**O que mostrar:**
- Slides 1–3.
- Citar `payments-api` como exemplo do lab (overprovisionado).
- Sem terminal.

**Comandos:** Nenhum.

**Antes de colar o prompt:**
Sem demo. Citar `payments-api` como exemplo do lab.

**Prompt IA — copiar e colar:**

```
Preciso traduzir uma otimização técnica de rightsizing em linguagem de negócio.

Dados:
- payments-api: economia estimada de 85% nos requests de CPU e 75% em memória após ajuste
- staging-api: economia adicional se desligado 12h/dia nos fins de semana
- users-api: já eficiente, sem ação imediata
- Esforço: 2 dias de engenharia + 1 semana de observação

Responda em português do Brasil:
1. Resumo executivo em 5 linhas para um Engineering Manager.
2. Tabela impacto vs. esforço vs. risco para as três iniciativas.
3. KPIs para medir sucesso após 30 dias (utilização, incidentes, custo alocado).
4. Uma frase de "por que agora" conectando eficiência operacional e margem do produto.
```

\newpage

### Vídeo 2.2 — Rightsizing baseado em comportamento real de workloads

| Campo | Valor |
|-------|-------|
| Tipo | **T+** |
| Tempo | 10–12 min |
| Dashboard | `grafana/dashboards/finops-ai-rightsizing.json` |
| Prompt | `ai-prompts/aula-02/2.2-rightsizing-payments-api.md` |

**Objetivo:** Mostrar como comparar requests vs uso real para identificar oportunidades de rightsizing.

**Slides:**
- Slide 4: Rightsizing baseado em comportamento real
- Slide 5: Margem de segurança operacional
- Slide 6: Usage vs Requests (conceito)

**O que mostrar:**
- Slides 4–6.
- Grafana → `finops-ai-rightsizing.json` → **Last 15 minutes**.
- Painéis: CPU/Memory Usage vs Requests, CPU Waste %.

**Comandos:**

```bash
# Grafana → finops-ai-rightsizing.json → Last 15 minutes
# Painéis: Usage vs Requests, Waste %
```

**Antes de colar o prompt:**
Dashboard `finops-ai-rightsizing.json`. Opcional: `./scripts/collect-lab-context.sh` para dados ao vivo.

**Prompt IA — copiar e colar:**

```
Você é um SRE com foco em rightsizing de workloads Kubernetes em produção.

Analise o deployment payments-api (namespace payments) e sugira novos requests/limits.

Dados atuais (2 réplicas):
- Requests: CPU 1000m, Memória 1 Gi
- Limits: CPU 1500m, Memória 2 Gi

Uso observado (7 dias, por pod):
- CPU média: 72m | CPU P95: 95m | CPU pico isolado: 120m
- Memória média: 88 Mi | Memória P95: 110 Mi | Pico: 125 Mi

Restrições:
- Manter margem de ~30% acima do P95 para requests
- Limits devem absorver picos sem OOMKill ou throttling agressivo
- Serviço é crítico (pagamentos), rollout gradual obrigatório

Responda em português do Brasil:
1. Valores sugeridos de requests e limits (CPU e memória) com justificativa.
2. Risco operacional de cada mudança (baixo/médio/alto) e mitigação.
3. Impacto estimado de capacidade liberada no cluster (CPU e memória agregadas).
4. Plano de rollout: ordem, monitoração durante 48h, critério de rollback.
5. Estimativa de economia relativa se o custo for proporcional aos requests (compare antes/depois em %).
```

\newpage

### Vídeo 2.3 — Ajustando recursos com automação operacional

| Campo | Valor |
|-------|-------|
| Tipo | **T+** |
| Tempo | 10–12 min |
| Dashboard | `grafana/dashboards/finops-ai-rightsizing.json` |
| Prompt | `ai-prompts/aula-02/2.3-automacao-vpa.md` |

**Objetivo:** Apresentar VPA, recomendações automatizadas e rollout gradual.

**Slides:**
- Slide 7: VPA e recomendações automatizadas
- Slide 8: HPA, VPA e rollout gradual
- Slide 9: Automação operacional de rightsizing

**O que mostrar:**
- Slides 7–9.
- Conceitual — mencionar requests/limits do payments-api.
- Opcional: `kubectl describe deployment payments-api -n payments`.

**Comandos:**

```bash
kubectl describe deployment payments-api -n payments
```

**Antes de colar o prompt:**
Conceitual. Mencionar `kubectl describe deployment payments-api -n payments`.

**Prompt IA — copiar e colar:**

```
Sou DevOps avaliando automação de rightsizing no cluster FinOps AI Lab (payments, users, staging).

Hoje os requests são definidos manualmente no YAML. Uso Prometheus para métricas reais.

Responda em português do Brasil:
1. Quando faz sentido usar VPA (Vertical Pod Autoscaler) vs. recomendações manuais assistidas por IA?
2. Para payments-api, users-api e staging-api, qual abordagem você recomenda e por quê?
3. Desenhe um fluxo simples: métrica → IA analisa → humano aprova → PR no GitOps.
4. Que guardrails impedem que automação reduza requests de serviço crítico sem aprovação?
5. Liste 3 anti-patterns comuns de rightsizing em Kubernetes que a IA não deve perpetuar.
```

\newpage

### Vídeo 2.4 — Scheduling inteligente e otimização de workloads

| Campo | Valor |
|-------|-------|
| Tipo | **T** |
| Tempo | 10–12 min |
| Dashboard | `grafana/dashboards/finops-ai-rightsizing.json` |
| Prompt | `ai-prompts/aula-02/2.4-comparativo-workloads.md` *(opcional)* |

**Objetivo:** Discutir otimização de workloads subutilizados e ambientes não produtivos.

**Slides:**
- Slide 10: Scheduling inteligente
- Slide 11: Otimização de workloads subutilizados
- Slide 12: Ambientes staging e scale-down

**O que mostrar:**
- Slides 10–12.
- Citar `staging-api` como workload subutilizado.
- Sem demo obrigatória.

**Comandos:** Nenhum.

**Antes de colar o prompt:**
Opcional. Conceitual — citar `staging-api` como workload subutilizado.

**Prompt IA — copiar e colar:**

```
Compare rightsizing entre três deployments e priorize por impacto financeiro.

| Workload      | NS       | Réplicas | CPU req | CPU P95 | Mem req | Mem P95 | Criticidade |
|---------------|----------|----------|---------|---------|---------|---------|-------------|
| payments-api  | payments | 2        | 1000m   | 95m     | 1 Gi    | 110 Mi  | Alta        |
| users-api     | users    | 2        | 100m    | 62m     | 128 Mi  | 92 Mi   | Alta        |
| staging-api   | staging  | 1        | 500m    | 35m     | 512 Mi  | 72 Mi   | Baixa       |

Premissa de custo (didática): custo alocável ≈ soma dos requests × preço unitário do cluster.

Responda em português do Brasil para um Platform Engineer:
1. Ranking de oportunidade de economia (1º ao 3º) com % estimado de redução de requests.
2. Para cada workload: requests/limits recomendados.
3. Qual mudança você faria na primeira sprint e qual deixaria para depois — e por quê.
4. O users-api precisa de alteração ou serve como baseline saudável?
5. staging-api: rightsizing ou scale-to-zero / desligamento noturno?
```

\newpage

### Vídeo 2.5 — Hands-on — pipeline de rightsizing operacional

| Campo | Valor |
|-------|-------|
| Tipo | **H** |
| Tempo | 12–15 min |
| Dashboard | `grafana/dashboards/finops-ai-rightsizing.json` |
| Prompt | `ai-prompts/aula-02/2.5-rightsizing-hands-on.md` |

**Objetivo:** Executar pipeline completo: métricas → análise → recomendação IA → plano de ação.

**Slides:**
Nenhum *(hands-on — apenas lab + dashboard + IA)*

**O que mostrar:**
- Sem slides.
- Grafana → `finops-ai-rightsizing.json` → CPU Waste, Top Overprovisioned, Candidates.
- Destacar **payments** (over) e **staging** (sub).
- Colar `collect-lab-context.sh` no prompt (Prompt A + B).
- Enfatizar: não aplicaria em prod sem validar em staging.

**Comandos:**

```bash
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
./scripts/collect-lab-context.sh
kubectl describe deployment payments-api -n payments
kubectl top pods -n payments
```

**Antes de colar o prompt:**
Hands-on. Rode `./scripts/collect-lab-context.sh` e substitua os dados de exemplo nos dois prompts abaixo.

**Prompt IA — copiar e colar:**

```
## Prompt A — Rightsizing do payments-api

Você é um SRE com foco em rightsizing de workloads Kubernetes em produção.

Analise o deployment payments-api (namespace payments) e sugira novos requests/limits.

Dados atuais (2 réplicas):
- Requests: CPU 1000m, Memória 1 Gi
- Limits: CPU 1500m, Memória 2 Gi

Uso observado (7 dias, por pod):
- CPU média: 72m | CPU P95: 95m | CPU pico isolado: 120m
- Memória média: 88 Mi | Memória P95: 110 Mi | Pico: 125 Mi

Restrições:
- Manter margem de ~30% acima do P95 para requests
- Limits devem absorver picos sem OOMKill ou throttling agressivo
- Serviço é crítico (pagamentos), rollout gradual obrigatório

Responda em português do Brasil:
1. Valores sugeridos de requests e limits (CPU e memória) com justificativa.
2. Risco operacional de cada mudança (baixo/médio/alto) e mitigação.
3. Impacto estimado de capacidade liberada no cluster (CPU e memória agregadas).
4. Plano de rollout: ordem, monitoração durante 48h, critério de rollback.
5. Estimativa de economia relativa se o custo for proporcional aos requests (compare antes/depois em %).

---

## Prompt B — Comparativo entre os três workloads

Compare rightsizing entre três deployments e priorize por impacto financeiro.

| Workload      | NS       | Réplicas | CPU req | CPU P95 | Mem req | Mem P95 | Criticidade |
|---------------|----------|----------|---------|---------|---------|---------|-------------|
| payments-api  | payments | 2        | 1000m   | 95m     | 1 Gi    | 110 Mi  | Alta        |
| users-api     | users    | 2        | 100m    | 62m     | 128 Mi  | 92 Mi   | Alta        |
| staging-api   | staging  | 1        | 500m    | 35m     | 512 Mi  | 72 Mi   | Baixa       |

Premissa de custo (didática): custo alocável ≈ soma dos requests × preço unitário do cluster.

Responda em português do Brasil para um Platform Engineer:
1. Ranking de oportunidade de economia (1º ao 3º) com % estimado de redução de requests.
2. Para cada workload: requests/limits recomendados.
3. Qual mudança você faria na primeira sprint e qual deixaria para depois — e por quê.
4. O users-api precisa de alteração ou serve como baseline saudável?
5. staging-api: rightsizing ou scale-to-zero / desligamento noturno?
```

\newpage

## Aula 3 — Anomalias de custo e capacity planning operacional

**Dashboard:** `grafana/dashboards/finops-ai-anomalies.json` | **Port-forwards:** Grafana (todos)

### Vídeo 3.1 — Detectando comportamento anormal de consumo

| Campo | Valor |
|-------|-------|
| Tipo | **T+** |
| Tempo | 8–10 min |
| Dashboard | `grafana/dashboards/finops-ai-anomalies.json` |
| Prompt | `ai-prompts/aula-03/3.1-deteccao-anomalia-cpu.md` |

**Objetivo:** Explicar baseline, desvio e detecção de anomalias operacionais.

**Slides:**
- Slide 1: Introdução — anomalias operacionais
- Slide 2: Baseline e detecção de desvio
- Slide 3: Comportamento anormal de consumo

**O que mostrar:**
- Slides 1–3.
- Grafana → `finops-ai-anomalies.json` → **Last 15 minutes**.
- Painel Payments CPU Timeline — baseline, **sem** cpu-spike ativo.

**Comandos:**

```bash
# Grafana → finops-ai-anomalies.json → Last 15 minutes
# Painel: Payments CPU Timeline (sem cpu-spike)
```

**Antes de colar o prompt:**
Dashboard sem spike ativo — baseline. Use dados de exemplo abaixo.

**Prompt IA — copiar e colar:**

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

\newpage

### Vídeo 3.2 — Investigando origem de anomalias operacionais

| Campo | Valor |
|-------|-------|
| Tipo | **T++** |
| Tempo | 10–12 min |
| Dashboard | `grafana/dashboards/finops-ai-anomalies.json` |
| Prompt | `ai-prompts/aula-03/3.2-investigacao-anomalia-cpu.md` |

**Objetivo:** Demonstrar processo de investigação: detectar → correlacionar → isolar causa.

**Slides:**
- Slide 4: Investigando origem de anomalias
- Slide 5: Correlação de eventos e métricas
- Slide 6: Processo de triagem

**O que mostrar:**
- Slides 4–6.
- Ativar spike com `start-anomaly.sh`.
- Terminal: pods e `kubectl top` em payments.
- Grafana → CPU Spike Detector (~30s).
- Explicar que `cpu-spike` simula anomalia.
- Encerrar com `stop-anomaly.sh`.

**Comandos:**

```bash
./scripts/start-anomaly.sh
kubectl get pods -n payments
kubectl top pods -n payments
# Grafana → CPU Spike Detector (~30s)
./scripts/stop-anomaly.sh
```

**Antes de colar o prompt:**
Com spike ativo. Rode `./scripts/start-anomaly.sh` e `./scripts/collect-anomaly-context.sh` — cole a saída no lugar dos dados de exemplo.

**Prompt IA — copiar e colar:**

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

\newpage

### Vídeo 3.3 — Planejamento operacional de capacidade

| Campo | Valor |
|-------|-------|
| Tipo | **T+** |
| Tempo | 10–12 min |
| Dashboard | `grafana/dashboards/finops-ai-anomalies.json` |
| Prompt | `ai-prompts/aula-03/3.3-capacity-planning.md` |

**Objetivo:** Apresentar capacity planning com headroom, allocatable e projeções.

**Slides:**
- Slide 7: Capacity planning operacional
- Slide 8: Headroom e projeções
- Slide 9: Planejamento pós-incidente

**O que mostrar:**
- Slides 7–9.
- Grafana → painel **Capacity Headroom** no dashboard anomalies.
- Gráficos do slide = exemplo conceitual.

**Comandos:**

```bash
# Grafana → finops-ai-anomalies.json → Capacity Headroom
```

**Antes de colar o prompt:**
Painel Capacity Headroom no dashboard `finops-ai-anomalies.json`.

**Prompt IA — copiar e colar:**

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

\newpage

### Vídeo 3.4 — Otimizando uso de recursos em cloud

| Campo | Valor |
|-------|-------|
| Tipo | **T++** |
| Tempo | 10–12 min |
| Dashboard | `grafana/dashboards/finops-ai-anomalies.json` |
| Prompt | `ai-prompts/aula-03/3.4-anomalia-silenciosa-staging.md` |

**Objetivo:** Discutir estratégias de otimização pós-anomalia e prevenção.

**Slides:**
- Slide 10: Otimização de recursos pós-anomalia
- Slide 11: Anomalias silenciosas de custo
- Slide 12: Prevenção e políticas

**O que mostrar:**
- Slides 10–12.
- Ativar `start-staging-anomaly.sh`.
- Terminal: jobs `backup-sync` em staging.
- Mostrar staging-api estável, mas jobs geram rajadas de CPU/custo.
- Encerrar com `stop-staging-anomaly.sh`.

**Comandos:**

```bash
./scripts/start-staging-anomaly.sh
kubectl get jobs -n staging -l app=backup-sync
kubectl top pods -n staging
./scripts/stop-staging-anomaly.sh
```

**Antes de colar o prompt:**
Com `./scripts/start-staging-anomaly.sh` ativo. Encerre com `./scripts/stop-staging-anomaly.sh`.

**Prompt IA — copiar e colar:**

```
O namespace staging não teve spike de CPU, mas o custo alocado subiu 22% na última semana sem deploy novo visível.

Dados:
- staging-api: 1 réplica, requests 500m CPU / 512 Mi, uso médio 28m CPU
- Novo CronJob detectado: backup-sync (no lab: a cada 2 min; em produção: ~15 min — pico ~400m CPU por ~90s)
- Labels: team=platform, environment=staging, cost-center=engineering
- Nenhuma mudança em payments ou users

Responda em português do Brasil:
1. Por que este é um caso de "anomalia de custo" e não de "incidente de disponibilidade"?
2. Como correlacionar CronJobs/Jobs com custo no OpenCost e no Prometheus?
3. O staging-api ainda deve ser rightsized ou o problema é o CronJob?
4. Políticas de governança que evitariam CronJobs órfãos em staging.
5. Mensagem para o time platform: tom colaborativo, foco em eficiência.
```

\newpage

### Vídeo 3.5 — Hands-on — análise de anomalias e capacidade operacional

| Campo | Valor |
|-------|-------|
| Tipo | **H** |
| Tempo | 12–15 min |
| Dashboard | `grafana/dashboards/finops-ai-anomalies.json` |
| Prompt | `ai-prompts/aula-03/3.5-runbook-anomalias.md` |

**Objetivo:** Fluxo completo: baseline → spike → investigação → capacity → encerramento.

**Slides:**
Nenhum *(hands-on — apenas lab + dashboard + IA)*

**O que mostrar:**
- Sem slides.
- Grafana → `finops-ai-anomalies.json` → **Last 15 minutes**.
- Fluxo: baseline (business-hours) → spike → Top CPU Consumers → Capacity Headroom.
- Colar `collect-anomaly-context.sh` no prompt.
- `stop-all-anomalies.sh` → confirmar retorno ao baseline.

**Comandos:**

```bash
./scripts/stop-all-anomalies.sh
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
./scripts/start-business-hours-load.sh
sleep 120
./scripts/start-anomaly.sh
./scripts/collect-anomaly-context.sh
./scripts/stop-all-anomalies.sh
```

**Antes de colar o prompt:**
Hands-on. Cole a saída de `./scripts/collect-anomaly-context.sh` no final do prompt, se disponível.

**Prompt IA — copiar e colar:**

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

\newpage

## Aula 4 — Governança operacional e visibilidade de custos

**Dashboard:** `grafana/dashboards/finops-ai-governance.json` | **Port-forwards:** Grafana (4.2+) + OpenCost (4.3, 4.5)

### Vídeo 4.1 — Ownership e responsabilidade sobre consumo cloud

| Campo | Valor |
|-------|-------|
| Tipo | **T+** |
| Tempo | 8–10 min |
| Dashboard | `grafana/dashboards/finops-ai-governance.json` |
| Prompt | `ai-prompts/aula-04/4.1-auditoria-labels.md` |

**Objetivo:** Explicar ownership, responsabilidade e accountability sobre consumo.

**Slides:**
- Slide 1: Introdução — governança FinOps
- Slide 2: Ownership e responsabilidade
- Slide 3: Accountability sobre consumo cloud

**O que mostrar:**
- Slides 1–3.
- Terminal: `kubectl get ns --show-labels` — team, environment, cost-center.

**Comandos:**

```bash
kubectl get ns --show-labels
```

**Antes de colar o prompt:**
Rode `./scripts/collect-lab-context.sh` e substitua a tabela de labels pelos dados reais.

**Prompt IA — copiar e colar:**

```
Você é Platform Engineer responsável por governança de custos em Kubernetes.

Labels atuais dos namespaces:

| Namespace | team     | environment | cost-center  |
|-----------|----------|-------------|--------------|
| payments  | payments | prod        | product      |
| users     | users    | prod        | product      |
| staging   | platform | staging     | engineering  |

Workloads herdam labels de team e environment nos pods. Não há label owner nem service-tier.

Responda em português do Brasil:
1. Score de maturidade de labeling (0–10) com gaps críticos.
2. Labels adicionais recomendados para FinOps (nome, exemplo, obrigatoriedade).
3. Como mapear ownership quando team=platform mas o workload é de outro squad?
4. Impacto de labels ausentes na alocação do OpenCost e em relatórios de showback.
5. Plano de 30 dias para corrigir governança sem bloquear deploys (admission policy gradual).
```

\newpage

### Vídeo 4.2 — Classificação operacional de recursos e ambientes

| Campo | Valor |
|-------|-------|
| Tipo | **T+** |
| Tempo | 10–12 min |
| Dashboard | `grafana/dashboards/finops-ai-governance.json` |
| Prompt | `ai-prompts/aula-04/4.2-politica-ambientes.md` |

**Objetivo:** Apresentar classificação por team, environment, cost-center e service-tier.

**Slides:**
- Slide 4: Classificação de recursos
- Slide 5: Tagging (team, environment, cost-center)
- Slide 6: Política prod vs staging

**O que mostrar:**
- Slides 4–6.
- Grafana → `finops-ai-governance.json` → painel **Governance Matrix**.

**Comandos:**

```bash
# Grafana → finops-ai-governance.json → Governance Matrix
```

**Antes de colar o prompt:**
Painel Governance Matrix no dashboard `finops-ai-governance.json`.

**Prompt IA — copiar e colar:**

```
Avalie a governança do ambiente staging frente a payments e users (prod).

Fatos:
- staging: environment=staging, cost-center=engineering, 1 réplica staging-api, uso CPU ~5% do request
- payments/users: environment=prod, cost-center=product, SLO implícito de disponibilidade
- Custo alocado de staging ≈ 29% do total com utilização real baixa
- Time platform argumenta que staging "precisa estar sempre disponível para QA"

Responda em português do Brasil:
1. A política atual é sustentável? Alternativas (auto shutdown, cluster separado, namespaces efêmeros).
2. Regras claras: o que pode e não pode rodar em staging (CPU stress, jobs longos, réplicas ociosas).
3. Como negociar com QA/Platform sem comprometer qualidade de release?
4. Template de política de namespace (1 página, bullets objetivos).
5. Indicadores para revisar a política trimestralmente.
```

\newpage

### Vídeo 4.3 — Alocação de custos orientada por contexto

| Campo | Valor |
|-------|-------|
| Tipo | **T+** |
| Tempo | 10–12 min |
| Dashboard | `grafana/dashboards/finops-ai-governance.json` |
| Prompt | `ai-prompts/aula-04/4.3-showback-chargeback.md` |

**Objetivo:** Explicar showback, chargeback e alocação por contexto operacional.

**Slides:**
- Slide 7: Showback
- Slide 8: Chargeback
- Slide 9: Alocação orientada por contexto

**O que mostrar:**
- Slides 7–9.
- Grafana → painel **Showback View**.
- OpenCost → `http://localhost:9003` (Allocation, Namespace Costs).
- Opcional: screenshot AWS Cost Explorer.

**Comandos:**

```bash
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
kubectl port-forward -n opencost svc/opencost 9003:9090
# Grafana → Showback View | http://localhost:9003
```

**Antes de colar o prompt:**
Painel Showback View + OpenCost (`localhost:9003`).

**Prompt IA — copiar e colar:**

```
Preciso explicar showback e chargeback para times de produto usando dados do lab.

Alocação de custo mensal estimada (didática):
- payments (team=payments, cost-center=product): R$ 12.400 — 62% do total
- users (team=users, cost-center=product): R$ 1.800 — 9%
- staging (team=platform, cost-center=engineering): R$ 5.800 — 29%

Contexto:
- payments-api overprovisionado é o principal driver de custo em payments
- staging tem baixo uso real mas requests altos
- Empresa quer accountability sem transferir dinheiro entre departamentos ainda (fase 1)

Responda em português do Brasil:
1. Neste cenário, showback ou chargeback? Justifique.
2. Como apresentar o relatório para o time payments sem parecer punição?
3. Métricas de eficiência por cost-center (custo por request, custo por réplica, % de utilização).
4. Roadmap em 3 fases: visibilidade → metas → chargeback opcional.
5. Script de 1 minuto para gravar no curso explicando a diferença dos modelos.
```

\newpage

### Vídeo 4.4 — Guardrails e políticas de eficiência operacional

| Campo | Valor |
|-------|-------|
| Tipo | **T+** |
| Tempo | 10–12 min |
| Dashboard | `grafana/dashboards/finops-ai-governance.json` |
| Prompt | `ai-prompts/aula-04/4.4-guardrails.md` |

**Objetivo:** Apresentar ResourceQuota, LimitRange, labels obrigatórios e políticas Kyverno/OPA.

**Slides:**
- Slide 10: Guardrails e políticas
- Slide 11: ResourceQuota, LimitRange, OPA/Kyverno
- Slide 12: Eficiência sem atrito

**O que mostrar:**
- Slides 10–12.
- Grafana → painel **Guardrails Checklist** (conceitual — não deployado no lab).

**Comandos:**

```bash
# Grafana → finops-ai-governance.json → Guardrails Checklist
```

**Antes de colar o prompt:**
Painel Guardrails Checklist no dashboard governance.

**Prompt IA — copiar e colar:**

```
Proponha guardrails de governança para o cluster FinOps AI Lab.

Problemas observados:
- Deploy de cpu-spike em payments sem label de ambiente=ephemeral
- staging-api com requests de produção mas tráfego de homologação
- Nenhuma ResourceQuota por namespace
- Times podem criar workloads em qualquer namespace com RBAC amplo

Responda em português do Brasil para DevOps/Platform:
1. Top 5 guardrails priorizados (quota, limitRange, OPA/Gatekeeper, labels obrigatórios, etc.).
2. Para cada guardrail: o que bloqueia, o que apenas alerta, esforço de implementação.
3. Exemplo de ResourceQuota para staging vs. payments (valores sugeridos).
4. Política de labels obrigatórios: validação no admission webhook.
5. Como medir se os guardrails estão funcionando (KPIs em 60 dias).
```

\newpage

### Vídeo 4.5 — Hands-on — dashboard operacional de custos e governança

| Campo | Valor |
|-------|-------|
| Tipo | **H** |
| Tempo | 12–15 min |
| Dashboard | `grafana/dashboards/finops-ai-governance.json` |
| Prompt | `ai-prompts/aula-04/4.5-visibilidade-persona.md` |

**Objetivo:** Demonstrar visibilidade completa: labels, showback proxy, OpenCost e governança.

**Slides:**
Nenhum *(hands-on — apenas lab + dashboard + IA)*

**O que mostrar:**
- Sem slides.
- Grafana → Matrix, Showback, Guardrails.
- OpenCost → custo por namespace/workload.
- Colar `collect-lab-context.sh` no prompt.
- Opcional: comparar com screenshot AWS Cost Explorer.

**Comandos:**

```bash
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
kubectl port-forward -n opencost svc/opencost 9003:9090
./scripts/collect-lab-context.sh
kubectl get ns --show-labels
```

**Antes de colar o prompt:**
Hands-on. Rode `./scripts/collect-lab-context.sh` e substitua dados de exemplo, se aplicável.

**Prompt IA — copiar e colar:**

```
Desenhe visibilidade de custos para três personas usando payments, users e staging.

Personas:
- SRE on-call: precisa achar desperdício e risco de saturação rápido
- FinOps analyst: precisa alocar custo por time e cost-center
- Engineering Manager do produto: precisa priorizar backlog de eficiência

Dados disponíveis: Prometheus, Grafana (dashboard finops-ai-lab.json), OpenCost, labels nos namespaces.

Responda em português do Brasil:
1. Um dashboard ou view por persona (métricas, filtros, frequência de revisão).
2. Perguntas que cada persona deve conseguir responder em menos de 2 minutos.
3. Como o EM do time payments deve interpretar que seu namespace é 62% do custo.
4. Rituais recomendados: daily (SRE), weekly (FinOps), monthly (EM + platform).
5. Erros comuns ao expor custo para engenharia (e como evitar).
```

\newpage

## Aula 5 — Operações cloud orientadas por eficiência

**Dashboard:** `Todos os dashboards anteriores` | **Port-forwards:** Grafana (5.1, 5.5) + OpenCost (5.5)

### Vídeo 5.1 — Relacionando custo, performance e observabilidade

| Campo | Valor |
|-------|-------|
| Tipo | **T+** |
| Tempo | 8–10 min |
| Dashboard | `Todos os dashboards anteriores` |
| Prompt | `ai-prompts/aula-05/5.1-diagnostico-consolidado.md` |

**Objetivo:** Conectar os três pilares e mostrar trade-offs em decisões operacionais.

**Slides:**
- Slide 1: Introdução — eficiência operacional contínua
- Slide 2: Custo × performance × observabilidade
- Slide 3: Trade-offs operacionais

**O que mostrar:**
- Slides 1–3.
- Tour rápido nos 4 dashboards Grafana (~30s cada).

**Comandos:**

```bash
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
# finops-ai-lab → rightsizing → anomalies → governance
```

**Antes de colar o prompt:**
Tour rápido nos 4 dashboards. Opcional: `./scripts/collect-lab-context.sh`.

**Prompt IA — copiar e colar:**

```
Você é consultor de FinOps e SRE. Faça diagnóstico consolidado do cluster FinOps AI Lab.

Stack: Minikube, Prometheus, Grafana, OpenCost.

Namespaces e workloads:
| NS       | Workload      | Réplicas | CPU req (total) | CPU uso médio | Mem req (total) | Mem uso média | Labels principais                    |
|----------|---------------|----------|-----------------|---------------|-----------------|---------------|--------------------------------------|
| payments | payments-api  | 2        | 2000m           | 145m          | 2 Gi            | 176 Mi        | team=payments, env=prod              |
| payments | cpu-spike*    | 0–1      | 0–500m          | 0–2000m       | 0–128 Mi        | variável      | *anomalia pontual para demo          |
| users    | users-api     | 2        | 200m            | 96m           | 256 Mi          | 152 Mi        | team=users, env=prod                 |
| staging  | staging-api   | 1        | 500m            | 28m           | 512 Mi          | 58 Mi         | team=platform, env=staging           |

Achados das aulas anteriores:
- Over-provisioning crítico em payments-api
- users-api relativamente saudável
- staging subutilizado com custo alocado desproporcional
- Anomalia cpu-spike demonstra gap de alertas e governança

Responda em português do Brasil:
1. Resumo executivo (10 linhas) do estado do ambiente.
2. Top 5 achados ordenados por impacto em custo e risco operacional.
3. Quick wins executáveis em 2 semanas.
4. Iniciativas estruturais para 90 dias.
5. O que monitorar para provar que a eficiência melhorou (KPIs com metas numéricas).
```

\newpage

### Vídeo 5.2 — Tomada de decisão orientada por dados operacionais

| Campo | Valor |
|-------|-------|
| Tipo | **T** |
| Tempo | 10–12 min |
| Dashboard | `Todos os dashboards anteriores` |
| Prompt | `ai-prompts/aula-05/5.2-priorizacao-matriz.md` |

**Objetivo:** Apresentar matriz impacto × esforço e priorização de ações.

**Slides:**
- Slide 4: Tomada de decisão orientada por dados
- Slide 5: Matriz impacto × esforço
- Slide 6: Priorização de ações

**O que mostrar:**
- Slides 4–6.
- Resumir achados do lab em tabela (conceitual).
- Sem lab obrigatório.

**Comandos:** Nenhum.

**Antes de colar o prompt:**
Conceitual. Resumir achados do lab em tabela antes de colar.

**Prompt IA — copiar e colar:**

```
Priorize as ações abaixo usando matriz impacto × esforço × risco.

Ações candidatas:
A. Rightsizing payments-api (CPU 1000m→150m, mem 1Gi→256Mi por pod)
B. Rightsizing staging-api + janela de desligamento noturno
C. Implementar ResourceQuota e LimitRange por namespace
D. Alertas de CPU e custo para anomalias tipo cpu-spike
E. Dashboards de showback por cost-center no Grafana
F. VPA em modo recommendation apenas para users-api
G. Política de labels obrigatórios (admission webhook)
H. Revisão trimestral de requests com ritual FinOps

Responda em português do Brasil:
1. Matriz com classificação de cada ação (impacto/esforço/risco).
2. Sequência recomendada de execução (1ª à 8ª) com justificativa em 1 linha cada.
3. Dependências entre ações (ex.: alertas antes ou depois de rightsizing?).
4. Qual ação traz maior valor percebido pelo C-level com menor esforço?
5. Qual ação você faria primeiro se tivesse apenas 1 dia de trabalho?
```

\newpage

### Vídeo 5.3 — Eficiência operacional contínua em ambientes modernos

| Campo | Valor |
|-------|-------|
| Tipo | **T** |
| Tempo | 10–12 min |
| Dashboard | `Todos os dashboards anteriores` |
| Prompt | `ai-prompts/aula-05/5.3-plano-90-dias.md` |

**Objetivo:** Apresentar ciclo contínuo de eficiência e plano de 90 dias.

**Slides:**
- Slide 7: Eficiência contínua
- Slide 8: Plano de otimização (90 dias)
- Slide 9: Forecast e projeção (exemplo conceitual)

**O que mostrar:**
- Slides 7–9.
- Sem lab.
- Opcional: screenshot AWS Cost Explorer forecast.

**Comandos:** Nenhum.

**Antes de colar o prompt:**
Sem demo. Slides de eficiência contínua.

**Prompt IA — copiar e colar:**

```
Monte um plano de otimização contínua de 90 dias para o FinOps AI Lab, aplicável como modelo em produção real.

Times envolvidos:
- Squad payments (dono payments-api)
- Squad users (dono users-api)
- Platform (dono staging, cluster, observabilidade)
- FinOps (alocação, relatórios, metas)

Restrições:
- Zero downtime em payments e users
- Mudanças em staging podem ser mais agressivas
- Orçamento de engenharia: ~20% de 1 platform engineer + suporte pontual dos squads

Responda em português do Brasil:
1. Roadmap por sprint (12 semanas): tema, entregável, dono, dependência.
2. Para cada iniciativa: impacto esperado (alto/médio/baixo), risco, esforço.
3. Rituais FinOps + SRE (review semanal de eficiência, game day de anomalia).
4. Critérios de "done" para encerrar a fase de otimização.
5. Como evitar regressão (requests voltarem a inflar após 6 meses).
```

\newpage

### Vídeo 5.4 — Construindo uma cultura operacional orientada por eficiência

| Campo | Valor |
|-------|-------|
| Tipo | **T** |
| Tempo | 10–12 min |
| Dashboard | `Todos os dashboards anteriores` |
| Prompt | `ai-prompts/aula-05/5.4-recomendacoes-executivas.md` |

**Objetivo:** Fechar o arco do curso com cultura, KPIs e governança de longo prazo.

**Slides:**
- Slide 10: Cultura FinOps
- Slide 11: KPIs executivos
- Slide 12: Fechamento do curso

**O que mostrar:**
- Slides 10–12.
- Sem lab.

**Comandos:** Nenhum.

**Antes de colar o prompt:**
Sem demo. Slides de cultura FinOps e KPIs.

**Prompt IA — copiar e colar:**

```
Transforme a análise técnica do FinOps AI Lab em recomendações executivas.

Números consolidados (estimativa didática, mensal):
- Custo alocado total: R$ 20.000
- Potencial de redução identificado: 35–45% em 90 dias sem perda de SLA
- Maior driver: requests inflados em payments (62% do custo, ~15% de utilização média)
- Incidente demo cpu-spike: +R$ 14 de custo evitável em 1h com detecção tardia
- Maturidade de governança: labels básicos ok, faltam quotas, alertas e rituais

Audiência: CTO e VP Engineering — técnica o suficiente, foco em decisão.

Responda em português do Brasil:
1. Memo executivo (máximo 250 palavras).
2. Três decisões que precisam de patrocínio executivo.
3. Riscos de NÃO agir nos próximos 6 meses (operacional e financeiro).
4. Investimento necessário (pessoas, ferramentas, tempo) vs. retorno esperado.
5. Uma métrica norte para acompanhar no board mensal.
```

\newpage

### Vídeo 5.5 — Hands-on — fluxo operacional completo de FinOps com IA

| Campo | Valor |
|-------|-------|
| Tipo | **H** |
| Tempo | 12–15 min |
| Dashboard | `Todos os dashboards anteriores` |
| Prompt | `ai-prompts/aula-05/5.5-copiloto-eficiencia.md` |

**Objetivo:** Executar fluxo end-to-end: observar → rightsizing → anomalias → governança → plano consolidado com IA.

**Slides:**
Nenhum *(hands-on — apenas lab + dashboard + IA)*

**O que mostrar:**
- Sem slides.
- Percorrer 4 dashboards (1 min cada) → **Last 15 minutes**.
- Resumo: payments over, users ok, staging sub, anomalias = lição.
- OpenCost → visão consolidada.
- Colar `collect-lab-context.sh` no **prompt mestre**.
- Apresentar plano de 90 dias e KPIs da resposta da IA.

**Comandos:**

```bash
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
kubectl port-forward -n opencost svc/opencost 9003:9090
./scripts/collect-lab-context.sh
kubectl top pods -A
```

**Antes de colar o prompt:**
Hands-on final. Cole `./scripts/collect-lab-context.sh` na seção `[DADOS]`. Mostre como salvar como template reutilizável.

**Prompt IA — copiar e colar:**

```
A partir de agora, atue como meu copiloto de eficiência operacional em Kubernetes e FinOps.

Regras:
- Respostas em português do Brasil, linguagem para SRE/DevOps/Platform
- Sempre separar: fato observado, hipótese, recomendação, risco
- Nunca sugerir mudança em produção sem plano de rollback
- Priorizar por impacto financeiro e segurança operacional
- Pedir dados faltantes antes de concluir se eu não informar

Meu ambiente:
- Cluster: Minikube (4 CPU, 8 Gi RAM)
- Observabilidade: Prometheus, Grafana, OpenCost
- Namespaces: payments (payments-api), users (users-api), staging (staging-api)
- Labels: team, environment, cost-center em cada namespace

Vou colar métricas atualizadas abaixo. Analise e devolva:
1. Diagnóstico em 5 bullets
2. Top 3 ações priorizadas
3. Comandos kubectl ou queries PromQL úteis para validar
4. Mensagem curta para o time dono do workload

[DADOS — cole aqui métricas do Grafana, OpenCost ou kubectl top]
```

\newpage

---

## Parte 3 — Checklist de gravação

Checklist operacional para garantir qualidade técnica e consistência em cada sessão de gravação.

---

## Checklist antes da gravação (geral)

### Ambiente local

- [ ] Minikube rodando (`minikube status`)
- [ ] `kubectl cluster-info` responde sem erro
- [ ] Helm instalado e funcional
- [ ] Repositório clonado e atualizado na máquina de gravação

### Stack do laboratório

- [ ] Prometheus instalado (`kubectl get pods -n monitoring`)
- [ ] Grafana acessível via port-forward (`localhost:3000`)
- [ ] OpenCost instalado (`kubectl get pods -n opencost`)
- [ ] Workloads do lab rodando (`kubectl get deploy -A | grep -E 'payments|users|staging'`)
- [ ] `./scripts/warmup-lab-metrics.sh` executado (metricas nos dashboards)
- [ ] Anomalias **desativadas** (`./scripts/stop-all-anomalies.sh` executado)

### Dashboards

- [ ] `finops-ai-lab.json` importado no Grafana
- [ ] `finops-ai-rightsizing.json` importado no Grafana
- [ ] `finops-ai-anomalies.json` importado no Grafana
- [ ] `finops-ai-governance.json` importado no Grafana
- [ ] Datasource Prometheus selecionado em todos os dashboards
- [ ] Painéis exibindo dados (sem "No data")

### Materiais de apoio

- [ ] Slides da aula abertos e revisados
- [ ] Manual completo aberto (`docs/manual-gravacao-completo.md` ou PDF `docs/manual-gravacao-completo.pdf`)

### Setup de gravação

- [ ] Terminal limpo (sem histórico confuso ou credenciais visíveis)
- [ ] Navegador sem abas pessoais (apenas Grafana, Prometheus, OpenCost, IA)
- [ ] Notificações do sistema desativadas (modo Não Perturbe)
- [ ] Microfone testado e nível de áudio adequado
- [ ] Zoom da tela entre 100% e 125% (texto legível)
- [ ] Credenciais sensíveis escondidas (senha Grafana, tokens, `.env`)
- [ ] Resolução de gravação configurada (mín. 1280×720)
- [ ] Port-forwards necessários abertos em terminais separados

---

## Checklist por aula

### Aula 1 — Observabilidade

- [ ] Dashboard principal (`finops-ai-lab.json`) importado e com dados
- [ ] Port-forward do Grafana ativo
- [ ] `kubectl get ns --show-labels` testado
- [ ] `kubectl get deploy -A` testado
- [ ] `kubectl top pods -A` retorna métricas
- [ ] Seção da Aula 1 no manual revisada (vídeos 1.1–1.5)

### Aula 2 — Rightsizing

- [ ] Dashboard rightsizing (`finops-ai-rightsizing.json`) importado e com dados
- [ ] Painel CPU Waste Percentage mostra payments com waste alto
- [ ] `kubectl describe deployment payments-api -n payments` testado
- [ ] Seção da Aula 2 no manual revisada (vídeos 2.1–2.5)

### Aula 3 — Anomalias

- [ ] Dashboard anomalies (`finops-ai-anomalies.json`) importado e com dados
- [ ] `./scripts/start-anomaly.sh` testado — spike visível no Grafana em ~30s
- [ ] `./scripts/start-staging-anomaly.sh` testado — job `backup-sync` criado imediatamente
- [ ] `./scripts/stop-all-anomalies.sh` testado — baseline restaurado
- [ ] `./scripts/collect-anomaly-context.sh` testado — saída utilizável nos prompts
- [ ] Seção da Aula 3 no manual revisada (vídeos 3.1–3.5)

### Aula 4 — Governança

- [ ] Dashboard governance (`finops-ai-governance.json`) importado e com dados
- [ ] Port-forward do OpenCost ativo (`localhost:9003`)
- [ ] `kubectl get ns --show-labels` mostra labels team, environment, cost-center
- [ ] Seção da Aula 4 no manual revisada (vídeos 4.1–4.5)
- [ ] *(Opcional)* Screenshot do AWS Cost Explorer preparado

### Aula 5 — Eficiência operacional

- [ ] Todos os 4 dashboards acessíveis no Grafana
- [ ] Port-forwards Grafana + OpenCost ativos
- [ ] Seção da Aula 5 no manual revisada (vídeo 5.5 — prompt mestre)
- [ ] Achados das aulas 1–4 anotados para o fluxo completo
- [ ] *(Opcional)* Screenshot do AWS Cost Explorer preparado

---

## Checklist durante a gravação

- [ ] Nome do vídeo anunciado no início (ex.: "Vídeo 2.5 — Hands-on rightsizing")
- [ ] Dados reais do lab mencionados (não apenas exemplos dos slides)
- [ ] Gráficos de slide explicados como exemplos conceituais quando aplicável
- [ ] Resposta da IA comentada criticamente (não aceitar cegamente)
- [ ] Comandos executados em ritmo legível (pausar após output importante)
- [ ] Erros técnicos anotados em tempo real para revisão posterior

---

## Checklist pós-gravação

Preencha para **cada vídeo** gravado:

| Campo | Vídeo ___ |
|-------|-----------|
| Arquivo salvo | [ ] Sim |
| Nome padronizado | [ ] `aula-XX-video-XX-titulo-curto.mp4` |
| Vídeo revisado (assistido pelo menos 1x) | [ ] Sim |
| Erro técnico anotado | [ ] Sim / [ ] Não — descrição: ___________ |
| Regravação necessária? | [ ] Sim / [ ] Não |

### Critérios para marcar regravação

Marque **Sim** se:

- Comando falhou visivelmente e não foi corrigido na gravação
- Dashboard mostrou "No data" durante a demo principal
- Credencial sensível apareceu na tela
- Áudio inaudível por mais de 10 segundos
- Demo principal (hands-on) não foi concluída

### Nome padronizado sugerido

```text
aula-01-video-01-desafio-eficiencia.mp4
aula-01-video-05-hands-on-observabilidade.mp4
aula-03-video-05-hands-on-anomalias.mp4
aula-05-video-05-hands-on-fluxo-completo.mp4
```

---

## Checklist de entrega final (após os 25 vídeos)

- [ ] 25 vídeos gravados e nomeados
- [ ] Todos os vídeos revisados
- [ ] Regravações concluídas
- [ ] Screenshots exportados (se aplicável)
- [ ] Erros técnicos documentados para melhoria do lab

*Gerado automaticamente por `scripts/generate-manual-gravacao.py`*