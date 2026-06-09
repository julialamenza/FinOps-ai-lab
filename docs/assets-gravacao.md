# FinOps com IA — Assets de Gravação

Lista de screenshots e assets visuais necessários para o curso, com indicação de uso por aula.

---

## Visão geral

| Tipo de asset | Obrigatório | Opcional |
|---------------|-------------|----------|
| Dashboards Grafana | ✅ | — |
| OpenCost UI | ✅ (Aulas 4 e 5) | — |
| kubectl / terminal | ✅ | — |
| Prompts IA | ✅ (hands-on) | — |
| AWS Cost Explorer | — | ✅ (Aulas 4 e 5) |

> **AWS Cost Explorer** é complemento visual opcional. O laboratório local usa **OpenCost** como ferramenta principal de visibilidade de custo.

---

## Screenshots obrigatórios

### Dashboards Grafana

| Screenshot | Arquivo de origem | Usar em |
|------------|-------------------|---------|
| Visão geral do cluster (CPU, Memory, gauges) | `finops-ai-lab.json` | Aula 1 — vídeos 1.3, 1.4, 1.5 |
| Top CPU Consumers e Top Memory Consumers | `finops-ai-lab.json` | Aula 1 — vídeo 1.5 |
| CPU Usage vs CPU Requests por namespace | `finops-ai-rightsizing.json` | Aula 2 — vídeos 2.2, 2.5 |
| CPU Waste Percentage (payments alto) | `finops-ai-rightsizing.json` | Aula 2 — vídeos 2.1, 2.5 |
| Top CPU Overprovisioned Pods | `finops-ai-rightsizing.json` | Aula 2 — vídeo 2.5 |
| Rightsizing Candidates (payments, staging) | `finops-ai-rightsizing.json` | Aula 2 — vídeo 2.5 |
| Payments CPU Timeline (baseline) | `finops-ai-anomalies.json` | Aula 3 — vídeo 3.1 |
| CPU Spike Detector com spike ativo | `finops-ai-anomalies.json` | Aula 3 — vídeos 3.2, 3.5 |
| Top CPU Consumers com cpu-spike no topo | `finops-ai-anomalies.json` | Aula 3 — vídeo 3.5 |
| Capacity Headroom — CPU | `finops-ai-anomalies.json` | Aula 3 — vídeo 3.3 |
| Governance Matrix | `finops-ai-governance.json` | Aula 4 — vídeo 4.2 |
| Showback View by Namespace | `finops-ai-governance.json` | Aula 4 — vídeo 4.3 |
| Guardrails Checklist | `finops-ai-governance.json` | Aula 4 — vídeo 4.4 |

### Grafana (UI geral)

| Screenshot | Usar em |
|------------|---------|
| Tela de import de dashboard (upload JSON) | Aula 1 — vídeo 1.5 (ou material de apoio) |
| Seleção de datasource Prometheus no import | Aula 1 — vídeo 1.5 |
| Menu Dashboards com os 4 dashboards listados | Aula 5 — vídeo 5.5 |

### OpenCost

| Screenshot | Usar em |
|------------|---------|
| Tela inicial do OpenCost (`localhost:9003`) | Aula 4 — vídeo 4.5 |
| Custo/allocação por namespace | Aula 4 — vídeos 4.3, 4.5 |
| Visão consolidada por workload | Aula 5 — vídeo 5.5 |

### Terminal / kubectl

| Screenshot | Comando | Usar em |
|------------|---------|---------|
| Namespaces com labels | `kubectl get ns --show-labels` | Aula 1 — vídeo 1.2; Aula 4 — vídeos 4.1, 4.5 |
| Deployments do lab | `kubectl get deploy -A` | Aula 1 — vídeo 1.2 |
| Uso de recursos por pod | `kubectl top pods -A` | Aula 1 — vídeo 1.5 |
| Requests do payments-api | `kubectl describe deployment payments-api -n payments` | Aula 2 — vídeo 2.5 |
| Pods com cpu-spike ativo | `kubectl get pods -n payments` (com cpu-spike Running) | Aula 3 — vídeo 3.5 |
| CPU do cpu-spike | `kubectl top pods -n payments` (com spike) | Aula 3 — vídeo 3.5 |

