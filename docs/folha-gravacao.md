# FinOps com IA — Folha Operacional de Gravação

Documento de consulta rápida para gravar as **5 aulas** e **25 vídeos**. Mantenha este arquivo aberto durante a gravação.

> O lab é montado **na hora**. Use **Last 15 minutes** em todos os dashboards Grafana.

---

## 1. Setup global (início de cada dia de gravação)

Execute na raiz do repositório:

```bash
cd /caminho/para/finops-ai-lab

minikube start --cpus=4 --memory=8192
kubectl cluster-info

chmod +x scripts/*.sh
./scripts/deploy-lab.sha
./scripts/install-opencost.sh

# Estado limpo — sem anomalias ativas
./scripts/stop-all-anomalies.sh

# Validar
kubectl get pods -n monitoring
kubectl get pods -n opencost
kubectl get deploy -A | grep -E 'payments|users|staging'
kubectl top pods -A
```

### Importar dashboards (primeira vez ou cluster novo)

Grafana → Dashboards → Import → Upload JSON → datasource **Prometheus**:

| Dashboard | Arquivo |
|-----------|---------|
| Aula 1 | `grafana/dashboards/finops-ai-lab.json` |
| Aula 2 | `grafana/dashboards/finops-ai-rightsizing.json` |
| Aula 3 | `grafana/dashboards/finops-ai-anomalies.json` |
| Aula 4 | `grafana/dashboards/finops-ai-governance.json` |

---

## 2. Port-forwards e acessos (copiar e colar)

Abra **um terminal por port-forward** e deixe rodando durante a sessão.

### Terminal A — Grafana

```bash
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
```

| Campo | Valor |
|-------|-------|
| URL | http://localhost:3000 |
| Usuário | `admin` |
| Senha | ver comando abaixo |

```bash
kubectl get secret -n monitoring monitoring-grafana \
  -o jsonpath="{.data.admin-password}" | base64 -d && echo
```

### Terminal B — Prometheus

```bash
kubectl port-forward -n monitoring svc/monitoring-kube-prometheus-prometheus 9090:9090
```

| Campo | Valor |
|-------|-------|
| URL | http://localhost:9090 |

### Terminal C — OpenCost

```bash
kubectl port-forward -n opencost svc/opencost 9003:9090
```

| Campo | Valor |
|-------|-------|
| URL | http://localhost:9003 |
| Uso principal | Allocation, Namespace Costs, Workload Costs |

### Quais port-forwards abrir por aula

| Aula | Grafana | Prometheus | OpenCost |
|------|---------|------------|----------|
| 1 | ✅ (1.3, 1.4, 1.5) | ⬜ opcional (1.4) | — |
| 2 | ✅ (2.2, 2.5) | — | — |
| 3 | ✅ (3.1–3.5) | — | — |
| 4 | ✅ (4.2–4.5) | — | ✅ (4.3, 4.5) |
| 5 | ✅ (5.1, 5.5) | — | ✅ (5.5) |

---

## 3. Scripts úteis (referência rápida)

```bash
# Carga por horário comercial (Aula 1 — aguarde 2–3 min)
./scripts/start-business-hours-load.sh
./scripts/stop-business-hours-load.sh

# Coleta de dados para prompts de IA
./scripts/collect-lab-context.sh          # Aulas 1, 2, 4, 5
./scripts/collect-anomaly-context.sh      # Aula 3

# Anomalias (Aula 3)
./scripts/start-anomaly.sh                # spike CPU (~30s para aparecer)
./scripts/start-anomaly.sh --duration 180
./scripts/start-staging-anomaly.sh        # CronJob backup-sync (job imediato)
./scripts/stop-all-anomalies.sh           # limpar tudo
```

---

## 4. Legenda dos tipos de vídeo

| Tipo | Significado |
|------|-------------|
| **T** | Teoria pura — slides + prompt IA, sem lab |
| **T+** | Teoria + demo leve — kubectl ou dashboard estático |
| **T++** | Teoria + demo ativa — scripts, spikes, jobs |
| **H** | Hands-on — demo completa (vídeo X.5) |

---

# AULA 1 — Observabilidade de custos

| Item | Valor |
|------|-------|
| Dashboard | `finops-ai-lab.json` |
| Prompts | `ai-prompts/aula-01-observabilidade.md` |
| Port-forwards | Grafana (1.3+) |

### Início da sessão (Dia 3 — teoria | Dia 4 — hands-on)

