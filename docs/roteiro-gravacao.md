# FinOps com IA — Roteiro de Gravação

Roteiro detalhado dos **25 vídeos** do curso (5 aulas × 5 vídeos). Cada vídeo tem duração estimada de **8 a 15 minutos**.

## Referência rápida

| Aula | Dashboard | Prompt IA |
|------|-----------|-----------|
| 1 | `grafana/dashboards/finops-ai-lab.json` | `ai-prompts/aula-01-observabilidade.md` |
| 2 | `grafana/dashboards/finops-ai-rightsizing.json` | `ai-prompts/aula-02-rightsizing.md` |
| 3 | `grafana/dashboards/finops-ai-anomalies.json` | `ai-prompts/aula-03-anomalias.md` |
| 4 | `grafana/dashboards/finops-ai-governance.json` | `ai-prompts/aula-04-governanca.md` |
| 5 | Todos os dashboards anteriores | `ai-prompts/aula-05-eficiencia.md` |

### Notas gerais para todas as aulas

- **Slides vs. dados reais:** gráficos ilustrativos dos slides são exemplos conceituais. Durante a gravação, compare-os com os dados reais do Grafana e OpenCost.
- **OpenCost** é a ferramenta principal de visibilidade de custo no laboratório local.
- **AWS Cost Explorer** é complemento visual opcional nas Aulas 4 e 5 — use screenshots ou menção conceitual, sem demo obrigatória.
- Substitua dados de exemplo nos prompts pelos valores coletados ao vivo (`kubectl top`, Grafana).

Documentos de apoio: `docs/guia-gravacao.md`, `docs/cronograma-gravacao.md`, `docs/checklist-gravacao.md`, `docs/assets-gravacao.md`.

---

## Aula 1 — Observabilidade de custos e comportamento operacional

**Dashboard:** `grafana/dashboards/finops-ai-lab.json`
**Prompts:** `ai-prompts/aula-01-observabilidade.md`

---

### Vídeo 1.1 — O desafio da eficiência operacional em cloud

Objetivo:
Explicar por que ambientes distribuídos aumentam complexidade operacional e dificultam controle de custos.

Slides:
- Slide 1: Introdução
- Slide 2: O desafio da eficiência operacional em cloud
- Slide 3: Crescimento da complexidade

Demo:
Nenhuma.

Prompt IA:
Prompt 5 — Narrativa para abertura da aula (`aula-01-observabilidade.md`)

Tempo estimado:
8–10 min

---

### Vídeo 1.2 — Entendendo comportamento de consumo em cloud

Objetivo:
Explicar como workloads, escalabilidade, ambientes e pipelines influenciam padrões de utilização e custo.

Slides:
- Slide 4: Observabilidade + FinOps
- Slide 5: Workloads, requests, limits, HPA/VPA e namespaces

Demo:
```bash
kubectl get ns --show-labels
kubectl get deploy -A
```

Prompt IA:
Prompt 2 — Desperdícios operacionais em ambientes distribuídos (opcional)

Tempo estimado:
10–12 min

---

### Vídeo 1.3 — Identificando tendências de crescimento operacional

Objetivo:
Mostrar como identificar tendências de consumo e crescimento operacional usando métricas de observabilidade.

Slides:
- Slides de tendências e crescimento operacional

Demo:
Abrir Grafana — dashboard `finops-ai-lab.json`. Comentar gauges e painéis de CPU/memória por namespace.

Prompt IA:
Prompt 3 — Padrões de uso e sazonalidade

Tempo estimado:
10–12 min

---

### Vídeo 1.4 — Alertas e visibilidade de custo orientados por contexto

Objetivo:
Explicar como alertas contextualizados conectam observabilidade técnica com visibilidade de custo.

Slides:
- Slides de alertas, SLIs e visibilidade de custo

Demo:
Mencionar Prometheus (`localhost:9090`) e painéis do Grafana. Gráficos de slide como exemplo conceitual.

Prompt IA:
Prompt 4 — Métricas essenciais para FinOps em Kubernetes

