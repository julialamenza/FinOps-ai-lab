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
| 2 | `grafana/dashboards/finops-ai-rightsizing.json` | Grafana (vídeo 2.5) |
| 3 | `grafana/dashboards/finops-ai-anomalies.json` | Grafana (vídeo 3.5) |
| 4 | `grafana/dashboards/finops-ai-governance.json` | Grafana + OpenCost (vídeo 4.5) |
| 5 | `Todos os dashboards anteriores` | Grafana + OpenCost (vídeo 5.5) |

O curso roda em **Minikube local**. **Não é obrigatório** ter Kubernetes na AWS (EKS), conta AWS ativa, nem abrir o console AWS ao vivo.

## O que demo ao vivo vs conceitual

| Ferramenta AWS | Demo ao vivo? | Vídeos |
|----------------|---------------|--------|
| **Cost Explorer** | Opcional (screenshot ou console) | **4.4** (principal), menção em 5.3 |
| **Billing (fatura)** | Não — conceitual ou screenshot | 4.4, 5.3, 5.5 (plano 90 dias) |
| **Budgets / alertas de billing** | Não — conceitual ou screenshot | 4.3, 5.3, 5.5 |
| **OpenCost** (no Minikube) | **Sim** — demo principal | 4.5, 5.5 |

**Hands-on (4.5 e 5.5):** use **OpenCost** (`http://localhost:9003`) + Grafana. **Não abra** Cost Explorer nem Billing durante o hands-on — fica confuso e não reflete o lab.

## Três modos de gravação

### Modo A — Sem conta AWS *(recomendado)*

- Use **slides** + painel *OpenCost + AWS Cost Explorer* no dashboard `finops-ai-governance.json`.
- Fale: *"Nosso lab é Minikube local; em produção o Cost Explorer mostraria a fatura cloud e o OpenCost alocaria por namespace."*
- Caso EKS +30% do slide = **cenário ilustrativo**, não precisa existir na sua conta.

### Modo B — Com conta AWS, sem EKS

- **Screenshot** do Cost Explorer (*Cost by Service*, últimos 30 dias) — qualquer serviço (EC2, S3, etc.) serve para mostrar visão de conta.
- **Budgets:** screenshot de um budget de exemplo ou slide; explique alertas por e-mail/SNS quando custo > 80% do budget.
- **Não precisa** linha EKS na fatura — o cruzamento com namespace continua sendo explicado com OpenCost local.

### Modo C — Com EKS *(opcional, produção)*

- Cost Explorer filtrado em *Elastic Kubernetes Service* + OpenCost por namespace.
- Mostre cruzamento real: fatura EKS subiu → OpenCost aponta namespace/workload.

## Script de fala (~30 s) — vídeo 4.4

> "O lab roda em Minikube — não temos cluster na AWS. O OpenCost simula custo por namespace com preços públicos AWS. O Cost Explorer, em produção, mostra o custo **real da infra cloud** — EC2, EKS, load balancers, storage. As duas ferramentas se complementam: a fatura sobe no Billing → Cost Explorer aponta o **serviço** → OpenCost aponta o **namespace/workload**. Budgets e alertas de billing avisam **antes** da surpresa na fatura; alertas no Grafana/OpenCost avisam **dentro** do cluster."

## Onde cada conceito aparece

| Vídeo | Slide | AWS console? | O que fazer |
|-------|-------|--------------|-------------|
| 1.4 | 10–12 | Não | Alertas = Grafana/Prometheus; mencione que em produção **Billing alerts** complementam |
| 4.3 | 7 | Não | FinOps persona: budget vs actual — **conceitual**; cite AWS Budgets como exemplo |
| **4.4** | **8** | **Opcional** | **Cost Explorer + Billing + Budgets** — teoria; screenshot ou Modo A |
| 4.5 | 9–10 | **Não** | OpenCost + Grafana ao vivo; painel comparativo no dashboard = referência |
| 5.3 | 7 | Não | OpenCost vs Cost Explorer — complementares; sem abrir AWS |
| 5.4 | 8 | Não | Estágio Governança = budgets — conceitual |
| 5.5 | 9–10 | **Não** | Plano 90 dias cita budgets/alertas — OpenCost + 4 dashboards ao vivo |

## Screenshots sugeridos (Modo A ou B)

Salve em `docs/screenshots/` (não commitar dados sensíveis):

| Arquivo sugerido | Conteúdo | Usar em |
|------------------|----------|---------|
| `cost-explorer-by-service.png` | Cost Explorer → Cost by Service | 4.4 |
| `aws-billing-monthly.png` | Billing → Bills → Total (valores borrados se necessário) | 4.4 |
| `aws-budget-alert.png` | Budgets → budget com threshold 80%/100% | 4.3 ou 4.4 |

## Checklist AWS (antes de gravar 4.3–4.4)

- [ ] Decidi o modo: **A** (sem AWS), **B** (screenshots) ou **C** (conta com EKS)
- [ ] Screenshots preparados *(Modo A/B)* — ou usar apenas slides
- [ ] Console AWS **fora** da gravação do hands-on 4.5
- [ ] Conta ID, nomes de conta e valores reais **borrados** se usar screenshot
- [ ] OpenCost testado em `localhost:9003` *(4.5)*

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
- **AWS Billing/Budgets:** não abrir console — mencione que alertas de fatura (AWS Budgets) **complementam** alertas técnicos no Grafana. Ver `docs/aws-billing-gravacao.md`.

**Comandos:**

```bash
# Terminal B (opcional):
kubectl port-forward -n monitoring svc/monitoring-kube-prometheus-prometheus 9090:9090
# http://localhost:9090
```

**Antes de colar o prompt:**
Slides + menção Prometheus/Grafana. Gráficos de slide como exemplo conceitual.

**AWS (conceitual):** alertas no Grafana/Prometheus são a demo; mencione que em produção **AWS Budgets** alertam sobre a fatura antes da surpresa. Não abrir console AWS. Ver `docs/aws-billing-gravacao.md`.

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

**Dashboard:** `grafana/dashboards/finops-ai-rightsizing.json` *(vídeo 2.5)* | **Port-forwards:** Grafana (vídeo 2.5)

### Vídeo 2.1 — O impacto do over-provisioning em ambientes modernos

| Campo | Valor |
|-------|-------|
| Tipo | **T** |
| Tempo | 8–10 min |
| Dashboard | — |
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
| Tipo | **T** |
| Tempo | 10–12 min |
| Dashboard | — |
| Prompt | `ai-prompts/aula-02/2.2-rightsizing-payments-api.md` |

**Objetivo:** Explicar como comparar requests vs uso real para identificar oportunidades de rightsizing.

**Slides:**
- Slide 4: Rightsizing baseado em comportamento real
- Slide 5: Margem de segurança operacional
- Slide 6: Usage vs Requests (conceito)

**O que mostrar:**
- Slides 4–6.
- Explicar gap request vs uso com `payments-api` (dados do prompt).
- Gráficos do slide = exemplo conceitual; demo no Grafana fica para o vídeo 2.5.
- Sem terminal.

**Comandos:** Nenhum.

