# Notas de fala — Aula 4 (Governança operacional e visibilidade de custos)

Fonte dos slides: `~/Desktop/alura/FinOps-com-IA-aula4.pdf`  
Roteiro operacional: `docs/manual-gravacao-completo.md`

> **Hands-on detalhado:** apenas no **Vídeo 4.5** (slides 9–10). Vídeos 4.1–4.4 são teoria; demo ao vivo fica para o 4.5.

---

## Vídeo 4.1 — Slides 1 a 3 (~8–10 min)

### Slide 1 — Governança Operacional e Visibilidade de Custos
*(~2 min)*

> "Nas aulas anteriores vimos **como o cluster consome**, **como rightsizar** e **como detectar anomalias**. Agora fechamos o ciclo com **governança**: quem é dono de cada recurso, como alocar custo por time e como criar **accountability financeiro** sem virar burocracia.
>
> Nesta aula você vai estruturar **labels**, entender **showback vs chargeback**, usar **OpenCost** na prática e definir **guardrails** que previnem desperdício antes da fatura chegar.
>
> O lab continua o mesmo: Minikube, Prometheus, Grafana, OpenCost — namespaces `payments`, `users` e `staging`. No vídeo 4.5 colocamos tudo isso na tela com dados reais."

---

### Slide 2 — Por Que Observabilidade Sozinha Não É Suficiente?
*(~3 min)*

> "Observabilidade responde **como o sistema se comporta** — latência, throughput, logs, alertas de saúde. Isso é essencial para SRE, mas **não responde quanto custa cada serviço, time ou workload**.
>
> Do lado esquerdo do slide: o que já temos — métricas, traces, detecção de incidentes. Do lado direito: o que **ainda falta** — quanto custa cada namespace? Qual time é responsável? Onde está o desperdício? Como priorizar otimização por **impacto financeiro**?
>
> O ponto central: **Observabilidade + FinOps = decisões orientadas por dados técnicos e financeiros**. Rightsizing sem governança vira economia técnica que ninguém mede. Anomalia sem ownership vira spike que ninguém paga.
>
> Pergunta para a audiência: *vocês conseguem dizer hoje qual squad consome mais CPU no cluster — e quanto isso representa em reais?*"

---

### Slide 3 — O Desafio da Atribuição de Custos em Kubernetes
*(~3 min)*

> "Em cluster **compartilhado**, vários times consomem recursos sem visibilidade clara de **quem paga o quê**. A granularidade do problema exige **estrutura antes de ferramenta**.
>
> Três desafios que se retroalimentam:
> 1. **Recursos compartilhados** — node pool, control plane, storage: custo diluído entre todos;
> 2. **Escala dinâmica** — HPA, pods efêmeros, CronJobs: consumo muda rápido e some da memória do time;
> 3. **Ownership difuso** — namespace sem label, workload órfão, staging 'de todo mundo'.
>
> Sem ownership definido → custos invisíveis → ninguém otimiza. A solução começa com **labels padronizadas** e **políticas de governança** — não com mais um dashboard genérico.
>
> No nosso lab, `staging` com `team=platform` é exemplo clássico: quem paga engineering ou product? Isso aparece no hands-on 4.5."

---

## Vídeo 4.2 — Slides 4 a 6 (~10–12 min)

### Slide 4 — Labels como Fundação da Governança
*(~4 min)*

> "Labels Kubernetes são o **mecanismo primário** de rastreabilidade de custos. Aplicadas com consistência, transformam recurso técnico em dado financeiro acionável.
>
> Padrão mínimo FinOps:
> - **`team`** — quem opera (payments, users, platform);
> - **`environment`** — prod, staging, dev;
> - **`cost-center`** — centro de custo financeiro;
> - **`owner`** — responsável técnico (email ou grupo);
> - **`service-tier`** — critical, standard, best-effort.
>
> O exemplo do slide usa `kubectl label namespace` — no lab os namespaces já vêm rotulados, mas **faltam** `owner` e `service-tier` em vários recursos. Isso é gap de maturidade que a IA vai auditar no 4.5.
>
> Regra: **padronize antes de implantar workloads** — corrigir label retroativa em produção é 10× mais caro."