Tempo estimado:
10–12 min

---

### Vídeo 1.5 — Hands-on — análise operacional de consumo em cloud

Objetivo:
Demonstrar análise operacional completa usando Grafana, kubectl e IA.

Slides:
Nenhum (ou resumo de 1 slide).

Demo:
```bash
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
kubectl get ns --show-labels
kubectl get deploy -A
kubectl top pods -A
```

1. Abrir dashboard `finops-ai-lab.json`
2. Comentar gauges e Top CPU/Memory Consumers
3. Comparar dados reais com exemplos dos slides
4. Colar Prompt 1 — Panorama de consumo por namespace

Prompt IA:
Prompt 1 — Panorama de consumo por namespace

Tempo estimado:
12–15 min

---

## Aula 2 — Rightsizing e eficiência operacional automatizada

**Dashboard:** `grafana/dashboards/finops-ai-rightsizing.json`
**Prompts:** `ai-prompts/aula-02-rightsizing.md`

---

### Vídeo 2.1 — O impacto do over-provisioning em ambientes modernos

Objetivo:
Explicar consequências de over-provisioning em custo, capacidade e operação.

Slides:
- Slides de over-provisioning e desperdício

Demo:
Nenhuma. Citar `payments-api` como exemplo do lab.

Prompt IA:
Prompt 5 — Business case para Engineering Manager

Tempo estimado:
8–10 min

---

### Vídeo 2.2 — Rightsizing baseado em comportamento real de workloads

Objetivo:
Mostrar como comparar requests vs uso real para identificar oportunidades de rightsizing.

Slides:
- Slides de rightsizing e margem de segurança

Demo:
Abrir dashboard `finops-ai-rightsizing.json` — painéis CPU/Memory Usage vs Requests.

Prompt IA:
Prompt 1 — Rightsizing do payments-api

Tempo estimado:
10–12 min

---

### Vídeo 2.3 — Ajustando recursos com automação operacional

Objetivo:
Apresentar VPA, recomendações automatizadas e rollout gradual.

Slides:
- Slides de VPA, HPA e automação

Demo:
Conceitual. Mencionar `kubectl describe deployment payments-api -n payments`.

Prompt IA:
Prompt 4 — Automação e VPA/Recommendation

Tempo estimado:
10–12 min

---

### Vídeo 2.4 — Scheduling inteligente e otimização de workloads

Objetivo:
Discutir otimização de workloads subutilizados e ambientes não produtivos.

Slides:
- Slides de scheduling e ambientes staging

Demo:
Conceitual. Citar `staging-api` como workload subutilizado.

Prompt IA:
Prompt 2 — Comparativo entre os três workloads (opcional)

Tempo estimado:
10–12 min

---

### Vídeo 2.5 — Hands-on — pipeline de rightsizing operacional

Objetivo:
Executar pipeline completo: métricas → análise → recomendação IA → plano de ação.

Slides:
Nenhum.

Demo:
```bash
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
kubectl describe deployment payments-api -n payments
kubectl top pods -n payments
```

1. Abrir dashboard `finops-ai-rightsizing.json`
2. Mostrar CPU Waste Percentage e Top Overprovisioned Pods
3. Destacar candidates payments e staging
4. Colar Prompt 1 + Prompt 2 e discutir recomendações

Prompt IA:
Prompt 1 — Rightsizing do payments-api + Prompt 2 — Comparativo entre workloads

Tempo estimado:
12–15 min

---

## Aula 3 — Anomalias de custo e capacity planning operacional

**Dashboard:** `grafana/dashboards/finops-ai-anomalies.json`
**Prompts:** `ai-prompts/aula-03-anomalias.md`

---

### Vídeo 3.1 — Detectando comportamento anormal de consumo

Objetivo:
Explicar baseline, desvio e detecção de anomalias operacionais.

Slides:
- Slides de detecção de anomalias

Demo:
Abrir dashboard — Payments CPU Timeline (baseline).

Prompt IA:
Prompt 1 — Detecção de anomalia de CPU

