# FinOps com IA — Guia de Gravação

Guia operacional para preparar o ambiente, configurar a tela e executar as demos de cada aula do curso.

---

## Preparação antes de gravar

### 1. Subir o laboratório

```bash
# Na raiz do repositório
minikube start --cpus=4 --memory=8192
./scripts/deploy-lab.sh
./scripts/install-opencost.sh
```

### 2. Importar dashboards no Grafana

Importe os 4 dashboards via Grafana UI (Dashboards → Import → Upload JSON):

| Dashboard | Arquivo |
|-----------|---------|
| Principal (Aula 1) | `grafana/dashboards/finops-ai-lab.json` |
| Rightsizing (Aula 2) | `grafana/dashboards/finops-ai-rightsizing.json` |
| Anomalies (Aula 3) | `grafana/dashboards/finops-ai-anomalies.json` |
| Governance (Aula 4) | `grafana/dashboards/finops-ai-governance.json` |

Selecione o datasource **Prometheus** em cada import.

### 3. Abrir materiais de apoio

| Material | Caminho |
|----------|---------|
| Prompts IA | `ai-prompts/aula-0X-*.md` (um por aula) |
| Roteiro detalhado | `docs/roteiro-gravacao.md` |
| Checklist | `docs/checklist-gravacao.md` |
| Slides | Apresentação Gamma/PPT da aula correspondente |

### 4. Garantir que cpu-spike está parado

```bash
./scripts/stop-anomaly.sh
kubectl get pods -n payments
```

---

## Configuração recomendada de tela

| Elemento | Recomendação |
|----------|--------------|
| Resolução | 1920×1080 (mínimo 1280×720) |
| Zoom do sistema | 100–125% (texto legível no vídeo) |
| Layout | Editor/terminal à esquerda (60%), navegador à direita (40%) — ou tela cheia alternando |
| Fonte do terminal | 14–16 pt, tema escuro com bom contraste |
| Abas do navegador | Apenas Grafana, Prometheus, OpenCost e ferramenta de IA |
| Notificações | Desativadas (modo Não Perturbe) |
| Credenciais | Esconder senhas do Grafana; não mostrar tokens ou `.env` |

### Ordem sugerida de janelas

1. Terminal (kubectl, scripts)
2. Grafana (dashboard da aula)
3. Ferramenta de IA (ChatGPT, Claude ou Cursor)
4. Prometheus ou OpenCost (quando necessário)

---

## Port-forwards úteis

Abra cada port-forward em um terminal separado **antes** de gravar o hands-on:

### Grafana

```bash
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
```

Acesso: `http://localhost:3000`

Senha admin:

```bash
kubectl get secret -n monitoring monitoring-grafana \
  -o jsonpath="{.data.admin-password}" | base64 -d && echo
```

### Prometheus

```bash
kubectl port-forward -n monitoring svc/monitoring-kube-prometheus-prometheus 9090:9090
```

Acesso: `http://localhost:9090`

### OpenCost

```bash
kubectl port-forward -n opencost svc/opencost 9003:9090
```

Acesso: `http://localhost:9003`

---

## Comandos para validar o ambiente

Execute antes de cada sessão de gravação:

```bash
# Cluster ativo
kubectl cluster-info

# Pods do monitoring
kubectl get pods -n monitoring

# Pods do OpenCost
kubectl get pods -n opencost

# Workloads do lab
kubectl get pods -A | grep -E 'payments|users|staging'

# Uso de recursos
kubectl top pods -A

# Labels de governança
kubectl get ns --show-labels

# Deployments
kubectl get deploy -A

# Detalhes dos workloads principais
kubectl describe deployment payments-api -n payments
kubectl describe deployment users-api -n users
kubectl describe deployment staging-api -n staging
```

Se algum pod estiver em `CrashLoopBackOff` ou `Pending`, resolva antes de gravar.

---

## Mapeamento: dashboards por aula