```bash
./scripts/stop-all-anomalies.sh
# Terminal A: port-forward Grafana (se gravar 1.3, 1.4 ou 1.5)
```

### Vídeos

| Vídeo | Título | Tipo | Tempo | O que gravar |
|-------|--------|------|-------|--------------|
| **1.1** | O desafio da eficiência operacional em cloud | **T** | 8–10 | Slides. Prompt 5 (narrativa). Sem terminal. |
| **1.2** | Entendendo comportamento de consumo em cloud | **T+** | 10–12 | Slides + comandos abaixo. Prompt 2 opcional. |
| **1.3** | Identificando tendências de crescimento operacional | **T+** | 10–12 | Slides + Grafana. Opcional: business-hours 2 min antes. Prompt 3. |
| **1.4** | Alertas e visibilidade de custo orientados por contexto | **T+** | 10–12 | Slides + Grafana + menção Prometheus. Prompt 4. |
| **1.5** | **Hands-on — análise operacional de consumo** | **H** | 12–15 | Fluxo completo abaixo. Prompt 1. |

### Comandos por vídeo

**1.2 — demo leve:**
```bash
kubectl get ns --show-labels
kubectl get deploy -A
```

**1.3 — dashboard (opcional: carga antes):**
```bash
./scripts/start-business-hours-load.sh
# aguarde 2–3 min
# Grafana → finops-ai-lab.json → Last 15 minutes
```

**1.5 — HANDS-ON:**
```bash
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
./scripts/start-business-hours-load.sh
sleep 120
./scripts/collect-lab-context.sh
```

Passos na tela:
1. http://localhost:3000 → `finops-ai-lab.json` → **Last 15 minutes**
2. Gauges por namespace + Top CPU/Memory Consumers
3. Colar saída do `collect-lab-context.sh` no **Prompt 1**
4. Comparar resposta da IA com o Grafana

---

# AULA 2 — Rightsizing

| Item | Valor |
|------|-------|
| Dashboard | `finops-ai-rightsizing.json` |
| Prompts | `ai-prompts/aula-02-rightsizing.md` |
| Port-forwards | Grafana (2.2, 2.5) |

### Início da sessão (Dia 5 — teoria | Dia 6 — hands-on)

```bash
./scripts/stop-all-anomalies.sh
# Terminal A: port-forward Grafana (se gravar 2.2 ou 2.5)
```

### Vídeos

| Vídeo | Título | Tipo | Tempo | O que gravar |
|-------|--------|------|-------|--------------|
| **2.1** | O impacto do over-provisioning | **T** | 8–10 | Slides. Citar `payments-api`. Prompt 5. |
| **2.2** | Rightsizing baseado em comportamento real | **T+** | 10–12 | Slides + dashboard Usage vs Requests. Prompt 1. |
| **2.3** | Ajustando recursos com automação | **T+** | 10–12 | Slides + `kubectl describe` opcional. Prompt 4. |
| **2.4** | Scheduling inteligente e otimização | **T** | 10–12 | Slides. Citar `staging-api`. Prompt 2 opcional. |
| **2.5** | **Hands-on — pipeline de rightsizing** | **H** | 12–15 | Fluxo completo abaixo. Prompt 1 + 2. |

### Comandos por vídeo

**2.2 — dashboard:**
```bash
# Grafana → finops-ai-rightsizing.json → Last 15 minutes
# Painéis: Usage vs Requests, Waste %
```

**2.3 — menção opcional:**
```bash
kubectl describe deployment payments-api -n payments
```

**2.5 — HANDS-ON:**
```bash
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
./scripts/collect-lab-context.sh
kubectl describe deployment payments-api -n payments
kubectl top pods -n payments
```

Passos na tela:
1. `finops-ai-rightsizing.json` → CPU Waste, Top Overprovisioned, Candidates
2. Destacar **payments** (over) e **staging** (sub)
3. Colar `collect-lab-context.sh` nos **Prompts 1 + 2**
4. Enfatizar: não aplicaria em prod sem validar em staging

---

# AULA 3 — Anomalias e capacity planning

| Item | Valor |
|------|-------|
| Dashboard | `finops-ai-anomalies.json` |
| Prompts | `ai-prompts/aula-03-anomalias.md` |
| Port-forwards | Grafana (todos os vídeos 3.x) |

### Início da sessão (Dia 7 — teoria | Dia 8 — hands-on)

```bash
./scripts/stop-all-anomalies.sh
kubectl get pods -n payments
kubectl get cronjobs,jobs -n staging
# Terminal A: port-forward Grafana
```