**Antes de colar o prompt:**
Sem demo. Slides 4–6. Citar `payments-api` com os dados do prompt (gap request vs uso). Demo no Grafana fica para o vídeo 2.5.

**Prompt IA — copiar e colar:**

```
Estou gravando o vídeo 2.2 (slides 4–6: rightsizing por comportamento real, margem de segurança, Usage vs Requests).

Contexto do lab: deployment payments-api (namespace payments), serviço crítico, overprovisionado.

Dados de referência (7 dias, por pod, 2 réplicas):
- Requests: CPU 1000m, Memória 1 Gi | Limits: CPU 1500m, Memória 2 Gi
- Uso: CPU média 72m, P95 95m, pico 120m | Memória média 88 Mi, P95 110 Mi, pico 125 Mi

Responda em português do Brasil para complementar os slides (ainda sem executar mudanças):
1. Explique o gap entre requests e uso real — CPU e memória — para um Platform Engineer.
2. Por que usar P95 (e não só a média) como base para rightsizing?
3. O que é margem de segurança operacional (~30% acima do P95) e por que não eliminar o gap de uma vez?
4. Diferença prática entre Usage vs Requests no Kubernetes (scheduling, custo alocável, throttling).
5. Este workload é candidato a rightsizing? Justifique em 3 bullet points.
```

\newpage

### Vídeo 2.3 — Ajustando recursos com automação operacional

| Campo | Valor |
|-------|-------|
| Tipo | **T** |
| Tempo | 10–12 min |
| Dashboard | — |
| Prompt | `ai-prompts/aula-02/2.3-automacao-vpa.md` |

**Objetivo:** Apresentar VPA e recomendações automatizadas.

**Slides:**
- Slide 7: VPA e recomendações automatizadas

**O que mostrar:**
- Slide 7.
- Conceitual — quando usar VPA vs recomendações assistidas por IA.
- Demo com dashboard e `collect-lab-context.sh` fica para o vídeo 2.5.
- Sem terminal.

**Comandos:** Nenhum.

**Antes de colar o prompt:**
Sem demo. Slide 7 — VPA e recomendações automatizadas. Demo com terminal e dashboard fica para o vídeo 2.5.

**Prompt IA — copiar e colar:**

```
Estou gravando o vídeo 2.3 (slide 7 — VPA e recomendações automatizadas) no FinOps AI Lab.

Workloads: payments-api (crítico, overprovisionado), users-api (saudável), staging-api (subutilizado).
Requests definidos manualmente no YAML; métricas reais via Prometheus.

Responda em português do Brasil:
1. O que o VPA (Vertical Pod Autoscaler) faz e quais modos existem (Off, Initial, Recreation, Auto)?
2. Quando VPA é adequado vs. recomendações manuais assistidas por IA?
3. Para payments-api (crítico): recomendaria VPA em produção? Por quê?
4. Para users-api e staging-api: mesma abordagem ou diferente?
5. Três riscos de ativar VPA sem guardrails em serviço de pagamentos.
```

\newpage

### Vídeo 2.4 — Scheduling inteligente e otimização de workloads

| Campo | Valor |
|-------|-------|
| Tipo | **T** |
| Tempo | 10–12 min |
| Dashboard | — |
| Prompt | `ai-prompts/aula-02/2.4-rollout-hpa-vpa.md` *(opcional)* |

**Objetivo:** Apresentar HPA, VPA e rollout gradual.

**Slides:**
- Slide 8: HPA, VPA e rollout gradual

**O que mostrar:**
- Slide 8.
- Conceitual — rollout gradual em serviço crítico (`payments-api`).
- Sem terminal.

**Comandos:** Nenhum.

**Antes de colar o prompt:**
Opcional. Slide 8 — rollout gradual no `payments-api`. Sem demo.

**Prompt IA — copiar e colar:**

```
Estou gravando o vídeo 2.4 (slide 8 — HPA, VPA e rollout gradual).

Contexto: ajuste proposto no payments-api (crítico, 2 réplicas) — reduzir CPU request de 1000m para ~125m e memória de 1 Gi para ~150 Mi, com margem sobre P95 observado.

Responda em português do Brasil:
1. Diferença entre HPA (escala horizontal) e VPA (escala vertical) — quando cada um entra no rightsizing?
2. Por que rightsizing em serviço crítico exige rollout gradual (não big bang)?
3. Plano de rollout em 4 passos para payments-api (ordem, réplicas, monitoração, rollback).
4. Métricas e alertas para monitorar nas primeiras 48h após o ajuste.
5. Em que cenário o HPA entraria depois do rightsizing — ou competiria com o VPA?
```

\newpage

### Vídeo 2.5 — Rightsizing — hands-on (payments + comparativo)

| Campo | Valor |
|-------|-------|
| Tipo | **H** |
| Tempo | 12–15 min |
| Dashboard | `grafana/dashboards/finops-ai-rightsizing.json` |
| Prompt | `ai-prompts/aula-02/2.5-rightsizing-hands-on.md` |

**Objetivo:** Executar pipeline completo: métricas → análise → recomendação IA → plano de ação.

**Slides:**
- Slide 9: Automação operacional de rightsizing
- Slide 10: Scheduling inteligente

**O que mostrar:**
- Slides 9–10.
- Grafana → `finops-ai-rightsizing.json` → **Last 15 minutes**.
- Citar `staging-api` como workload subutilizado (slide 10).
- Colar saída de `./scripts/collect-lab-context.sh` nos prompts A, B e C.

**Comandos:**

```bash
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
./scripts/collect-lab-context.sh
```

**Antes de colar o prompt:**
Hands-on. Slides 9–10. Rode `./scripts/collect-lab-context.sh` e cole a saída no bloco abaixo. Percorra o Grafana (`finops-ai-rightsizing.json`, Last 15 minutes) antes dos prompts A, B e C.

**Prompt IA — copiar e colar:**

```
## Contexto ao vivo

[COLE AQUI A SAÍDA DE ./scripts/collect-lab-context.sh]

Observações do Grafana (finops-ai-rightsizing.json, Last 15 minutes):
- payments: CPU Waste % alto
- users: waste moderado/baixo
- staging: subutilizado, waste alto
- Painéis: CPU/Memory Usage vs Requests, Top Overprovisioned, Rightsizing Candidates

---

## Prompt A — Rightsizing do payments-api (dados ao vivo)

Você é um SRE. Com base no contexto coletado acima e no dashboard Grafana, analise payments-api e sugira novos requests/limits.

Restrições:
- Margem ~30% acima do P95 para requests
- Limits absorvem picos sem OOMKill ou throttling agressivo
- Serviço crítico — rollout gradual

Responda em português do Brasil:
1. Requests e limits sugeridos (CPU e memória) com justificativa baseada nos dados ao vivo.
2. Risco (baixo/médio/alto) e mitigação.
3. Capacidade liberada no cluster (CPU e memória agregadas, 2 réplicas).
4. Plano de rollout (48h, critério de rollback).
5. Economia relativa estimada (% vs requests atuais).

---

## Prompt B — Comparativo e scheduling inteligente (slide 10)

Compare rightsizing entre payments-api, users-api e staging-api usando os dados do contexto acima.

Premissa: custo alocável ≈ soma dos requests × preço unitário do cluster.

Responda em português do Brasil:
1. Ranking de oportunidade de economia (1º ao 3º) com % estimado.
2. Requests/limits recomendados por workload.
3. Primeira sprint vs. depois — o que muda e por quê.
4. users-api: alterar ou manter como baseline?
5. staging-api: rightsizing, scale-to-zero ou desligamento noturno (scheduling inteligente)?

---

## Prompt C — Pipeline de automação operacional (slide 9)

Com base nas recomendações dos prompts A e B, desenhe um fluxo de rightsizing com IA no FinOps AI Lab.

Responda em português do Brasil:
1. Fluxo: métrica → IA analisa → humano aprova → PR no GitOps (passo a passo).
2. Guardrails para payments-api (aprovação obrigatória, teto de redução, etc.).
3. O que automatizar vs. o que manter manual neste lab.
4. Checklist de validação antes de merge do PR de rightsizing.
```