| Aula | Dashboard | Quando abrir |
|------|-----------|--------------|
| 1 | `grafana/dashboards/finops-ai-lab.json` | Vídeos 1.3, 1.4 e 1.5 |
| 2 | `grafana/dashboards/finops-ai-rightsizing.json` | Vídeos 2.2 e 2.5 |
| 3 | `grafana/dashboards/finops-ai-anomalies.json` | Vídeos 3.1 a 3.5 |
| 4 | `grafana/dashboards/finops-ai-governance.json` | Vídeos 4.2 a 4.5 |
| 5 | Todos os dashboards anteriores | Vídeo 5.5 (fluxo completo) |

### Painéis-chave por dashboard

**finops-ai-lab.json**
- Cluster CPU/Memory Usage
- Gauges por namespace (payments, users, staging)
- Top CPU/Memory Consumers

**finops-ai-rightsizing.json**
- CPU/Memory Usage vs Requests
- CPU/Memory Waste Percentage
- Top CPU Overprovisioned Pods
- Rightsizing Candidates (payments, staging)

**finops-ai-anomalies.json**
- Payments CPU Timeline
- CPU Spike Detector
- Top CPU Consumers
- Capacity Headroom
- cpu-spike Investigation (comandos)

**finops-ai-governance.json**
- CPU/Memory Usage e Requests por namespace
- Governance Matrix
- Showback View by Namespace
- Guardrails Checklist
- OpenCost + AWS Cost Explorer (texto comparativo)

---

## Mapeamento: prompts IA por aula

| Aula | Arquivo de prompts | Prompts principais por vídeo |
|------|-------------------|------------------------------|
| 1 | `ai-prompts/aula-01-observabilidade.md` | 1.1 → Prompt 5 (narrativa); 1.3 → Prompt 3; 1.4 → Prompt 4; 1.5 → Prompt 1 |
| 2 | `ai-prompts/aula-02-rightsizing.md` | 2.1 → Prompt 5; 2.2 → Prompt 1; 2.3 → Prompt 4; 2.5 → Prompt 1 + 2 |
| 3 | `ai-prompts/aula-03-anomalias.md` | 3.1 → Prompt 1; 3.2 → Prompt 1; 3.3 → Prompt 3; 3.5 → Prompt 5 |
| 4 | `ai-prompts/aula-04-governanca.md` | 4.1 → Prompt 1; 4.3 → Prompt 2; 4.4 → Prompt 3; 4.5 → Prompt 4 |
| 5 | `ai-prompts/aula-05-eficiencia.md` | 5.1 → Prompt 1; 5.2 → Prompt 3; 5.3 → Prompt 2; 5.5 → **Prompt 5 (mestre)** |

> Substitua os dados de exemplo nos prompts pelos valores reais coletados no Grafana ou `kubectl top` durante a gravação.

---

## Roteiro operacional por aula

### Aula 1 — Observabilidade

**Vídeos teóricos (1.1–1.4):** slides + eventual menção ao lab.

**Vídeo 1.5 — Hands-on:**

```bash
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
kubectl get ns --show-labels
kubectl get deploy -A
kubectl top pods -A
```

1. Abrir dashboard `finops-ai-lab.json`
2. Comentar gauges de CPU/memória por namespace
3. Mostrar Top CPU/Memory Consumers
4. Colar Prompt 1 de `aula-01-observabilidade.md` na IA
5. Comparar resposta da IA com dados reais do Grafana

---

### Aula 2 — Rightsizing

**Vídeos teóricos (2.1–2.4):** slides; no 2.2, mostrar painéis usage vs requests.

**Vídeo 2.5 — Hands-on:**

```bash
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
kubectl describe deployment payments-api -n payments
kubectl top pods -n payments
```