### Prompts IA

| Screenshot | Usar em |
|------------|---------|
| Prompt colado na ferramenta de IA (antes de enviar) | Hands-on de cada aula (1.5, 2.5, 3.5, 4.5, 5.5) |
| Resposta da IA com recomendações | Hands-on de cada aula |
| Prompt mestre da Aula 5 (`aula-05-eficiencia.md` → Prompt 5) | Aula 5 — vídeo 5.5 |

---

## Screenshots opcionais

### AWS Cost Explorer *(complemento visual — Aulas 4 e 5)*

| Screenshot | Usar em | Observação |
|------------|---------|------------|
| Visão geral de custos por serviço AWS | Aula 4 — vídeo 4.3 | Comparar com OpenCost (K8s vs cloud provider) |
| Custos agrupados por tag (cost-center, team) | Aula 4 — vídeo 4.3 | Ilustrar showback em ambiente AWS real |
| Forecast de custos (previsão) | Aula 5 — vídeo 5.3 | Conceito de planejamento — lab local não tem forecast real |
| Cost Explorer vs. OpenCost lado a lado | Aula 5 — vídeo 5.1 | Reforçar complementaridade das ferramentas |

> Não é necessário ter conta AWS ativa para gravar o curso. Use screenshots preparados previamente ou explique conceitualmente via slides.

### Prometheus (opcional)

| Screenshot | Usar em |
|------------|---------|
| Query de CPU usage no Prometheus UI | Aula 1 — vídeo 1.4 |
| Alertmanager (se configurado) | Aula 1 — vídeo 1.4 |

---

## Assets por aula — resumo

| Aula | Screenshots obrigatórios | Screenshots opcionais |
|------|--------------------------|----------------------|
| **1** | Dashboard principal, kubectl labels/deploys, kubectl top, prompt IA | Prometheus query |
| **2** | Dashboard rightsizing (waste, overprovisioned pods, candidates), describe payments-api, prompt IA | — |
| **3** | Dashboard anomalies (timeline, spike detector, top consumers, headroom), cpu-spike ativo (get pods + top), prompt IA | — |
| **4** | Dashboard governance (matrix, showback, guardrails), kubectl labels, OpenCost UI, prompt IA | AWS Cost Explorer |
| **5** | Todos os dashboards (visão rápida), OpenCost consolidado, prompt mestre | AWS Cost Explorer, comparativo lado a lado |

---

## Convenção de nomes para arquivos exportados

Salve screenshots em pasta local (fora do repo ou em pasta de produção):

```text
assets/
  aula-01/
    grafana-lab-overview.png
    kubectl-ns-labels.png
    prompt-01-panorama.png
  aula-02/
    grafana-rightsizing-waste.png
    grafana-overprovisioned-pods.png
  aula-03/
    grafana-spike-detector.png
    kubectl-cpu-spike-active.png
  aula-04/
    grafana-governance-matrix.png
    opencost-by-namespace.png
    cost-explorer-optional.png
  aula-05/
    grafana-all-dashboards.png
    opencost-consolidated.png
    prompt-mestre.png
```

---

## Dicas para captura

1. **Grafana:** use tema escuro, refresh 10s, janela de tempo `now-1h` para ter histórico visível.
2. **cpu-spike:** capture antes (baseline), durante (spike) e depois (`stop-anomaly.sh`) — três screenshots.
3. **OpenCost:** aguarde dados carregarem; pode levar 1–2 min após port-forward.
4. **Prompts IA:** oculte informações pessoais da conta; mostre apenas o prompt e a resposta.
5. **Cost Explorer:** se usar screenshots opcionais, anonimize IDs de conta AWS.

---

## Referências

- `docs/guia-gravacao.md` — comandos para reproduzir cada screenshot ao vivo
- `docs/checklist-gravacao.md` — validar assets antes de gravar
- `grafana/dashboards/` — origem dos dashboards
- `ai-prompts/` — origem dos prompts
