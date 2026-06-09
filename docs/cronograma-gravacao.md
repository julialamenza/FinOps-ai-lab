# FinOps com IA — Cronograma de Gravação

Cronograma operacional para gravar **5 aulas** e **25 vídeos** do curso, usando o laboratório local (Minikube, Prometheus, Grafana, OpenCost).

---

## Visão geral até a entrega

| Fase | Período sugerido | Entregável |
|------|------------------|------------|
| **Preparação** | Dias 1–2 | Ambiente validado, dashboards importados, slides revisados, prompts abertos |
| **Gravação** | Dias 3–12 | 25 vídeos gravados (5 por aula, 8–15 min cada) |
| **Revisão** | Dias 13–14 | Vídeos revisados, regravações pontuais, erros técnicos documentados |
| **Entrega** | Dia 15 | Arquivos nomeados, assets exportados, checklist final assinado |

**Tempo total estimado de gravação:** ~4h30–6h15 (média de 10 min/vídeo) + buffer para regravações.

---

## Cronograma sugerido por dias

| Dia | Atividade | Vídeos | Observação |
|-----|-----------|--------|------------|
| 1 | Preparação do ambiente e importação de dashboards | — | Seguir `checklist-gravacao.md` |
| 2 | Revisão de slides, prompts e roteiro | — | Ler `guia-gravacao.md` e `roteiro-gravacao.md` |
| 3 | Aula 1 — teoria (1.1 a 1.4) | 1.1, 1.2, 1.3, 1.4 | Sem hands-on pesado |
| 4 | Aula 1 — hands-on | 1.5 | Dashboard principal + kubectl |
| 5 | Aula 2 — teoria (2.1 a 2.4) | 2.1, 2.2, 2.3, 2.4 | Slides + menção ao dashboard rightsizing |
| 6 | Aula 2 — hands-on | 2.5 | Dashboard rightsizing + prompt IA |
| 7 | Aula 3 — teoria (3.1 a 3.4) | 3.1, 3.2, 3.3, 3.4 | Preparar `start-anomaly.sh` para o dia seguinte |
| 8 | Aula 3 — hands-on | 3.5 | Anomaly script + dashboard anomalies |
| 9 | Aula 4 — teoria (4.1 a 4.4) | 4.1, 4.2, 4.3, 4.4 | Labels, showback, guardrails |
| 10 | Aula 4 — hands-on | 4.5 | Dashboard governance + OpenCost |
| 11 | Aula 5 — teoria (5.1 a 5.4) | 5.1, 5.2, 5.3, 5.4 | Consolidação + Cost Explorer opcional |
| 12 | Aula 5 — hands-on final | 5.5 | Todos os dashboards + prompt mestre |
| 13 | Revisão de todos os vídeos | — | Anotar regravações em `checklist-gravacao.md` |
| 14 | Regravações pontuais | — | Priorizar hands-on com erro técnico |
| 15 | Entrega final | — | Nomear arquivos, exportar assets |

> Ajuste o ritmo conforme sua disponibilidade. Recomenda-se gravar no máximo 4 vídeos teóricos ou 2 hands-on por sessão.

---

## Lista das 5 aulas

| Aula | Tema | Dashboard | Prompt IA |
|------|------|-----------|-----------|
| 1 | Observabilidade de custos e comportamento operacional | `grafana/dashboards/finops-ai-lab.json` | `ai-prompts/aula-01-observabilidade.md` |
| 2 | Rightsizing e eficiência operacional automatizada | `grafana/dashboards/finops-ai-rightsizing.json` | `ai-prompts/aula-02-rightsizing.md` |
| 3 | Anomalias de custo e capacity planning operacional | `grafana/dashboards/finops-ai-anomalies.json` | `ai-prompts/aula-03-anomalias.md` |
| 4 | Governança operacional e visibilidade de custos | `grafana/dashboards/finops-ai-governance.json` | `ai-prompts/aula-04-governanca.md` |
| 5 | Operações cloud orientadas por eficiência | Todos os dashboards anteriores | `ai-prompts/aula-05-eficiencia.md` |

---

## 25 vídeos — status e dependências

Legenda de dependências: ✅ = necessário | ⬜ = opcional | — = não aplicável

### Aula 1 — Observabilidade de custos e comportamento operacional

| Vídeo | Título | Tempo (min) | Status | Slides | Dashboard | Demo | Prompt IA | Observações |
|-------|--------|-------------|--------|--------|-----------|------|-----------|-------------|
| 1.1 | O desafio da eficiência operacional em cloud | 8–10 | pendente | ✅ | — | — | ✅ | Abertura conceitual; sem demo |
| 1.2 | Entendendo comportamento de consumo em cloud | 10–12 | pendente | ✅ | — | ✅ | ⬜ | `kubectl get ns --show-labels`, `kubectl get deploy -A` |
| 1.3 | Identificando tendências de crescimento operacional | 10–12 | pendente | ✅ | ✅ | ⬜ | ✅ | Mostrar painéis de tendência no Grafana |
| 1.4 | Alertas e visibilidade de custo orientados por contexto | 10–12 | pendente | ✅ | ✅ | ⬜ | ✅ | Conectar Prometheus + Grafana |
| 1.5 | Hands-on — análise operacional de consumo em cloud | 12–15 | pendente | ⬜ | ✅ | ✅ | ✅ | Demo principal da Aula 1 |