---

### Slide 5 — Ownership, Accountability e Modelos de Custeio
*(~4 min)*

> "Três perguntas que toda organização FinOps precisa responder:
> 1. **Quem consome?** — identificado via `team` e `owner`;
> 2. **Quem paga?** — mapeado via `cost-center`;
> 3. **Quem otimiza?** — engenheiro/SRE com contexto técnico, sem quebrar SLO.
>
> Modelos de custeio:
> - **Showback** — mostra custo por time, **sem cobrança real**. Ideal para fase inicial: cria cultura e visibilidade.
> - **Chargeback** — cobra efetivamente do time. Exige maturidade, confiança nos números e processo financeiro.
> - **Hybrid** — showback interno + chargeback para BUs externas.
>
> Recomendação do slide — e a nossa no curso: **comece com showback**. No lab, o Grafana `finops-ai-governance.json` tem painel **Showback View** como proxy didático; custo real vem do OpenCost no hands-on.
>
> *Gráficos de distribuição de custo no deck são ilustrativos — no 4.5 comparamos com dados ao vivo.*"

---

### Slide 6 — OpenCost na Prática
*(~3 min)*

> "OpenCost é o padrão CNCF para **alocação de custos em Kubernetes**. Integrado ao Prometheus, traduz consumo em valor monetário por namespace, workload e label — **sem depender de API específica de cloud**.
>
> Fluxo em quatro etapas: **Coleta** (métricas kube/cAdvisor) → **Normalização** (preços AWS/Azure/GCP) → **Alocação** (por namespace/label) → **Exposição** (UI e API).
>
> Com OpenCost no cluster você responde: quanto custa o `payments-api`? Qual namespace tem maior custo por requisição? Onde há recursos ociosos?
>
> No lab instalamos com `./scripts/install-opencost.sh` e acessamos via port-forward na porta **9003**. Demo completa no vídeo **4.5** — aqui é conceitual."

---

## Vídeo 4.3 — Slide 7 (~10–12 min)

### Slide 7 — Visibilidade para Diferentes Personas
*(~10 min)*

> "Dashboard genérico gera **ruído**. Personas diferentes precisam de **cortes diferentes** dos mesmos dados.
>
> **SRE / Platform Engineer:** custo por workload, eficiência requests/limits, recursos ociosos, alertas de anomalia de consumo. Pergunta: *onde está o waste agora?*
>
> **FinOps Analyst:** custo por cost-center, tendências mensais, budget vs actual, relatório de showback por squad. Pergunta: *quem está acima do budget?*
>
> **Engineering Manager:** custo por produto, eficiência relativa entre times, impacto de decisões arquiteturais. Pergunta: *vale a pena priorizar eficiência este sprint?*
>
> **Liderança executiva:** visão consolidada cloud, eficiência por BU, ROI de otimização. Pergunta: *cloud está crescendo mais rápido que receita?*
>
> No lab, o dashboard `finops-ai-governance.json` cobre SRE e FinOps; OpenCost complementa. No 4.5 montamos a 'view' de cada persona com os mesmos dados.
>
> Erro comum: mostrar fatura AWS crua para o EM — assusta sem dar alavanca de ação."

---

## Vídeo 4.4 — Slide 8 (~10–12 min)

### Slide 8 — AWS Cost Explorer + OpenCost: Visões Complementares
*(~10 min)*

> "Nenhuma ferramenta sozinha fecha o ciclo. **Cost Explorer** = camada **infra cloud**; **OpenCost** = camada **aplicação Kubernetes**.
>
> **Cost Explorer:** serviços AWS (EC2, EKS, RDS, S3), allocation tags, RIs/Savings Plans, forecast por conta. Granularidade: conta → serviço → tag.
>
> **OpenCost:** namespace, workload, pod, labels K8s, custo por requisição, subutilização. Granularidade: cluster → namespace → pod.
>
> Caso de uso do slide: Cost Explorer mostra EKS +30%. OpenCost revela que **`staging-api` consome ~40% dos recursos sem tráfego real** — aí você rightsiza ou escala para zero, não compra node às cegas.
>
> No Minikube local, OpenCost usa **preços públicos AWS** como estimativa — didático, não é fatura real. Opcional: screenshot do Cost Explorer para contrastar.
>
> Cruzamento prático: `custo_namespace = custo_cluster × (requests_namespace / requests_total)` — fórmula no painel Showback do Grafana."