\newpage

## Aula 3 — Anomalias de custo e capacity planning operacional

**Dashboard:** `grafana/dashboards/finops-ai-anomalies.json` *(vídeo 3.5)* | **Port-forwards:** Grafana (vídeo 3.5)

### Vídeo 3.1 — Fundamentos de anomalias operacionais

| Campo | Valor |
|-------|-------|
| Tipo | **T** |
| Tempo | 8–10 min |
| Dashboard | — |
| Prompt | `ai-prompts/aula-03/3.1-deteccao-anomalia-cpu.md` |

**Objetivo:** Explicar o que é anomalia operacional e a diferença entre anomalia e incidente.

**Slides:**
- Slide 1: Anomalias de Custo e Capacity Planning Operacional
- Slide 2: O que é uma Anomalia Operacional?
- Slide 3: Incidente vs. Anomalia: Entendendo a Diferença

**O que mostrar:**
- Slides 1–3.
- Conceitual — baseline, desvio e detecção.
- Citar `cpu-spike` como exemplo do lab.
- Demo no Grafana e terminal fica para o vídeo 3.5.
- Sem terminal.

**Comandos:** Nenhum.

**Antes de colar o prompt:**
Sem demo. Slides 1–3. Citar `cpu-spike` como exemplo do lab. Demo no Grafana e terminal fica para o vídeo 3.5.

**Prompt IA — copiar e colar:**

```
Estou gravando o vídeo 3.1 (slides 1–3: o que é anomalia operacional, incidente vs. anomalia) no FinOps AI Lab.

Contexto: cluster Minikube com namespaces payments, users e staging. O workload cpu-spike simula anomalia de CPU no namespace payments.

Responda em português do Brasil:
1. Definição de anomalia operacional em FinOps/Kubernetes (CPU, memória, custo).
2. Diferença prática entre anomalia e incidente — com exemplos do lab.
3. O que é baseline e como detectar desvio estatisticamente significativo.
4. Por que nem toda anomalia vira incidente — e por que toda anomalia de custo merece investigação.
5. Uma pergunta provocativa para a audiência antes do hands-on (vídeo 3.5).
```

\newpage

### Vídeo 3.2 — Detecção, investigação e correlação de anomalias

| Campo | Valor |
|-------|-------|
| Tipo | **T** |
| Tempo | 10–12 min |
| Dashboard | — |
| Prompt | `ai-prompts/aula-03/3.2-investigacao-anomalia-cpu.md` |

**Objetivo:** Apresentar detecção com Prometheus/Grafana, investigação de spikes e correlação com mudanças.

**Slides:**
- Slide 4: Detectando Comportamento Anormal com Prometheus e Grafana
- Slide 5: Investigando a Origem de Spikes de Consumo
- Slide 6: Correlação entre Mudanças e Consumo

**O que mostrar:**
- Slides 4–6.
- Explicar fluxo detectar → correlacionar → isolar causa com dados do prompt.
- Gráficos do slide = exemplo conceitual; demo ao vivo fica para o vídeo 3.5.
- Sem terminal.

**Comandos:** Nenhum.

**Antes de colar o prompt:**
Sem demo. Slides 4–6. Use os dados de exemplo abaixo. Demo ao vivo fica para o vídeo 3.5.

**Prompt IA — copiar e colar:**

```
Estou gravando o vídeo 3.2 (slides 4–6: detecção, investigação de spikes, correlação com mudanças).

Timeline ilustrativa (UTC):
- 14:00 — CPU payments: ~140 mCPU total (baseline)
- 14:05 — deploy manual do workload cpu-spike (1 réplica)
- 14:06 — CPU payments: ~2100 mCPU total (+1400% vs. baseline)
- 14:06 — payments-api estável em ~145 mCPU (2 pods)

Workloads no namespace payments:
- payments-api: 2 réplicas, requests 1000m CPU
- cpu-spike: 1 réplica, stress --cpu 2, requests 500m, limits 2000m

Responda em português do Brasil:
1. Queries PromQL ou painéis Grafana para detectar este spike (conceitual).
2. Fluxo de investigação em ordem: detectar → correlacionar → isolar causa.
3. Como correlacionar deploys/mudanças com variação de consumo.
4. A anomalia é carga legítima ou misconfiguration/teste esquecido?
5. Checklist de triagem em 10 minutos (kubectl, métricas, change calendar).
```

\newpage

### Vídeo 3.3 — Capacity planning baseado em histórico

| Campo | Valor |
|-------|-------|
| Tipo | **T** |
| Tempo | 10–12 min |
| Dashboard | — |
| Prompt | `ai-prompts/aula-03/3.3-capacity-planning.md` |

**Objetivo:** Apresentar capacity planning com headroom, projeções e planejamento pós-incidente.

**Slides:**
- Slide 7: Capacity Planning Baseado em Histórico

**O que mostrar:**
- Slide 7.
- Conceitual — headroom, allocatable e projeções.
- Painel Capacity Headroom no Grafana fica para o vídeo 3.5.
- Sem terminal.

**Comandos:** Nenhum.

**Antes de colar o prompt:**
Sem demo. Slide 7 — Capacity Planning Baseado em Histórico. Painel Capacity Headroom no Grafana fica para o vídeo 3.5.

**Prompt IA — copiar e colar:**

```
Estou gravando o vídeo 3.3 (slide 7 — Capacity Planning Baseado em Histórico).

Após incidente com cpu-spike no namespace payments, projete capacidade do cluster para os próximos 90 dias.

Estado atual (Minikube, 4 CPU / 8 Gi RAM):
- Alocação por requests: payments ~2200m, users ~200m, staging ~500m, sistema ~800m
- Uso real médio: payments ~200m, users ~100m, staging ~30m
- Crescimento esperado: users-api +30% tráfego em 90 dias; payments estável

Responda em português do Brasil:
1. O cluster tem headroom suficiente hoje? Quantifique CPU e memória.
2. Em que cenário um novo spike derruba scheduling (Pending pods)?
3. Projeção de uso em 90 dias (tabela por namespace).
4. Recomendações: expandir cluster, quotas, limitRange, PriorityClass?
5. Quando escalar node pool vs. rightsizing primeiro?
```

