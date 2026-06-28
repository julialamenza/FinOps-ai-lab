# Notas de fala — Aula 5 (Operações cloud orientadas por eficiência)

Fonte dos slides: `~/Desktop/alura/FinOps-com-IA-aula5.pdf`  
Roteiro operacional: `docs/manual-gravacao-completo.md`

> **Hands-on detalhado:** apenas no **Vídeo 5.5** (slides 9–10). Vídeos 5.1–5.4 são teoria; tour nos dashboards e prompt mestre ficam para o 5.5.

---

## Vídeo 5.1 — Slides 1 a 3 (~8–10 min)

### Slide 1 — Operações Cloud Orientadas por Eficiência
*(~2 min)*

> "Chegamos à **última aula** do curso. Não é só recap — é **consolidar** como observabilidade, FinOps, governança e IA se integram num processo **contínuo** de eficiência operacional.
>
> A IA entra como **copiloto** para tomada de decisão em Kubernetes e cloud — não como substituto do engenheiro.
>
> O lab que usamos do início ao fim: Minikube, Prometheus, Grafana, OpenCost, namespaces `payments`, `users`, `staging`. No vídeo **5.5** rodamos o fluxo completo com o **prompt mestre** e o plano 30-60-90."

---

### Slide 2 — O Que Aprendemos ao Longo do Curso
*(~3 min)*

> "Quatro camadas que construímos, em ordem lógica:
>
> **Aula 1 — Observabilidade:** Prometheus + Grafana + OpenCost para ver consumo e comportamento. Sem visibilidade, FinOps é achismo.
>
> **Aula 2 — Rightsizing:** ajustar requests/limits com **dados reais** — no lab, `payments-api` overprovisionado, `staging-api` subutilizado.
>
> **Aula 3 — Anomalias:** picos de CPU, custo silencioso, capacity planning. O `cpu-spike` e o CronJob `backup-sync` mostraram que anomalia ≠ incidente, mas **sempre merece investigação**.
>
> **Aula 4 — Governança:** labels, showback, guardrails, Cost Explorer + OpenCost. Quem consome, quem paga, quem otimiza.
>
> Cada aula empilha a anterior. Eficiência não é uma ferramenta — é **disciplina operacional**."

---

### Slide 3 — Eficiência Operacional é uma Disciplina, Não um Projeto
*(~3 min)*

> "A maior armadilha: tratar FinOps como **projeto com data de término**. Não tem escopo fechado — quando o custo cai 20%, o trabalho **não acaba**.
>
> Workshops e sprints de otimização ajudam, mas **sem rotina** voltam ao waste. O que funciona:
> - revisões **semanais** com dashboard aberto;
> - alertas configurados, não só gráficos bonitos;
> - decisões baseadas em **dados**, não em reunião trimestral.
>
> Pergunta para a audiência: *vocês têm ritmo fixo de revisão de eficiência — ou só olham a fatura quando assusta?*
>
> No 5.5 montamos o **plano 30-60-90** para sair do curso com ação concreta."

---

## Vídeo 5.2 — Slides 4 a 6 (~10–12 min)

### Slide 4 — O Ciclo da Eficiência
*(~4 min)*

> "Eficiência operacional é um **ciclo de cinco etapas** que se retroalimenta — cada iteração melhora a baseline e a maturidade:
>
> 1. **Observar** — métricas, dashboards, custo alocado (Prometheus, Grafana, OpenCost);
> 2. **Analisar** — waste, anomalias, tendências (rightsizing, capacity);
> 3. **Decidir** — priorizar por impacto × esforço × risco (humano no loop);
> 4. **Agir** — rightsizing, quotas, guardrails, mitigação de anomalia;
> 5. **Medir** — KPIs, antes/depois, showback mensal.
>
> Ritmos diferentes: **diário** — alertas e observação; **semanal** — análise e priorização; **mensal** — governança e capacity planning.
>
> A IA **acelera** observar e analisar — correlaciona métricas em minutos. **Decidir e agir** continuam com o engenheiro. No lab, percorremos esse ciclo inteiro no hands-on 5.5."

---

### Slide 5 — O Papel da IA na Operação Moderna
*(~4 min)*