1. Abrir dashboard `finops-ai-rightsizing.json`
2. Mostrar CPU Waste Percentage (payments deve estar alto)
3. Abrir tabela Top CPU Overprovisioned Pods
4. Destacar Rightsizing Candidates (payments, staging)
5. Colar Prompt 1 de `aula-02-rightsizing.md` e discutir recomendações

---

### Aula 3 — Anomalias e capacity planning

**Vídeos teóricos (3.1–3.4):** slides + dashboard anomalies nos vídeos 3.1–3.3.

**Vídeo 3.5 — Hands-on:**

```bash
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
./scripts/start-anomaly.sh
kubectl top pods -n payments
kubectl get pods -n payments
```

1. Abrir dashboard `finops-ai-anomalies.json`
2. Observar baseline em Payments CPU Timeline
3. Executar `start-anomaly.sh` e mostrar spike no CPU Spike Detector
4. Verificar `cpu-spike` no Top CPU Consumers
5. Colar Prompt 1 de `aula-03-anomalias.md` com dados do spike
6. Encerrar com `./scripts/stop-anomaly.sh`

---

### Aula 4 — Governança e visibilidade de custos

**Vídeos teóricos (4.1–4.4):** slides + labels + showback.

**Vídeo 4.5 — Hands-on:**

```bash
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
kubectl port-forward -n opencost svc/opencost 9003:9090
kubectl get ns --show-labels
```

1. Abrir dashboard `finops-ai-governance.json`
2. Mostrar Governance Matrix e Label Coverage
3. Abrir Showback View by Namespace (proxy didático)
4. Abrir OpenCost em `http://localhost:9003` — **ferramenta principal do lab**
5. Colar Prompt 2 de `aula-04-governanca.md` (showback vs chargeback)
6. *(Opcional)* Mostrar screenshot do AWS Cost Explorer como complemento visual

---

### Aula 5 — Eficiência operacional contínua

**Vídeos teóricos (5.1–5.4):** consolidação conceitual; Cost Explorer opcional nas Aulas 4 e 5.

**Vídeo 5.5 — Hands-on (fluxo completo):**

```bash
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
kubectl port-forward -n opencost svc/opencost 9003:9090
kubectl top pods -A
```

1. Percorrer rapidamente os 4 dashboards (1 min cada)
2. Resumir achados: over-provisioning (Aula 2), anomalia (Aula 3), governança (Aula 4)
3. Abrir OpenCost para visão consolidada de custo
4. Colar **Prompt 5 (mestre)** de `aula-05-eficiencia.md`
5. Apresentar plano de 90 dias e KPIs da resposta da IA

---

## Notas importantes para a gravação

### Slides vs. dados reais

Gráficos ilustrativos dos slides são **exemplos conceituais**. Durante a gravação, compare-os com os dados reais do Grafana e OpenCost. Frases úteis:

- "No slide usamos um exemplo ilustrativo; agora vamos ver o que o laboratório mostra de fato."
- "Os números do dashboard são ao vivo — podem diferir levemente dos exemplos dos slides."

### OpenCost vs. AWS Cost Explorer

| Ferramenta | Papel no curso |
|------------|----------------|
| **OpenCost** | Ferramenta principal do laboratório local — use nas demos |
| **AWS Cost Explorer** | Complemento visual opcional nas Aulas 4 e 5 — screenshots, sem demo ao vivo obrigatória |

### Scripts de anomalia

| Script | Função |
|--------|--------|
| `./scripts/start-anomaly.sh` | Ativa `cpu-spike` no namespace payments |
| `./scripts/stop-anomaly.sh` | Remove o workload de anomalia |

Teste ambos **antes** de gravar a Aula 3.

---

## Referências

- `docs/roteiro-gravacao.md` — roteiro detalhado por vídeo
- `docs/cronograma-gravacao.md` — cronograma e status dos 25 vídeos
- `docs/checklist-gravacao.md` — checklist pré/pós gravação
- `docs/assets-gravacao.md` — screenshots necessários
- `README.md` — instruções completas do laboratório