\newpage

### Vídeo 3.4 — Uso de IA para investigação e projeções

| Campo | Valor |
|-------|-------|
| Tipo | **T** |
| Tempo | 10–12 min |
| Dashboard | — |
| Prompt | `ai-prompts/aula-03/3.4-anomalia-silenciosa-staging.md` |

**Objetivo:** Mostrar como a IA acelera investigação de anomalias e projeções de capacidade/custo.

**Slides:**
- Slide 8: Uso de IA para Investigação e Projeções

**O que mostrar:**
- Slide 8.
- Conceitual — IA como copiloto na investigação e projeções.
- Demo com `collect-anomaly-context.sh` fica para o vídeo 3.5.
- Sem terminal.

**Comandos:** Nenhum.

**Antes de colar o prompt:**
Sem demo. Slide 8 — Uso de IA para Investigação e Projeções. Demo com `collect-anomaly-context.sh` fica para o vídeo 3.5.

**Prompt IA — copiar e colar:**

```
Estou gravando o vídeo 3.4 (slide 8 — Uso de IA para Investigação e Projeções) no FinOps AI Lab.

Contexto: após detectar anomalias de CPU (cpu-spike) e de custo silencioso (CronJob backup-sync em staging), quero usar IA como copiloto.

Responda em português do Brasil:
1. Como a IA acelera investigação de anomalias vs. análise manual (3 casos de uso concretos).
2. Que dados colar no prompt para a IA ser útil (métricas, timeline, kubectl output)?
3. Como a IA ajuda em projeções de capacidade e custo — limites e cuidados.
4. Riscos de confiar cegamente na IA em incidentes operacionais.
5. Template de prompt reutilizável para investigação de anomalia (5 linhas).
```

\newpage

### Vídeo 3.5 — Hands-on — anomalias e capacity planning operacional

| Campo | Valor |
|-------|-------|
| Tipo | **H** |
| Tempo | 12–15 min |
| Dashboard | `grafana/dashboards/finops-ai-anomalies.json` |
| Prompt | `ai-prompts/aula-03/3.5-runbook-anomalias.md` |

**Objetivo:** Fluxo completo: baseline → spike → investigação → staging → capacity → runbook com IA.

**Slides:**
- Slide 9: Exemplo Prático: Workload cpu-spike
- Slide 10: Boas Práticas e Preparação para o Hands-on

**O que mostrar:**
- Slides 9–10.
- Grafana → `finops-ai-anomalies.json` → **Last 15 minutes**.
- Fluxo: baseline → `start-anomaly.sh` → Top CPU Consumers → `start-staging-anomaly.sh` → Capacity Headroom.
- Colar `./scripts/collect-anomaly-context.sh` nos prompts A, B e C.
- `stop-all-anomalies.sh` → confirmar retorno ao baseline.

**Comandos:**

```bash
./scripts/stop-all-anomalies.sh
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
./scripts/start-business-hours-load.sh
sleep 120
./scripts/start-anomaly.sh
kubectl get pods -n payments
kubectl top pods -n payments
./scripts/start-staging-anomaly.sh
kubectl get jobs -n staging -l app=backup-sync
./scripts/collect-anomaly-context.sh
./scripts/stop-all-anomalies.sh
```

**Antes de colar o prompt:**
Hands-on. Slides 9–10. Rode `./scripts/collect-anomaly-context.sh` e cole a saída no bloco abaixo. Percorra o Grafana (`finops-ai-anomalies.json`, Last 15 minutes) antes dos prompts A, B e C.

**Prompt IA — copiar e colar:**

```
## Contexto ao vivo

[COLE AQUI A SAÍDA DE ./scripts/collect-anomaly-context.sh]

Observações do Grafana (finops-ai-anomalies.json, Last 15 minutes):
- Baseline com business-hours-load (sem cpu-spike)
- Spike em payments após start-anomaly.sh — CPU Spike Detector
- Jobs backup-sync em staging (anomalia silenciosa de custo)
- Painel Capacity Headroom após incidentes

---

## Prompt A — Investigação do cpu-spike (slide 9)

Você é um SRE. Com base no contexto coletado acima e no dashboard Grafana, investigue o spike de CPU no namespace payments.

Responda em português do Brasil:
1. A anomalia é legítima ou misconfiguration/teste esquecido?
2. Passos de triagem em ordem (kubectl, métricas, logs).
3. Impacto no cluster Minikube (4 CPUs): risco de contenção?
4. Ação imediata e ação preventiva (alerta, quota, policy).
5. Postmortem leve (template 5 linhas).

---

## Prompt B — Anomalia silenciosa em staging

O namespace staging teve aumento de custo alocado sem spike visível no staging-api.

Dados do contexto acima + observação: CronJob backup-sync com rajadas de CPU.

Responda em português do Brasil:
1. Por que é "anomalia de custo" e não incidente de disponibilidade?
2. Como correlacionar CronJobs/Jobs com custo no OpenCost/Prometheus?
3. Rightsizing do staging-api ou o problema é o CronJob?
4. Políticas de governança que evitariam CronJobs órfãos.
5. Mensagem colaborativa para o time platform.

---

## Prompt C — Runbook e capacity planning (slide 10)

Com base nos prompts A e B, crie um runbook operacional para anomalias de custo/consumo no FinOps AI Lab.

Responda em português do Brasil, formato runbook SRE on-call:
1. Sintomas (alerta ou dashboard).
2. Diagnóstico em 10 minutos (comandos kubectl e queries PromQL).
3. Mitigação imediata (scale down, delete pod, isolate namespace).
4. Comunicação (payments, platform, FinOps).
5. Encerramento e follow-up.
6. Seção "Quando NÃO agir" — falsos positivos comuns.
```

\newpage

## Aula 4 — Governança operacional e visibilidade de custos

**Dashboard:** `grafana/dashboards/finops-ai-governance.json` *(vídeo 4.5)* | **Port-forwards:** Grafana + OpenCost (vídeo 4.5)

### Vídeo 4.1 — Por que governança de custos em Kubernetes

| Campo | Valor |
|-------|-------|
| Tipo | **T** |
| Tempo | 8–10 min |
| Dashboard | — |
| Prompt | `ai-prompts/aula-04/4.1-auditoria-labels.md` |

**Objetivo:** Explicar por que observabilidade sozinha não basta e o desafio de atribuição de custos.

**Slides:**
- Slide 1: Governança Operacional e Visibilidade de Custos
- Slide 2: Por Que Observabilidade Sozinha Não É Suficiente?
- Slide 3: O Desafio da Atribuição de Custos em Kubernetes

**O que mostrar:**
- Slides 1–3.
- Conceitual — accountability e visibilidade de custos.
- Demo com labels e OpenCost fica para o vídeo 4.5.
- Sem terminal.

**Comandos:** Nenhum.

**Antes de colar o prompt:**
Sem demo. Slides 1–3. Demo com labels e OpenCost fica para o vídeo 4.5.

**Prompt IA — copiar e colar:**