> "IA **não substitui** o engenheiro — **amplifica** análise e decisão.
>
> **Copiloto:** analisa logs, métricas e custos juntos. Exemplo do slide: `payments` com CPU request **3× acima do P95** — exatamente o que vimos no rightsizing.
>
> **Acelerador:** anomalia que levaria horas para correlacionar (deploy + HPA + custo) vira minutos com contexto colado no prompt.
>
> **Não substitui engenharia:** aplicar rightsizing em serviço crítico, alterar política de quota, escalar cluster — **sempre** julgamento humano de risco e negócio.
>
> Regras que usamos no curso: separar **fato, hipótese, recomendação, risco**; nunca mudança em produção sem **rollback**. O prompt mestre do 5.5 codifica isso."

---

### Slide 6 — Fluxo Operacional Orientado por Dados
*(~3 min)*

> "Decisão eficiente exige **fluxo claro de dados** — cada ferramenta com papel definido:
>
> **Prometheus** → coleta bruta (CPU, memória, kube-state);
> **Grafana** → visualização, alertas, painéis por persona;
> **OpenCost** → tradução em custo por namespace/workload;
> **IA Copiloto** → conecta pontos que dashboard sozinho não revela.
>
> No lab: namespaces `payments`, `users`, `staging`. O cenário `cpu-spike` mostra como anomalia de performance vira **impacto de custo** — e como a IA acelera detecção e resposta.
>
> *Diagrama do slide = arquitetura de referência; demo com os 4 dashboards no 5.5.*"

---

## Vídeo 5.3 — Slide 7 (~10–12 min)

### Slide 7 — Métricas que Realmente Importam
*(~10 min)*

> "Nem toda métrica merece atenção. Foque no que conecta **performance, eficiência e custo**:
>
> 1. **Utilização** — uso real vs requests (CPU/memória);
> 2. **Eficiência** — % provisionado que é efetivamente usado (waste %);
> 3. **Custo** — por namespace, workload, ambiente (OpenCost);
> 4. **Tendência** — crescimento ao longo do tempo (capacity planning);
> 5. **Capacidade** — headroom antes do limite (Pending pods, saturation).
>
> **OpenCost vs Cost Explorer** — complementares:
> - OpenCost → decisões **técnicas** no cluster (rightsizing, alocação interna);
> - Cost Explorer → decisões **financeiras** na conta (budget, executivo).
>
> *Gravação:* lab Minikube — **não abra AWS**. Cost Explorer/Billing = conceito ou screenshot (vídeo 4.4). Ver `docs/aws-billing-gravacao.md`.
>
> Ruído comum: olhar só CPU do cluster sem namespace; olhar só fatura AWS sem workload K8s. No 5.5 cruzamos os quatro dashboards + OpenCost num diagnóstico único."

---

## Vídeo 5.4 — Slide 8 (~10–12 min)

### Slide 8 — Roadmap de Maturidade FinOps
*(~10 min)*

> "Maturidade FinOps evolui em **quatro estágios** — não pule etapas:
>
> **1. Visibilidade** — instrumentação, dashboards, métricas de custo visíveis. *O lab está aqui.*
>
> **2. Otimização** — rightsizing sistemático, eliminação de waste. *Oportunidade crítica em `payments-api`.*
>
> **3. Governança** — budgets, políticas, aprovação de mudanças de capacidade. *Labels ok, faltam quotas e guardrails.*
>
> *AWS Budgets* = exemplo de budget/alerta de fatura em produção — conceitual na gravação (`docs/aws-billing-gravacao.md`).
>
> **4. Automação** — alertas inteligentes, rightsizing contínuo, IA no pipeline. *Meta do plano 90 dias.*
>
> Risco de pular: **chargeback antes de showback**, automação de rightsizing em serviço crítico sem guardrails. Identifique onde sua org está e planeje o **próximo estágio** — o 5.5 gera isso com IA."

---

## Vídeo 5.5 — Slides 9 e 10 (~12–15 min, hands-on)

### Slide 9 — O Copiloto de Eficiência: Prompts e Templates
*(~1–2 min na fala + demo)*