### Aula 2 — Rightsizing e eficiência operacional automatizada

| Vídeo | Título | Tempo (min) | Status | Slides | Dashboard | Demo | Prompt IA | Observações |
|-------|--------|-------------|--------|--------|-----------|------|-----------|-------------|
| 2.1 | O impacto do over-provisioning em ambientes modernos | 8–10 | pendente | ✅ | — | — | ✅ | Conceito; citar payments-api |
| 2.2 | Rightsizing baseado em comportamento real de workloads | 10–12 | pendente | ✅ | ✅ | ⬜ | ✅ | Painéis usage vs requests |
| 2.3 | Ajustando recursos com automação operacional | 10–12 | pendente | ✅ | — | ⬜ | ✅ | VPA/HPA como conceito |
| 2.4 | Scheduling inteligente e otimização de workloads | 10–12 | pendente | ✅ | ⬜ | ⬜ | ⬜ | staging-api como exemplo |
| 2.5 | Hands-on — pipeline de rightsizing operacional | 12–15 | pendente | ⬜ | ✅ | ✅ | ✅ | Demo principal da Aula 2 |

### Aula 3 — Anomalias de custo e capacity planning operacional

| Vídeo | Título | Tempo (min) | Status | Slides | Dashboard | Demo | Prompt IA | Observações |
|-------|--------|-------------|--------|--------|-----------|------|-----------|-------------|
| 3.1 | Detectando comportamento anormal de consumo | 8–10 | pendente | ✅ | ✅ | — | ✅ | Explicar baseline vs spike |
| 3.2 | Investigando origem de anomalias operacionais | 10–12 | pendente | ✅ | ✅ | ✅ | ✅ | Preparar `cpu-spike` |
| 3.3 | Planejamento operacional de capacidade | 10–12 | pendente | ✅ | ✅ | ⬜ | ✅ | Painel Capacity Headroom |
| 3.4 | Otimizando uso de recursos em cloud | 10–12 | pendente | ✅ | ⬜ | ⬜ | ⬜ | Conceito; gráficos de slide como exemplo |
| 3.5 | Hands-on — análise de anomalias e capacidade operacional | 12–15 | pendente | ⬜ | ✅ | ✅ | ✅ | `start-anomaly.sh` + `stop-anomaly.sh` |

### Aula 4 — Governança operacional e visibilidade de custos

| Vídeo | Título | Tempo (min) | Status | Slides | Dashboard | Demo | Prompt IA | Observações |
|-------|--------|-------------|--------|--------|-----------|------|-----------|-------------|
| 4.1 | Ownership e responsabilidade sobre consumo cloud | 8–10 | pendente | ✅ | — | ✅ | ✅ | `kubectl get ns --show-labels` |
| 4.2 | Classificação operacional de recursos e ambientes | 10–12 | pendente | ✅ | ✅ | ⬜ | ✅ | Governance Matrix no dashboard |
| 4.3 | Alocação de custos orientada por contexto | 10–12 | pendente | ✅ | ✅ | ✅ | ✅ | Showback proxy + OpenCost |
| 4.4 | Guardrails e políticas de eficiência operacional | 10–12 | pendente | ✅ | ✅ | — | ✅ | Checklist de guardrails |
| 4.5 | Hands-on — dashboard operacional de custos e governança | 12–15 | pendente | ⬜ | ✅ | ✅ | ✅ | OpenCost é ferramenta principal; Cost Explorer opcional |

### Aula 5 — Operações cloud orientadas por eficiência

| Vídeo | Título | Tempo (min) | Status | Slides | Dashboard | Demo | Prompt IA | Observações |
|-------|--------|-------------|--------|--------|-----------|------|-----------|-------------|
| 5.1 | Relacionando custo, performance e observabilidade | 8–10 | pendente | ✅ | ✅ | ⬜ | ✅ | Revisitar dashboards anteriores |
| 5.2 | Tomada de decisão orientada por dados operacionais | 10–12 | pendente | ✅ | — | ⬜ | ✅ | Matriz impacto × esforço |
| 5.3 | Eficiência operacional contínua em ambientes modernos | 10–12 | pendente | ✅ | — | — | ✅ | Plano de 90 dias |
| 5.4 | Construindo uma cultura operacional orientada por eficiência | 10–12 | pendente | ✅ | — | — | ✅ | Fechamento conceitual |
| 5.5 | Hands-on — fluxo operacional completo de FinOps com IA | 12–15 | pendente | ⬜ | ✅ | ✅ | ✅ | Prompt mestre (`aula-05-eficiencia.md`) |

---

## Resumo de progresso

| Métrica | Valor |
|---------|-------|
| Total de vídeos | 25 |
| Vídeos pendentes | 25 |
| Vídeos gravados | 0 |
| Vídeos revisados | 0 |
| Regravações necessárias | 0 |

Atualize esta tabela conforme avançar na gravação.

---

## Documentos de apoio

| Arquivo | Uso |
|---------|-----|
| `docs/guia-gravacao.md` | Preparação técnica, port-forwards, demos por aula |
| `docs/roteiro-gravacao.md` | Roteiro detalhado de cada vídeo |
| `docs/checklist-gravacao.md` | Checklist antes, durante e depois da gravação |
| `docs/assets-gravacao.md` | Screenshots e assets visuais necessários |
| `docs/cronograma-curso.md` | Status geral do conteúdo do curso |