Tempo estimado:
8–10 min

---

### Vídeo 3.2 — Investigando origem de anomalias operacionais

Objetivo:
Demonstrar processo de investigação: detectar → correlacionar → isolar causa.

Slides:
- Slides de investigação e correlação

Demo:
```bash
./scripts/start-anomaly.sh
kubectl get pods -n payments
kubectl top pods -n payments
```

Mostrar spike no CPU Spike Detector. Explicar que `cpu-spike` simula anomalia.

Prompt IA:
Prompt 1 — Detecção de anomalia de CPU (com dados do spike)

Tempo estimado:
10–12 min

---

### Vídeo 3.3 — Planejamento operacional de capacidade

Objetivo:
Apresentar capacity planning com headroom, allocatable e projeções.

Slides:
- Slides de capacity planning (gráficos como exemplo conceitual)

Demo:
Painel Capacity Headroom no dashboard anomalies.

Prompt IA:
Prompt 3 — Capacity planning após incidente

Tempo estimado:
10–12 min

---

### Vídeo 3.4 — Otimizando uso de recursos em cloud

Objetivo:
Discutir estratégias de otimização pós-anomalia e prevenção.

Slides:
- Slides de otimização e prevenção

Demo:
```bash
./scripts/start-staging-anomaly.sh
kubectl get jobs -n staging -l app=backup-sync
kubectl top pods -n staging
```

Mostrar que staging-api está estável, mas jobs `backup-sync` geram rajadas de CPU/custo.

Prompt IA:
Prompt 4 — Anomalia silenciosa em staging

Tempo estimado:
10–12 min

---

### Vídeo 3.5 — Hands-on — análise de anomalias e capacidade operacional

Objetivo:
Fluxo completo: baseline → spike → investigação → capacity → encerramento.

Slides:
Nenhum.

Demo:
```bash
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
./scripts/start-business-hours-load.sh
sleep 120
./scripts/start-anomaly.sh
./scripts/collect-anomaly-context.sh
# ... análise no dashboard ...
./scripts/stop-all-anomalies.sh
```

1. Abrir dashboard `finops-ai-anomalies.json` (Last 15 minutes)
2. Mostrar baseline com business-hours-load, ativar spike, investigar Top CPU Consumers
3. Verificar Capacity Headroom
4. Colar saída de `collect-anomaly-context.sh` no Prompt 5 — Runbook de resposta a anomalias
5. Parar anomalias e confirmar retorno ao baseline

Prompt IA:
Prompt 5 — Runbook de resposta a anomalias

Tempo estimado:
12–15 min

---

## Aula 4 — Governança operacional e visibilidade de custos

**Dashboard:** `grafana/dashboards/finops-ai-governance.json`
**Prompts:** `ai-prompts/aula-04-governanca.md`

---

### Vídeo 4.1 — Ownership e responsabilidade sobre consumo cloud

Objetivo:
Explicar ownership, responsabilidade e accountability sobre consumo.

Slides:
- Slides de ownership e FinOps

Demo:
```bash
kubectl get ns --show-labels
```

Prompt IA:
Prompt 1 — Auditoria de labels e ownership

Tempo estimado:
8–10 min

---

### Vídeo 4.2 — Classificação operacional de recursos e ambientes

Objetivo:
Apresentar classificação por team, environment, cost-center e service-tier.

Slides:
- Slides de classificação e tagging

Demo:
Painel Governance Matrix no dashboard governance.

Prompt IA:
Prompt 5 — Política de ambientes (prod vs. staging)

Tempo estimado:
10–12 min

---

### Vídeo 4.3 — Alocação de custos orientada por contexto

Objetivo:
Explicar showback, chargeback e alocação por contexto operacional.

Slides:
- Slides de showback/chargeback (exemplos conceituais)

Demo:
Painel Showback View no dashboard. Abrir **OpenCost** (`localhost:9003`) — ferramenta principal.
*(Opcional)* Screenshot AWS Cost Explorer como complemento visual.

Prompt IA:
Prompt 2 — Showback vs. chargeback