```
Estou gravando o vídeo 4.1 (slides 1–3: governança, limites da observabilidade, atribuição de custos).

Contexto: cluster Kubernetes compartilhado (payments, users, staging) com Prometheus, Grafana e OpenCost.

Responda em português do Brasil:
1. Por que observabilidade sozinha não responde "quanto custa cada time/workload"?
2. Três desafios de atribuição de custo em clusters Kubernetes compartilhados.
3. Diferença entre visibilidade técnica e accountability financeira.
4. O que muda na operação quando existe governança de custos estruturada.
5. Pergunta provocativa para engajar a audiência antes do hands-on (vídeo 4.5).
```

\newpage

### Vídeo 4.2 — Labels, ownership e OpenCost na prática

| Campo | Valor |
|-------|-------|
| Tipo | **T** |
| Tempo | 10–12 min |
| Dashboard | — |
| Prompt | `ai-prompts/aula-04/4.2-politica-ambientes.md` |

**Objetivo:** Apresentar labels como fundação, modelos de custeio e alocação com OpenCost.

**Slides:**
- Slide 4: Labels como Fundação da Governança
- Slide 5: Ownership, Accountability e Modelos de Custeio
- Slide 6: OpenCost na Prática

**O que mostrar:**
- Slides 4–6.
- Conceitual — showback vs chargeback e alocação por namespace.
- Gráficos do slide = exemplo conceitual; demo no Grafana/OpenCost fica para o vídeo 4.5.
- Sem terminal.

**Comandos:** Nenhum.

**Antes de colar o prompt:**
Sem demo. Slides 4–6. Use a tabela de labels abaixo. Demo no Grafana/OpenCost fica para o vídeo 4.5.

**Prompt IA — copiar e colar:**

```
Estou gravando o vídeo 4.2 (slides 4–6: labels, ownership, OpenCost).

Labels atuais dos namespaces:

| Namespace | team     | environment | cost-center  |
|-----------|----------|-------------|--------------|
| payments  | payments | prod        | product      |
| users     | users    | prod        | product      |
| staging   | platform | staging     | engineering  |

Responda em português do Brasil:
1. Score de maturidade de labeling (0–10) e gaps críticos.
2. Labels adicionais recomendados para FinOps (nome, exemplo, obrigatoriedade).
3. Showback vs. chargeback neste cenário — qual fase e por quê?
4. Como o OpenCost traduz métricas de consumo em custo por namespace/workload.
5. Plano de 30 dias para corrigir governança sem bloquear deploys.
```

\newpage

### Vídeo 4.3 — Visibilidade para diferentes personas

| Campo | Valor |
|-------|-------|
| Tipo | **T** |
| Tempo | 10–12 min |
| Dashboard | — |
| Prompt | `ai-prompts/aula-04/4.3-showback-chargeback.md` |

**Objetivo:** Mostrar como entregar a informação certa para SRE, FinOps e Engineering Manager.

**Slides:**
- Slide 7: Visibilidade para Diferentes Personas

**O que mostrar:**
- Slide 7.
- Conceitual — dashboards e rituais por persona.
- FinOps persona: budget vs actual — cite **AWS Budgets** e alertas de billing como exemplo **em produção** (sem abrir console).
- Demo no Grafana fica para o vídeo 4.5.
- Sem terminal. Ver `docs/aws-billing-gravacao.md`.

**Comandos:** Nenhum.

**Antes de colar o prompt:**
Sem demo. Slide 7 — Visibilidade para Diferentes Personas. Demo no Grafana fica para o vídeo 4.5.

**AWS (conceitual):** persona FinOps usa budget vs actual — cite **AWS Budgets** e alertas de billing como exemplo em produção. **Não abra** console AWS. Ver `docs/aws-billing-gravacao.md`.

**Prompt IA — copiar e colar:**

```
Estou gravando o vídeo 4.3 (slide 7 — Visibilidade para Diferentes Personas).

Personas:
- SRE on-call: desperdício e risco de saturação
- FinOps analyst: alocação por time e cost-center
- Engineering Manager: priorizar backlog de eficiência

Dados disponíveis no lab: Prometheus, Grafana (finops-ai-governance.json), OpenCost, labels nos namespaces.

Responda em português do Brasil:
1. Um dashboard ou view por persona (métricas, filtros, frequência).
2. Perguntas que cada persona responde em menos de 2 minutos.
3. Como o EM do time payments interpreta ser ~62% do custo alocado.
4. Rituais: daily (SRE), weekly (FinOps), monthly (EM + platform).
5. Erros comuns ao expor custo para engenharia.
```

\newpage

### Vídeo 4.4 — AWS Cost Explorer e OpenCost — visões complementares

| Campo | Valor |
|-------|-------|
| Tipo | **T** |
| Tempo | 10–12 min |
| Dashboard | — |
| Prompt | `ai-prompts/aula-04/4.4-guardrails.md` |

**Objetivo:** Explicar como Cost Explorer e OpenCost se complementam na visão de custo.

**Slides:**
- Slide 8: AWS Cost Explorer + OpenCost: Visões Complementares

**O que mostrar:**
- Slide 8.
- **Lab local (Minikube) — não precisa de EKS nem conta AWS.**
- Conceitual — infra cloud (Cost Explorer/Billing) vs camada Kubernetes (OpenCost).
- **Modo recomendado:** slides + script de 30 s (`docs/aws-billing-gravacao.md`).
- **Opcional:** screenshot Cost Explorer, Billing ou AWS Budgets — sem demo ao vivo obrigatória.
- Mencionar alertas de billing (Budgets) vs alertas técnicos (Grafana).
- Demo OpenCost ao vivo fica para o vídeo 4.5.
- Sem terminal.

**Comandos:** Nenhum.

**Antes de colar o prompt:**
Sem demo de terminal. Slide 8 — Cost Explorer, Billing e Budgets **complementam** OpenCost.

**Lab local:** Minikube — **não precisa** de EKS nem abrir AWS ao vivo. Três opções:

| Modo | O que fazer |
|------|-------------|
| **A (recomendado)** | Slides + painel *OpenCost + AWS Cost Explorer* no Grafana + script de 30 s no doc AWS |
| **B** | Screenshot Cost Explorer / Billing / Budgets (valores borrados) |
| **C** | Console AWS ao vivo *(só se tiver conta; EKS opcional)* |

Mencione **alertas de billing** (AWS Budgets) vs **alertas técnicos** (Grafana). Demo OpenCost ao vivo fica para o **vídeo 4.5**.

**Prompt IA — copiar e colar:**

```
Estou gravando o vídeo 4.4 (slide 8 — AWS Cost Explorer + OpenCost: Visões Complementares).

Contexto de gravação:
- Lab local Minikube — NÃO tenho EKS nem cluster Kubernetes na AWS
- OpenCost no lab usa preços públicos AWS como estimativa (não é fatura real)
- Cost Explorer/Billing/Budgets serão explicados como camada cloud em produção

Responda em português do Brasil:
1. O que cada ferramenta responde que a outra não responde (Cost Explorer, Billing, Budgets, OpenCost).
2. Como cruzar fatura AWS com alocação por namespace no OpenCost — mesmo sem EKS na conta.
3. Cenário didático: custo AWS subiu 10% — onde investigar primeiro (Billing → Cost Explorer → OpenCost)?
4. Diferença entre alerta de billing (AWS Budgets) e alerta técnico (Grafana/Prometheus).
5. Script de 1 minuto para gravar explicando as visões complementares — lab Minikube, sem demo AWS obrigatória.
```