### Vídeos

| Vídeo | Título | Tipo | Tempo | O que gravar |
|-------|--------|------|-------|--------------|
| **3.1** | Detectando comportamento anormal de consumo | **T+** | 8–10 | Slides + dashboard **sem** spike. Prompt 1 (exemplo). |
| **3.2** | Investigando origem de anomalias | **T++** | 10–12 | Slides + ativar spike. Prompt 1 com dados reais. |
| **3.3** | Planejamento operacional de capacidade | **T+** | 10–12 | Slides + Capacity Headroom. Prompt 3. |
| **3.4** | Otimizando uso de recursos em cloud | **T++** | 10–12 | Slides + anomalia silenciosa staging. Prompt 4. |
| **3.5** | **Hands-on — anomalias e capacidade** | **H** | 12–15 | Fluxo completo abaixo. Prompt 5. |

### Comandos por vídeo

**3.1 — dashboard estático (baseline):**
```bash
# Grafana → finops-ai-anomalies.json → Last 15 minutes
# Painel: Payments CPU Timeline (sem cpu-spike ativo)
```

**3.2 — demo ativa (parar ao final do vídeo):**
```bash
./scripts/start-anomaly.sh
kubectl get pods -n payments
kubectl top pods -n payments
# Grafana → CPU Spike Detector (~30s)
./scripts/stop-anomaly.sh
```

**3.3 — capacity:**
```bash
# Grafana → painel Capacity Headroom
```

**3.4 — anomalia silenciosa (parar ao final):**
```bash
./scripts/start-staging-anomaly.sh
kubectl get jobs -n staging -l app=backup-sync
kubectl top pods -n staging
# Prompt 4
./scripts/stop-staging-anomaly.sh
```

**3.5 — HANDS-ON:**
```bash
./scripts/stop-all-anomalies.sh
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
./scripts/start-business-hours-load.sh
sleep 120
./scripts/start-anomaly.sh
./scripts/collect-anomaly-context.sh
```

Passos na tela:
1. `finops-ai-anomalies.json` → **Last 15 minutes**
2. Baseline → spike → Top CPU Consumers → Capacity Headroom
3. Colar `collect-anomaly-context.sh` no **Prompt 5**
4. `./scripts/stop-all-anomalies.sh` → confirmar retorno ao baseline

---

# AULA 4 — Governança e visibilidade de custos

| Item | Valor |
|------|-------|
| Dashboard | `finops-ai-governance.json` |
| Prompts | `ai-prompts/aula-04-governanca.md` |
| Port-forwards | Grafana (4.2+) + OpenCost (4.3, 4.5) |

### Início da sessão (Dia 9 — teoria | Dia 10 — hands-on)

```bash
./scripts/stop-all-anomalies.sh
# Terminal A: Grafana
# Terminal C: OpenCost (se gravar 4.3 ou 4.5)
```

### Vídeos

| Vídeo | Título | Tipo | Tempo | O que gravar |
|-------|--------|------|-------|--------------|
| **4.1** | Ownership e responsabilidade | **T+** | 8–10 | Slides + labels. Prompt 1. |
| **4.2** | Classificação de recursos e ambientes | **T+** | 10–12 | Slides + Governance Matrix. Prompt 5. |
| **4.3** | Alocação de custos por contexto | **T+** | 10–12 | Slides + Showback + OpenCost. Prompt 2. |
| **4.4** | Guardrails e políticas | **T+** | 10–12 | Slides + Guardrails Checklist. Prompt 3. |
| **4.5** | **Hands-on — governança e custos** | **H** | 12–15 | Fluxo completo abaixo. Prompt 4. |

### Comandos por vídeo

**4.1:**
```bash
kubectl get ns --show-labels
```

**4.2 — dashboard:**
```bash
# Grafana → finops-ai-governance.json → Governance Matrix
```

**4.3 — showback + OpenCost:**
```bash
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
kubectl port-forward -n opencost svc/opencost 9003:9090
# Grafana → Showback View
# http://localhost:9003 → Allocation / Namespace Costs
```

**4.4 — guardrails:**
```bash
# Grafana → Guardrails Checklist (conceitual — não deployado no lab)
```

**4.5 — HANDS-ON:**
```bash
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
kubectl port-forward -n opencost svc/opencost 9003:9090
./scripts/collect-lab-context.sh
kubectl get ns --show-labels
```