Tempo estimado:
10–12 min

---

### Vídeo 4.4 — Guardrails e políticas de eficiência operacional

Objetivo:
Apresentar ResourceQuota, LimitRange, labels obrigatórios e políticas Kyverno/OPA.

Slides:
- Slides de guardrails e políticas

Demo:
Painel Guardrails Checklist no dashboard governance.

Prompt IA:
Prompt 3 — Guardrails sem atrito

Tempo estimado:
10–12 min

---

### Vídeo 4.5 — Hands-on — dashboard operacional de custos e governança

Objetivo:
Demonstrar visibilidade completa: labels, showback proxy, OpenCost e governança.

Slides:
Nenhum.

Demo:
```bash
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
kubectl port-forward -n opencost svc/opencost 9003:9090
kubectl get ns --show-labels
```

1. Abrir dashboard `finops-ai-governance.json`
2. Percorrer Governance Matrix, Showback View, Guardrails
3. Abrir OpenCost — custo por namespace/workload
4. Colar Prompt 4 — Visibilidade por persona
5. *(Opcional)* Comparar com screenshot AWS Cost Explorer

Prompt IA:
Prompt 4 — Visibilidade por persona

Tempo estimado:
12–15 min

---

## Aula 5 — Operações cloud orientadas por eficiência

**Dashboards:** todos os anteriores
**Prompts:** `ai-prompts/aula-05-eficiencia.md`

---

### Vídeo 5.1 — Relacionando custo, performance e observabilidade

Objetivo:
Conectar os três pilares e mostrar trade-offs em decisões operacionais.

Slides:
- Slides de custo × performance × observabilidade

Demo:
Visão rápida dos dashboards das aulas 1–4 no Grafana.

Prompt IA:
Prompt 1 — Diagnóstico consolidado do laboratório

Tempo estimado:
8–10 min

---

### Vídeo 5.2 — Tomada de decisão orientada por dados operacionais

Objetivo:
Apresentar matriz impacto × esforço e priorização de ações.

Slides:
- Slides de priorização e decisão

Demo:
Conceitual. Resumir achados do lab em tabela.

Prompt IA:
Prompt 3 — Priorização por matriz impacto × esforço

Tempo estimado:
10–12 min

---

### Vídeo 5.3 — Eficiência operacional contínua em ambientes modernos

Objetivo:
Apresentar ciclo contínuo de eficiência e plano de 90 dias.

Slides:
- Slides de eficiência contínua (forecast como exemplo conceitual)

Demo:
Nenhuma. *(Opcional)* Screenshot AWS Cost Explorer forecast.

Prompt IA:
Prompt 2 — Plano de otimização contínua (90 dias)

Tempo estimado:
10–12 min

---

### Vídeo 5.4 — Construindo uma cultura operacional orientada por eficiência

Objetivo:
Fechar o arco do curso com cultura, KPIs e governança de longo prazo.

Slides:
- Slides de cultura FinOps e KPIs

Demo:
Nenhuma.

Prompt IA:
Prompt 4 — Recomendações executivas (CTO / VP Engineering)

Tempo estimado:
10–12 min

---

### Vídeo 5.5 — Hands-on — fluxo operacional completo de FinOps com IA

Objetivo:
Executar fluxo end-to-end: observar → rightsizing → anomalias → governança → plano consolidado com IA.

Slides:
Nenhum.

Demo:
```bash
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
kubectl port-forward -n opencost svc/opencost 9003:9090
kubectl top pods -A
```

1. Percorrer os 4 dashboards (resumo de 1 min cada)
2. Resumir achados: payments overprovisionado, users saudável, staging subutilizado, cpu-spike como lição
3. Abrir OpenCost para visão consolidada
4. Colar **Prompt 5 — Copiloto de eficiência (prompt mestre)**
5. Apresentar plano de 90 dias e KPIs da resposta

Prompt IA:
**Prompt 5 — Copiloto de eficiência — prompt mestre reutilizável**

Tempo estimado:
12–15 min