\newpage

### Vídeo 4.5 — Hands-on — governança e visibilidade de custos

| Campo | Valor |
|-------|-------|
| Tipo | **H** |
| Tempo | 12–15 min |
| Dashboard | `grafana/dashboards/finops-ai-governance.json` |
| Prompt | `ai-prompts/aula-04/4.5-visibilidade-persona.md` |

**Objetivo:** Demonstrar labels, governança, showback, guardrails e OpenCost com dados ao vivo.

**Slides:**
- Slide 9: Guardrails Operacionais: Governança sem Burocracia
- Slide 10: Laboratório Prático: payments, users e staging

**O que mostrar:**
- Slides 9–10 (intro ~2 min), depois lab.
- **Não abrir AWS console** (Cost Explorer/Billing) neste vídeo — use OpenCost + Grafana.
- **Terminal A** — port-forwards Grafana (3000) e OpenCost (9003).
- **Terminal B** — demo:
-   1. `kubectl get ns --show-labels` — comparar com Governance Matrix
-   2. `kubectl get resourcequota -A` e `kubectl get limitrange -A` — gaps do Guardrails Checklist
-   3. `./scripts/collect-lab-context.sh` — contexto para IA
- **Grafana** → `finops-ai-governance.json` → **Last 15 minutes**:
-   - Resource Overview: CPU/Memory Usage e Requests by Namespace
-   - Governance & Labels: Namespace Label Coverage + Governance Matrix
-   - Cost Visibility: Showback View by Namespace + Showback — Nota didática
-   - Guardrails & Tooling: Guardrails Checklist + painel *OpenCost + AWS Cost Explorer* (referência, não substitui demo)
- **OpenCost** → http://localhost:9003 — alocação por namespace (payments > users > staging)
- Colar `./scripts/collect-lab-context.sh` nos prompts A (slides 4–6), B (slide 7), C (slide 9).
- Comentar resposta da IA criticamente.

**Comandos:**

```bash
./scripts/stop-all-anomalies.sh
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
kubectl port-forward -n opencost svc/opencost 9003:9090
kubectl get ns --show-labels
kubectl get resourcequota -A
kubectl get limitrange -A
./scripts/warmup-lab-metrics.sh
./scripts/collect-lab-context.sh
# Grafana: http://localhost:3000 → FinOps AI - Governance and Cost Visibility
# OpenCost: http://localhost:9003
# AWS Cost Explorer/Billing: NÃO usar ao vivo — ver docs/aws-billing-gravacao.md
```

**Antes de colar o prompt:**
Hands-on. Slides 9–10. Setup: `./scripts/stop-all-anomalies.sh`, port-forwards Grafana (3000) e OpenCost (9003), `./scripts/warmup-lab-metrics.sh`.

**Não abrir AWS** (Cost Explorer/Billing/Budgets) neste vídeo — demo = OpenCost + Grafana. Painel comparativo no dashboard é referência visual. Ver `docs/aws-billing-gravacao.md`.

Percorra **antes** de colar os prompts:

| Ordem | Onde | O quê |
|-------|------|-------|
| 1 | Terminal | `kubectl get ns --show-labels` → Governance Matrix |
| 2 | Terminal | `kubectl get resourcequota -A` + `kubectl get limitrange -A` → Guardrails Checklist |
| 3 | Grafana `finops-ai-governance.json` (Last 15 min) | Resource Overview → Governance & Labels → Cost Visibility → Guardrails & Tooling |
| 4 | OpenCost http://localhost:9003 | Alocação por namespace/workload |
| 5 | Terminal | `./scripts/collect-lab-context.sh` → colar abaixo |

Rode `./scripts/collect-lab-context.sh` e cole a saída no bloco abaixo antes dos prompts A, B e C.

**Prompt IA — copiar e colar:**

```
## Contexto ao vivo

[COLE AQUI A SAÍDA DE ./scripts/collect-lab-context.sh]

Observações do Grafana (finops-ai-governance.json, Last 15 minutes):
- Governance Matrix — labels por namespace
- Showback View — custo alocado por cost-center
- Guardrails Checklist — gaps de governança

OpenCost (http://localhost:9003): alocação por namespace/workload.

---

## Prompt A — Auditoria de labels e ownership (slides 4–6)

Com base no contexto coletado, avalie a governança de labels e ownership.

Responda em português do Brasil:
1. Score de maturidade (0–10) com gaps críticos nos dados reais.
2. Labels adicionais recomendados (owner, service-tier).
3. Impacto de labels ausentes no OpenCost e showback.
4. Como mapear ownership quando team=platform em staging.
5. Top 3 correções prioritárias.

---

## Prompt B — Showback e visibilidade por persona (slide 7)

Use os dados do OpenCost e Grafana para explicar showback aos times.

Responda em português do Brasil:
1. Alocação estimada por namespace/cost-center com os dados ao vivo.
2. Showback ou chargeback neste estágio — justificativa.
3. View recomendada para SRE, FinOps e EM (1 parágrafo cada).
4. Como apresentar ao time payments sem parecer punição.
5. Métricas de eficiência por cost-center.

---

## Prompt C — Guardrails operacionais (slide 9)

Problemas observados no lab: cpu-spike sem label ephemeral, staging overprovisionado, sem ResourceQuota.

Responda em português do Brasil:
1. Top 5 guardrails priorizados (quota, limitRange, labels obrigatórios, etc.).
2. Para cada um: bloqueia, alerta ou recomenda — esforço de implementação.
3. ResourceQuota sugerida para staging vs. payments.
4. Política de labels obrigatórios no admission webhook.
5. KPIs para medir eficácia em 60 dias.
```

\newpage

## Aula 5 — Operações cloud orientadas por eficiência

**Dashboard:** `Todos os dashboards anteriores` *(vídeo 5.5)* | **Port-forwards:** Grafana + OpenCost (vídeo 5.5)

### Vídeo 5.1 — Revisão do curso e mentalidade de eficiência

| Campo | Valor |
|-------|-------|
| Tipo | **T** |
| Tempo | 8–10 min |
| Dashboard | — |
| Prompt | `ai-prompts/aula-05/5.1-diagnostico-consolidado.md` |

**Objetivo:** Revisar a jornada do curso e consolidar eficiência operacional como disciplina contínua.

**Slides:**
- Slide 1: Operações Cloud Orientadas por Eficiência
- Slide 2: O Que Aprendemos ao Longo do Curso
- Slide 3: Eficiência Operacional é uma Disciplina, Não um Projeto

**O que mostrar:**
- Slides 1–3.
- Conceitual — recapitular achados das aulas 1–4.
- Tour nos dashboards fica para o vídeo 5.5.
- Sem terminal.

**Comandos:** Nenhum.