Passos na tela:
1. `finops-ai-governance.json` → Matrix, Showback, Guardrails
2. http://localhost:9003 → custo por namespace/workload
3. Colar `collect-lab-context.sh` no **Prompt 4**
4. *(Opcional)* screenshot AWS Cost Explorer

---

# AULA 5 — Eficiência operacional contínua

| Item | Valor |
|------|-------|
| Dashboards | Todos os 4 anteriores |
| Prompts | `ai-prompts/aula-05-eficiencia.md` |
| Port-forwards | Grafana (5.1, 5.5) + OpenCost (5.5) |

### Início da sessão (Dia 11 — teoria | Dia 12 — hands-on)

```bash
./scripts/stop-all-anomalies.sh
# Terminal A: Grafana (5.1 tour)
# Dia 12: Terminal A + C para 5.5
```

### Vídeos

| Vídeo | Título | Tipo | Tempo | O que gravar |
|-------|--------|------|-------|--------------|
| **5.1** | Custo × performance × observabilidade | **T+** | 8–10 | Slides + tour rápido nos 4 dashboards. Prompt 1. |
| **5.2** | Tomada de decisão orientada por dados | **T** | 10–12 | Slides + matriz impacto×esforço. Prompt 3. |
| **5.3** | Eficiência contínua (90 dias) | **T** | 10–12 | Slides. Prompt 2. Sem lab. |
| **5.4** | Cultura orientada por eficiência | **T** | 10–12 | Slides de fechamento. Prompt 4. |
| **5.5** | **Hands-on — fluxo completo FinOps com IA** | **H** | 12–15 | Fluxo end-to-end abaixo. **Prompt 5 mestre**. |

### Comandos por vídeo

**5.1 — tour dashboards (~30s cada):**
```bash
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
# finops-ai-lab → rightsizing → anomalies → governance
```

**5.5 — HANDS-ON FINAL:**
```bash
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
kubectl port-forward -n opencost svc/opencost 9003:9090
./scripts/collect-lab-context.sh
kubectl top pods -A
```

Passos na tela:
1. Percorrer 4 dashboards (1 min cada) → **Last 15 minutes**
2. Resumo: payments over, users ok, staging sub, anomalias = lição
3. http://localhost:9003 → visão consolidada
4. Colar `collect-lab-context.sh` no **Prompt 5 (mestre)**
5. Plano de 90 dias + KPIs da resposta da IA

---

## 5. Calendário sugerido (15 dias)

| Dia | Vídeos | Port-forwards |
|-----|--------|---------------|
| 1–2 | Preparação | Validar tudo |
| 3 | 1.1–1.4 | Grafana (1.3+) |
| 4 | **1.5** | Grafana |
| 5 | 2.1–2.4 | Grafana (2.2) |
| 6 | **2.5** | Grafana |
| 7 | 3.1–3.4 | Grafana |
| 8 | **3.5** | Grafana |
| 9 | 4.1–4.4 | Grafana + OpenCost (4.3) |
| 10 | **4.5** | Grafana + OpenCost |
| 11 | 5.1–5.4 | Grafana (5.1) |
| 12 | **5.5** | Grafana + OpenCost |
| 13–15 | Revisão e entrega | — |

---

## 6. Frases úteis na gravação

- *"No slide usamos um exemplo ilustrativo; agora vamos ver o que o laboratório mostra de fato."*
- *"Os números do dashboard são ao vivo — podem diferir dos exemplos dos prompts."*
- *"A IA acelera a análise, mas a decisão final é humana."*
- *"Não aplicaria essa mudança em produção sem validar em staging."*

---

## 7. Checklist rápido antes de gravar

- [ ] `minikube status` → Running
- [ ] `./scripts/stop-all-anomalies.sh`
- [ ] Port-forwards da aula abertos
- [ ] Dashboards com dados (sem "No data")
- [ ] Prompts da aula abertos (`ai-prompts/aula-0X-*.md`)
- [ ] Slides da aula abertos
- [ ] Notificações desativadas
- [ ] Senha Grafana não visível na tela

---

## Referências

| Arquivo | Conteúdo |
|---------|----------|
| `docs/roteiro-gravacao.md` | Roteiro detalhado por vídeo |
| `docs/guia-gravacao.md` | Guia técnico completo |
| `docs/checklist-gravacao.md` | Checklist pré/pós gravação |
| `docs/cronograma-gravacao.md` | Cronograma de 15 dias |
| `README.md` | Instalação do laboratório |