---

## Vídeo 4.5 — Slides 9 e 10 (~12–15 min, hands-on)

### Slide 9 — Guardrails Operacionais: Governança sem Burocracia
*(~1–2 min na fala + demo)*

> "Governança não é trava de deploy — é **prevenir problema antes do custo**. Quatro guardrails do slide:
>
> 1. **ResourceQuota** por namespace — teto de CPU/memória/pods;
> 2. **LimitRange** — defaults para containers sem limits;
> 3. **Labels obrigatórias** via admission webhook;
> 4. **Kyverno/OPA** — políticas como código.
>
> No lab, abra o painel **Guardrails Checklist** no Grafana e rode `kubectl get resourcequota,limitrange -A` — vai ver **gaps reais** (sem quota no staging). Isso alimenta o Prompt C da IA."

**Roteiro hands-on (slides 9–10 + lab):**

1. Setup: `./scripts/stop-all-anomalies.sh` + port-forwards Grafana (3000) e OpenCost (9003)
2. Terminal: `kubectl get ns --show-labels` → comparar com **Governance Matrix**
3. Terminal: `kubectl get resourcequota -A` e `kubectl get limitrange -A` → **Guardrails Checklist**
4. Grafana `finops-ai-governance.json`, **Last 15 minutes**:
   - **Resource Overview** — CPU/Memory Usage e Requests by Namespace
   - **Governance & Labels** — Label Coverage + Governance Matrix
   - **Cost Visibility** — Showback View + Nota didática
   - **Guardrails & Tooling** — Checklist + OpenCost vs Cost Explorer
5. OpenCost `http://localhost:9003` — alocação payments > users > staging
6. `./scripts/collect-lab-context.sh` → colar nos prompts A, B, C
7. Comentar respostas da IA (Prompt A = slides 4–6, B = slide 7, C = slide 9)

---

### Slide 10 — Laboratório Prático: payments, users e staging
*(~2 min fechamento)*

> "Três namespaces no lab:
> - **`payments-api`** — produção, crítico, overprovisionado (maior fatia de showback);
> - **`users-api`** — produção, standard, relativamente eficiente;
> - **`staging-api`** — staging, best-effort, subutilizado (~33% do custo no exemplo do slide — desperdício clássico).
>
> Oportunidades do slide: staging com requests de produção, réplicas ociosas fora do horário comercial, containers sem limits no users-api.
>
> *Gráfico de barras USD/mês é ilustrativo — no Grafana usamos proxy por requests; no OpenCost, estimativa monetária.*
>
> Você viu labels, showback, personas, guardrails e OpenCost com dados reais. Na **Aula 5** consolidamos tudo no **copiloto de eficiência** e plano 30-60-90."

---

## Referência rápida (slide → vídeo)

| Slide | Título | Vídeo | Tempo fala |
|-------|--------|-------|------------|
| 1 | Governança Operacional e Visibilidade de Custos | 4.1 | ~2 min |
| 2 | Por Que Observabilidade Sozinha Não É Suficiente? | 4.1 | ~3 min |
| 3 | O Desafio da Atribuição de Custos em Kubernetes | 4.1 | ~3 min |
| 4 | Labels como Fundação da Governança | 4.2 | ~4 min |
| 5 | Ownership, Accountability e Modelos de Custeio | 4.2 | ~4 min |
| 6 | OpenCost na Prática | 4.2 | ~3 min |
| 7 | Visibilidade para Diferentes Personas | 4.3 | ~10 min |
| 8 | AWS Cost Explorer + OpenCost | 4.4 | ~10 min |
| 9 | Guardrails Operacionais | 4.5 | ~1–2 min + demo |
| 10 | Laboratório Prático | 4.5 | ~2 min + demo |