**Antes de colar o prompt:**
Sem demo. Slides 1–3. Recapitular achados das aulas 1–4. Tour nos dashboards fica para o vídeo 5.5.

**Prompt IA — copiar e colar:**

```
Estou gravando o vídeo 5.1 (slides 1–3: revisão do curso e eficiência como disciplina).

Jornada do curso:
- Aula 1: observabilidade de consumo (payments over, users ok, staging sub)
- Aula 2: rightsizing e automação (VPA, scheduling)
- Aula 3: anomalias e capacity planning (cpu-spike, backup-sync)
- Aula 4: governança, labels, OpenCost, showback

Responda em português do Brasil:
1. Resumo da jornada em 8 bullets (1 por conceito-chave).
2. Três achados consolidados do FinOps AI Lab.
3. Por que eficiência operacional é disciplina contínua, não projeto pontual.
4. Armadilhas comuns ao tratar FinOps como iniciativa temporária.
5. Pergunta provocativa antes do hands-on final (vídeo 5.5).
```

\newpage

### Vídeo 5.2 — Ciclo da eficiência e IA na operação

| Campo | Valor |
|-------|-------|
| Tipo | **T** |
| Tempo | 10–12 min |
| Dashboard | — |
| Prompt | `ai-prompts/aula-05/5.2-priorizacao-matriz.md` |

**Objetivo:** Apresentar o ciclo de eficiência, o papel da IA e o fluxo orientado por dados.

**Slides:**
- Slide 4: O Ciclo da Eficiência
- Slide 5: O Papel da IA na Operação Moderna
- Slide 6: Fluxo Operacional Orientado por Dados

**O que mostrar:**
- Slides 4–6.
- Conceitual — observar → analisar → decidir → agir → medir.
- Sem lab.

**Comandos:** Nenhum.

**Antes de colar o prompt:**
Sem demo. Slides 4–6. Conceitual — ciclo, IA e fluxo orientado por dados.

**Prompt IA — copiar e colar:**

```
Estou gravando o vídeo 5.2 (slides 4–6: ciclo da eficiência, IA na operação, fluxo orientado por dados).

Stack: Minikube, Prometheus, Grafana, OpenCost, IA como copiloto.

Responda em português do Brasil:
1. Descreva o ciclo de eficiência em 5 etapas (observar → agir → medir).
2. Papel da IA como copiloto — o que amplifica vs. o que não substitui.
3. Fluxo operacional orientado por dados: Prometheus → Grafana → OpenCost → IA → ação.
4. Onde humanos devem manter aprovação obrigatória (ex.: rightsizing em payments).
5. Exemplo de decisão que atravessa todo o ciclo no FinOps AI Lab.
```

\newpage

### Vídeo 5.3 — Métricas que realmente importam

| Campo | Valor |
|-------|-------|
| Tipo | **T** |
| Tempo | 10–12 min |
| Dashboard | — |
| Prompt | `ai-prompts/aula-05/5.3-plano-90-dias.md` |

**Objetivo:** Identificar métricas que conectam performance, eficiência e custo.

**Slides:**
- Slide 7: Métricas que Realmente Importam

**O que mostrar:**
- Slide 7.
- Conceitual — KPIs operacionais e FinOps.
- OpenCost vs Cost Explorer — complementares; **sem abrir AWS** (ver `docs/aws-billing-gravacao.md`).
- Sem lab.

**Comandos:** Nenhum.

**Antes de colar o prompt:**
Sem demo. Slide 7 — Métricas que Realmente Importam.

OpenCost vs Cost Explorer — complementares. **Sem abrir AWS**; lab = Minikube + OpenCost. Ver `docs/aws-billing-gravacao.md`.

**Prompt IA — copiar e colar:**

```
Estou gravando o vídeo 5.3 (slide 7 — Métricas que Realmente Importam).

Contexto: operação Kubernetes com FinOps — payments (crítico, overprovisionado), users (saudável), staging (subutilizado).

Responda em português do Brasil:
1. As 5 métricas essenciais que conectam performance, eficiência e custo.
2. Para cada métrica: o que revela, fonte (Prometheus/OpenCost), exemplo de query.
3. Métricas que parecem importantes mas geram ruído — evite.
4. KPIs por persona: SRE, FinOps, Engineering Manager (1 KPI cada).
5. Dashboard mínimo viável para review semanal de eficiência.
```

\newpage

### Vídeo 5.4 — Roadmap de maturidade FinOps

| Campo | Valor |
|-------|-------|
| Tipo | **T** |
| Tempo | 10–12 min |
| Dashboard | — |
| Prompt | `ai-prompts/aula-05/5.4-recomendacoes-executivas.md` |

**Objetivo:** Apresentar evolução em estágios de maturidade FinOps na organização.

**Slides:**
- Slide 8: Roadmap de Maturidade FinOps

**O que mostrar:**
- Slide 8.
- Conceitual — estágios de maturidade e desbloqueios.
- Estágio Governança: budgets e alertas de billing — **conceitual** (AWS Budgets); lab usa OpenCost + Grafana.
- Sem lab.

**Comandos:** Nenhum.

**Antes de colar o prompt:**
Sem demo. Slide 8 — Roadmap de Maturidade FinOps.

Estágio Governança cita budgets — explique **AWS Budgets** como conceito; lab usa OpenCost. Ver `docs/aws-billing-gravacao.md`.

**Prompt IA — copiar e colar:**

```
Estou gravando o vídeo 5.4 (slide 8 — Roadmap de Maturidade FinOps).

Estado atual do FinOps AI Lab (síntese):
- Observabilidade: ok (Prometheus, Grafana, 4 dashboards)
- Rightsizing: oportunidade crítica em payments
- Anomalias: gap de alertas e runbooks
- Governança: labels básicos, faltam quotas e guardrails
- IA: usada pontualmente, sem playbook consolidado

Responda em português do Brasil:
1. Em qual estágio de maturidade FinOps este ambiente está (Crawl/Walk/Run ou similar)?
2. Quatro estágios de evolução com entregáveis e critérios de avanço.
3. O que desbloqueia cada estágio (pessoas, processos, ferramentas).
4. Riscos de pular estágios (ex.: chargeback antes de showback).
5. Próximo marco recomendado para o lab em 90 dias.
```

\newpage

### Vídeo 5.5 — Hands-on — copiloto de eficiência e plano 30-60-90

| Campo | Valor |
|-------|-------|
| Tipo | **H** |
| Tempo | 12–15 min |
| Dashboard | `Todos os dashboards anteriores` |
| Prompt | `ai-prompts/aula-05/5.5-copiloto-eficiencia.md` |

**Objetivo:** Executar fluxo end-to-end com IA: dashboards → diagnóstico → plano de ação.

**Slides:**
- Slide 9: O Copiloto de Eficiência: Prompts e Templates
- Slide 10: Plano de Ação 30-60-90 Dias