> "Encerramos com **playbook reutilizável**. Três templates do slide:
>
> - **Prompt mestre** — análise cross-namespace, waste, priorização;
> - **Prompt de anomalia** — correlacionar spike com deploy/HPA/custo;
> - **Template semanal** — relatório recorrente para o time.
>
> No curso usamos `./scripts/collect-lab-context.sh` como bloco `[DADOS]`. Você adapta para Prometheus export, OpenCost API ou output de CI."

**Roteiro hands-on (slides 9–10 + lab):**

> **Não abrir AWS** — plano 90 dias menciona budgets/alertas como próximo passo; demo = OpenCost + 4 dashboards.

1. Setup: `./scripts/stop-all-anomalies.sh` + port-forwards + `./scripts/warmup-lab-metrics.sh`
2. **Tour dos 4 dashboards** (Grafana, **Last 15 minutes**, ~1 min cada):
   - `finops-ai-lab.json` — consumo por namespace, Top CPU/Memory Consumers
   - `finops-ai-rightsizing.json` — CPU Waste %, payments alto, staging subutilizado
   - `finops-ai-anomalies.json` — CPU Spike Detector, Capacity Headroom (baseline, sem spike ativo)
   - `finops-ai-governance.json` — Showback View, Governance Matrix, Guardrails Checklist
3. **OpenCost** `http://localhost:9003` — visão consolidada por namespace
4. Terminal: `./scripts/collect-lab-context.sh` + `kubectl top pods -A`
5. Colar no **prompt mestre** (abaixo) + observações dos 4 dashboards
6. Apresentar: diagnóstico, top 3 ações, plano 30-60-90, KPIs, template reutilizável

**Achados esperados para narrar:**
- `payments-api` — overprovisionado (maior waste e showback)
- `users-api` — relativamente eficiente (baseline saudável)
- `staging-api` — subutilizado (candidato a scale-down ou desligamento noturno)
- Anomalias (Aula 3) — lição: alertas + runbook, não só detecção reativa

---

### Slide 10 — Plano de Ação 30-60-90 Dias
*(~2 min fechamento)*

> "Transforme aprendizado em ação — três horizontes:
>
> **30 dias — Quick wins:** OpenCost ativo, dashboards Grafana, top 5 waste, rightsizing inicial em staging, alertas básicos de CPU/custo.
>
> **60 dias — Estrutura:** budgets por namespace, revisão semanal, IA nas anomalias, política de requests/limits, treinar time nos prompts.
>
> **90 dias — Automação:** relatórios semanais com IA, alertas com contexto, pipeline de rightsizing contínuo, ritmo do Ciclo da Eficiência.
>
> **Boas práticas do curso:** requests baseados em P95; observabilidade de custo desde o início; IA copiloto; revisões semanais.
>
> **Erros comuns:** FinOps como projeto; requests sem histórico; ignorar staging/dev; dashboard sem alerta e ação.
>
> Frase de fechamento: *FinOps não é reduzir custo — é maximizar valor por recurso consumido, com visibilidade, disciplina e inteligência.*
>
> Obrigado por acompanhar o FinOps com IA. Salve o prompt mestre como playbook da equipe."

---

## Referência rápida (slide → vídeo)

| Slide | Título | Vídeo | Tempo fala |
|-------|--------|-------|------------|
| 1 | Operações Cloud Orientadas por Eficiência | 5.1 | ~2 min |
| 2 | O Que Aprendemos ao Longo do Curso | 5.1 | ~3 min |
| 3 | Eficiência Operacional é uma Disciplina | 5.1 | ~3 min |
| 4 | O Ciclo da Eficiência | 5.2 | ~4 min |
| 5 | O Papel da IA na Operação Moderna | 5.2 | ~4 min |
| 6 | Fluxo Operacional Orientado por Dados | 5.2 | ~3 min |
| 7 | Métricas que Realmente Importam | 5.3 | ~10 min |
| 8 | Roadmap de Maturidade FinOps | 5.4 | ~10 min |
| 9 | O Copiloto de Eficiência | 5.5 | ~1–2 min + demo |
| 10 | Plano de Ação 30-60-90 Dias | 5.5 | ~2 min + demo |