**O que mostrar:**
- Slides 9–10 (intro ~2 min), depois lab.
- **Não abrir AWS console** — plano 90 dias cita budgets/alertas como ação futura; demo = OpenCost + Grafana.
- **Terminal A** — port-forwards Grafana (3000) e OpenCost (9003).
- **Terminal B** — demo:
-   1. `./scripts/stop-all-anomalies.sh` + `./scripts/warmup-lab-metrics.sh`
-   2. `./scripts/collect-lab-context.sh` + `kubectl top pods -A`
- **Grafana** — tour **Last 15 minutes** (~1 min cada dashboard):
-   1. `finops-ai-lab.json` — CPU/Memory por namespace, Top Consumers
-   2. `finops-ai-rightsizing.json` — CPU Waste %, Top Overprovisioned, Rightsizing Candidates
-   3. `finops-ai-anomalies.json` — CPU Spike Detector, Capacity Headroom (baseline, sem spike)
-   4. `finops-ai-governance.json` — Showback View, Governance Matrix, Guardrails Checklist
- **OpenCost** → http://localhost:9003 — alocação consolidada por namespace
- Narrar achados: payments over, users ok, staging sub, anomalias = lição (Aula 3).
- Colar `./scripts/collect-lab-context.sh` + observações dos 4 dashboards no **prompt mestre**.
- Apresentar: diagnóstico, top 3 ações, plano 30-60-90, KPIs, template reutilizável.

**Comandos:**

```bash
./scripts/stop-all-anomalies.sh
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
kubectl port-forward -n opencost svc/opencost 9003:9090
./scripts/warmup-lab-metrics.sh
./scripts/collect-lab-context.sh
kubectl top pods -A
# Grafana: http://localhost:3000 → 4 dashboards (Last 15 minutes)
# OpenCost: http://localhost:9003
# AWS Cost Explorer/Billing: NÃO usar ao vivo — ver docs/aws-billing-gravacao.md
```

**Antes de colar o prompt:**
Hands-on final. Slides 9–10. Setup: `./scripts/stop-all-anomalies.sh`, port-forwards Grafana (3000) e OpenCost (9003), `./scripts/warmup-lab-metrics.sh`.

**Não abrir AWS** — plano 30-60-90 cita budgets/alertas como ação futura; demo = 4 dashboards Grafana + OpenCost. Ver `docs/aws-billing-gravacao.md`.

Percorra **antes** de colar o prompt mestre:

| Ordem | Onde | O quê |
|-------|------|-------|
| 1 | Grafana `finops-ai-lab.json` (Last 15 min) | Consumo por namespace, Top CPU/Memory Consumers |
| 2 | Grafana `finops-ai-rightsizing.json` | CPU Waste %, Top Overprovisioned, Rightsizing Candidates |
| 3 | Grafana `finops-ai-anomalies.json` | CPU Spike Detector, Capacity Headroom (baseline) |
| 4 | Grafana `finops-ai-governance.json` | Showback View, Governance Matrix, Guardrails Checklist |
| 5 | OpenCost http://localhost:9003 | Alocação consolidada por namespace |
| 6 | Terminal | `./scripts/collect-lab-context.sh` + `kubectl top pods -A` → colar em `[DADOS]` |

Narrar: payments overprovisionado, users ok, staging subutilizado, anomalias (Aula 3) como lição operacional.

**Prompt IA — copiar e colar:**

```
A partir de agora, atue como meu copiloto de eficiência operacional em Kubernetes e FinOps.

Regras:
- Respostas em português do Brasil, linguagem para SRE/DevOps/Platform
- Sempre separar: fato observado, hipótese, recomendação, risco
- Nunca sugerir mudança em produção sem plano de rollback
- Priorizar por impacto financeiro e segurança operacional

Meu ambiente:
- Cluster: Minikube (4 CPU, 8 Gi RAM)
- Observabilidade: Prometheus, Grafana (4 dashboards), OpenCost
- Namespaces: payments (payments-api), users (users-api), staging (staging-api)
- Labels: team, environment, cost-center

[DADOS — cole aqui a saída de ./scripts/collect-lab-context.sh + observações dos 4 dashboards Grafana e OpenCost]

Analise e devolva:

## 1. Diagnóstico consolidado (5 bullets)

## 2. Top 3 ações priorizadas (impacto × esforço)

## 3. Plano de Ação 30-60-90 Dias (slide 10)
- 30 dias: quick wins
- 60 dias: estruturação (alertas, quotas, rituais)
- 90 dias: automação e maturidade

## 4. KPIs para acompanhar (slide 7)

## 5. Template de prompt reutilizável (slide 9) — salve como playbook da equipe
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

- [ ] Dashboard rightsizing (`finops-ai-rightsizing.json`) importado e com dados *(vídeo 2.5)*
- [ ] Port-forward do Grafana ativo *(vídeo 2.5)*
- [ ] Painel CPU Waste Percentage mostra payments com waste alto *(vídeo 2.5)*
- [ ] `./scripts/collect-lab-context.sh` testado *(vídeo 2.5)*
- [ ] Seção da Aula 2 no manual revisada (vídeos 2.1–2.5)

### Aula 3 — Anomalias

- [ ] Dashboard anomalies (`finops-ai-anomalies.json`) importado e com dados *(vídeo 3.5)*
- [ ] Port-forward do Grafana ativo *(vídeo 3.5)*
- [ ] `./scripts/start-anomaly.sh` testado — spike visível no Grafana em ~30s *(vídeo 3.5)*
- [ ] `./scripts/start-staging-anomaly.sh` testado — job `backup-sync` criado imediatamente *(vídeo 3.5)*
- [ ] `./scripts/stop-all-anomalies.sh` testado — baseline restaurado *(vídeo 3.5)*
- [ ] `./scripts/collect-anomaly-context.sh` testado — saída utilizável nos prompts *(vídeo 3.5)*
- [ ] Seção da Aula 3 no manual revisada (vídeos 3.1–3.5)

### Aula 4 — Governança

- [ ] Dashboard governance (`finops-ai-governance.json`) importado e com dados *(vídeo 4.5)*
- [ ] Port-forwards Grafana + OpenCost ativos *(vídeo 4.5)*
- [ ] `kubectl get ns --show-labels` mostra labels team, environment, cost-center *(vídeo 4.5)*
- [ ] `./scripts/collect-lab-context.sh` testado *(vídeo 4.5)*
- [ ] Seção da Aula 4 no manual revisada (vídeos 4.1–4.5)
- [ ] Leu `docs/aws-billing-gravacao.md` — decidiu Modo A/B/C para vídeos 4.3–4.4
- [ ] Screenshots AWS preparados *(opcional, Modo B)* ou usa só slides *(Modo A)*
- [ ] Console AWS **fora** do hands-on 4.5

### Aula 5 — Eficiência operacional

- [ ] Todos os 4 dashboards acessíveis no Grafana *(vídeo 5.5)*
- [ ] Port-forwards Grafana + OpenCost ativos *(vídeo 5.5)*
- [ ] `./scripts/collect-lab-context.sh` testado *(vídeo 5.5 — prompt mestre)*
- [ ] Seção da Aula 5 no manual revisada (vídeos 5.1–5.5)
- [ ] Achados das aulas 1–4 anotados para o fluxo completo
- [ ] Console AWS **fora** do hands-on 5.5 (budgets/alertas = conceitual no plano 90 dias)

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