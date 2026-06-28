#!/usr/bin/env python3
"""Generate per-video prompt files from embedded definitions."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "ai-prompts"

# (aula, video, slug, title, optional, before, prompt)
VIDEOS = [
    # --- Aula 1 ---
    ("01", "1.1", "narrativa-abertura", "Narrativa para abertura da aula", False,
     "Sem demo. Prompt curto — não precisa de dados do cluster.",
     """Estou gravando a aula 1 de um curso "FinOps com IA" para público de SRE, DevOps e Platform Engineers.

Contexto do lab: Minikube com workloads simulados (payments-api overprovisionado, users-api saudável, staging-api subutilizado).

Escreva em português do Brasil:
1. Um parágrafo de abertura (30–40 segundos de fala) sobre por que observabilidade operacional precede otimização de custo.
2. Três analogias simples para explicar a diferença entre "custo na fatura" e "comportamento de consumo".
3. Uma pergunta provocativa para engajar a audiência antes da primeira demo com kubectl/Grafana."""),

    ("01", "1.2", "desperdicios-operacionais", "Desperdícios operacionais em ambientes distribuídos", True,
     "Opcional. Complementa slides + `kubectl get ns --show-labels` e `kubectl get deploy -A`.",
     """Analise este cenário de cloud Kubernetes com múltiplos namespaces e explique onde podem surgir desperdícios operacionais — mesmo sem fatura AWS visível ainda.

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
4. Proponha um checklist semanal de revisão operacional."""),

    ("01", "1.3", "padroes-sazonalidade", "Padrões de uso e sazonalidade", False,
     "Slides + Grafana (`finops-ai-lab.json`, Last 15 minutes). Rode `./scripts/start-business-hours-load.sh` 2 min antes e comente no vídeo o que os gráficos mostram. Os números abaixo são **ilustrativos**, alinhados ao comportamento dos geradores de carga do lab — em produção você usaria 7–30 dias de histórico.",
     """Atue como Platform Engineer. Com base nos padrões abaixo, explique o comportamento de uso e o que isso implica para planejamento de capacidade e custo.

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
4. Que alertas configuraria para evitar surpresa operacional?"""),

    ("01", "1.4", "metricas-essenciais", "Métricas essenciais para FinOps em Kubernetes", False,
     "Slides + menção Prometheus/Grafana. Gráficos de slide como exemplo conceitual.",
     """Sou Cloud Engineer montando observabilidade FinOps em um cluster Kubernetes (Prometheus + Grafana + OpenCost). Os namespaces são payments, users e staging.

Quero uma lista prática de métricas e painéis, não teoria genérica.

Responda em português do Brasil:
1. Quais 8 métricas Prometheus são indispensáveis para correlacionar uso, requests/limits e custo?
2. Para cada métrica, diga o que ela revela e um exemplo de query ou nome de série. 
3. Como organizar dashboards por persona: SRE (operação), FinOps (custo), Engineering Manager (produtividade)?
4. Que dados do OpenCost devo cruzar com métricas de utilização do kube-state-metrics/cAdvisor?
5. Sugira um painel mínimo viável para a primeira demo do curso."""),

    ("01", "1.5", "panorama-consumo", "Panorama de consumo por namespace", False,
     "Hands-on. Rode `./scripts/collect-lab-context.sh` e cole a saída no lugar dos dados de exemplo.",
     """Você é um SRE especialista em FinOps e Kubernetes. Analise o consumo operacional do cluster abaixo e identifique onde há desperdício, subutilização ou risco de saturação.

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
4. Que perguntas você faria ao time dono de cada workload?"""),

    # --- Aula 2 ---
    ("02", "2.1", "business-case-em", "Business case para Engineering Manager", False,
     "Sem demo. Citar `payments-api` como exemplo do lab.",
     """Preciso traduzir uma otimização técnica de rightsizing em linguagem de negócio.

Dados:
- payments-api: economia estimada de 85% nos requests de CPU e 75% em memória após ajuste
- staging-api: economia adicional se desligado 12h/dia nos fins de semana
- users-api: já eficiente, sem ação imediata
- Esforço: 2 dias de engenharia + 1 semana de observação

Responda em português do Brasil:
1. Resumo executivo em 5 linhas para um Engineering Manager.
2. Tabela impacto vs. esforço vs. risco para as três iniciativas.
3. KPIs para medir sucesso após 30 dias (utilização, incidentes, custo alocado).
4. Uma frase de "por que agora" conectando eficiência operacional e margem do produto."""),

    ("02", "2.2", "rightsizing-payments-api", "Rightsizing baseado em comportamento real de workloads", False,
     "Sem demo. Slides 4–6. Citar `payments-api` com os dados do prompt (gap request vs uso). Demo no Grafana fica para o vídeo 2.5.",
     """Estou gravando o vídeo 2.2 (slides 4–6: rightsizing por comportamento real, margem de segurança, Usage vs Requests).

Contexto do lab: deployment payments-api (namespace payments), serviço crítico, overprovisionado.

Dados de referência (7 dias, por pod, 2 réplicas):
- Requests: CPU 1000m, Memória 1 Gi | Limits: CPU 1500m, Memória 2 Gi
- Uso: CPU média 72m, P95 95m, pico 120m | Memória média 88 Mi, P95 110 Mi, pico 125 Mi

Responda em português do Brasil para complementar os slides (ainda sem executar mudanças):
1. Explique o gap entre requests e uso real — CPU e memória — para um Platform Engineer.
2. Por que usar P95 (e não só a média) como base para rightsizing?
3. O que é margem de segurança operacional (~30% acima do P95) e por que não eliminar o gap de uma vez?
4. Diferença prática entre Usage vs Requests no Kubernetes (scheduling, custo alocável, throttling).
5. Este workload é candidato a rightsizing? Justifique em 3 bullet points."""),

    ("02", "2.3", "automacao-vpa", "Ajustando recursos com automação operacional", False,
     "Sem demo. Slide 7 — VPA e recomendações automatizadas. Demo com terminal e dashboard fica para o vídeo 2.5.",
     """Estou gravando o vídeo 2.3 (slide 7 — VPA e recomendações automatizadas) no FinOps AI Lab.

Workloads: payments-api (crítico, overprovisionado), users-api (saudável), staging-api (subutilizado).
Requests definidos manualmente no YAML; métricas reais via Prometheus.

Responda em português do Brasil:
1. O que o VPA (Vertical Pod Autoscaler) faz e quais modos existem (Off, Initial, Recreation, Auto)?
2. Quando VPA é adequado vs. recomendações manuais assistidas por IA?
3. Para payments-api (crítico): recomendaria VPA em produção? Por quê?
4. Para users-api e staging-api: mesma abordagem ou diferente?
5. Três riscos de ativar VPA sem guardrails em serviço de pagamentos."""),

    ("02", "2.4", "rollout-hpa-vpa", "HPA, VPA e rollout gradual", True,
     "Opcional. Slide 8 — rollout gradual no `payments-api`. Sem demo.",
     """Estou gravando o vídeo 2.4 (slide 8 — HPA, VPA e rollout gradual).

Contexto: ajuste proposto no payments-api (crítico, 2 réplicas) — reduzir CPU request de 1000m para ~125m e memória de 1 Gi para ~150 Mi, com margem sobre P95 observado.

Responda em português do Brasil:
1. Diferença entre HPA (escala horizontal) e VPA (escala vertical) — quando cada um entra no rightsizing?
2. Por que rightsizing em serviço crítico exige rollout gradual (não big bang)?
3. Plano de rollout em 4 passos para payments-api (ordem, réplicas, monitoração, rollback).
4. Métricas e alertas para monitorar nas primeiras 48h após o ajuste.
5. Em que cenário o HPA entraria depois do rightsizing — ou competiria com o VPA?"""),

    ("02", "2.5", "rightsizing-hands-on", "Rightsizing — hands-on (payments + comparativo)", False,
     "Hands-on. Slides 9–10. Rode `./scripts/collect-lab-context.sh` e cole a saída no bloco abaixo. Percorra o Grafana (`finops-ai-rightsizing.json`, Last 15 minutes) antes dos prompts A, B e C.",
     """## Contexto ao vivo

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
4. Checklist de validação antes de merge do PR de rightsizing."""),

    # --- Aula 3 ---
    ("03", "3.1", "deteccao-anomalia-cpu", "Fundamentos de anomalias operacionais", False,
     "Sem demo. Slides 1–3. Citar `cpu-spike` como exemplo do lab. Demo no Grafana e terminal fica para o vídeo 3.5.",
     """Estou gravando o vídeo 3.1 (slides 1–3: o que é anomalia operacional, incidente vs. anomalia) no FinOps AI Lab.

Contexto: cluster Minikube com namespaces payments, users e staging. O workload cpu-spike simula anomalia de CPU no namespace payments.

Responda em português do Brasil:
1. Definição de anomalia operacional em FinOps/Kubernetes (CPU, memória, custo).
2. Diferença prática entre anomalia e incidente — com exemplos do lab.
3. O que é baseline e como detectar desvio estatisticamente significativo.
4. Por que nem toda anomalia vira incidente — e por que toda anomalia de custo merece investigação.
5. Uma pergunta provocativa para a audiência antes do hands-on (vídeo 3.5)."""),

    ("03", "3.2", "investigacao-anomalia-cpu", "Detecção, investigação e correlação de anomalias", False,
     "Sem demo. Slides 4–6. Use os dados de exemplo abaixo. Demo ao vivo fica para o vídeo 3.5.",
     """Estou gravando o vídeo 3.2 (slides 4–6: detecção, investigação de spikes, correlação com mudanças).

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
5. Checklist de triagem em 10 minutos (kubectl, métricas, change calendar)."""),

    ("03", "3.3", "capacity-planning", "Capacity planning baseado em histórico", False,
     "Sem demo. Slide 7 — Capacity Planning Baseado em Histórico. Painel Capacity Headroom no Grafana fica para o vídeo 3.5.",
     """Estou gravando o vídeo 3.3 (slide 7 — Capacity Planning Baseado em Histórico).

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
5. Quando escalar node pool vs. rightsizing primeiro?"""),

    ("03", "3.4", "anomalia-silenciosa-staging", "Uso de IA para investigação e projeções", False,
     "Sem demo. Slide 8 — Uso de IA para Investigação e Projeções. Demo com `collect-anomaly-context.sh` fica para o vídeo 3.5.",
     """Estou gravando o vídeo 3.4 (slide 8 — Uso de IA para Investigação e Projeções) no FinOps AI Lab.

Contexto: após detectar anomalias de CPU (cpu-spike) e de custo silencioso (CronJob backup-sync em staging), quero usar IA como copiloto.

Responda em português do Brasil:
1. Como a IA acelera investigação de anomalias vs. análise manual (3 casos de uso concretos).
2. Que dados colar no prompt para a IA ser útil (métricas, timeline, kubectl output)?
3. Como a IA ajuda em projeções de capacidade e custo — limites e cuidados.
4. Riscos de confiar cegamente na IA em incidentes operacionais.
5. Template de prompt reutilizável para investigação de anomalia (5 linhas)."""),

    ("03", "3.5", "runbook-anomalias", "Hands-on — anomalias e capacity planning operacional", False,
     "Hands-on. Slides 9–10. Rode `./scripts/collect-anomaly-context.sh` e cole a saída no bloco abaixo. Percorra o Grafana (`finops-ai-anomalies.json`, Last 15 minutes) antes dos prompts A, B e C.",
     """## Contexto ao vivo

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
6. Seção "Quando NÃO agir" — falsos positivos comuns."""),

    # --- Aula 4 ---
    ("04", "4.1", "auditoria-labels", "Por que governança de custos em Kubernetes", False,
     "Sem demo. Slides 1–3. Demo com labels e OpenCost fica para o vídeo 4.5.",
     """Estou gravando o vídeo 4.1 (slides 1–3: governança, limites da observabilidade, atribuição de custos).

Contexto: cluster Kubernetes compartilhado (payments, users, staging) com Prometheus, Grafana e OpenCost.

Responda em português do Brasil:
1. Por que observabilidade sozinha não responde "quanto custa cada time/workload"?
2. Três desafios de atribuição de custo em clusters Kubernetes compartilhados.
3. Diferença entre visibilidade técnica e accountability financeira.
4. O que muda na operação quando existe governança de custos estruturada.
5. Pergunta provocativa para engajar a audiência antes do hands-on (vídeo 4.5)."""),

    ("04", "4.2", "politica-ambientes", "Labels, ownership e OpenCost na prática", False,
     "Sem demo. Slides 4–6. Use a tabela de labels abaixo. Demo no Grafana/OpenCost fica para o vídeo 4.5.",
     """Estou gravando o vídeo 4.2 (slides 4–6: labels, ownership, OpenCost).

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
5. Plano de 30 dias para corrigir governança sem bloquear deploys."""),

    ("04", "4.3", "showback-chargeback", "Visibilidade para diferentes personas", False,
     "Sem demo. Slide 7 — Visibilidade para Diferentes Personas. Demo no Grafana fica para o vídeo 4.5.",
     """Estou gravando o vídeo 4.3 (slide 7 — Visibilidade para Diferentes Personas).

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
5. Erros comuns ao expor custo para engenharia."""),

    ("04", "4.4", "guardrails", "AWS Cost Explorer e OpenCost — visões complementares", False,
     "Sem demo. Slide 8 — Cost Explorer/Billing/Budgets complementam OpenCost. Lab Minikube — não precisa EKS. Ver docs/aws-billing-gravacao.md. Demo OpenCost ao vivo fica para 4.5.",
     """Estou gravando o vídeo 4.4 (slide 8 — AWS Cost Explorer + OpenCost: Visões Complementares).

Contexto de gravação:
- Lab local Minikube — NÃO tenho EKS nem cluster Kubernetes na AWS
- OpenCost no lab usa preços públicos AWS como estimativa (não é fatura real)
- Cost Explorer/Billing/Budgets serão explicados como camada cloud em produção

Responda em português do Brasil:
1. O que cada ferramenta responde que a outra não responde (Cost Explorer, Billing, Budgets, OpenCost).
2. Como cruzar fatura AWS com alocação por namespace no OpenCost — mesmo sem EKS na conta.
3. Cenário didático: custo AWS subiu 10% — onde investigar primeiro (Billing → Cost Explorer → OpenCost)?
4. Diferença entre alerta de billing (AWS Budgets) e alerta técnico (Grafana/Prometheus).
5. Script de 1 minuto para gravar explicando as visões complementares — lab Minikube, sem demo AWS obrigatória."""),

    ("04", "4.5", "visibilidade-persona", "Hands-on — governança e visibilidade de custos", False,
     "Hands-on. Slides 9–10. Rode `./scripts/collect-lab-context.sh` e cole a saída no bloco abaixo. Percorra Grafana (`finops-ai-governance.json`) e OpenCost antes dos prompts A, B e C.",
     """## Contexto ao vivo

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
5. KPIs para medir eficácia em 60 dias."""),

    # --- Aula 5 ---
    ("05", "5.1", "diagnostico-consolidado", "Revisão do curso e mentalidade de eficiência", False,
     "Sem demo. Slides 1–3. Recapitular achados das aulas 1–4. Tour nos dashboards fica para o vídeo 5.5.",
     """Estou gravando o vídeo 5.1 (slides 1–3: revisão do curso e eficiência como disciplina).

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
5. Pergunta provocativa antes do hands-on final (vídeo 5.5)."""),

    ("05", "5.2", "priorizacao-matriz", "Ciclo da eficiência e IA na operação", False,
     "Sem demo. Slides 4–6. Conceitual — ciclo, IA e fluxo orientado por dados.",
     """Estou gravando o vídeo 5.2 (slides 4–6: ciclo da eficiência, IA na operação, fluxo orientado por dados).

Stack: Minikube, Prometheus, Grafana, OpenCost, IA como copiloto.

Responda em português do Brasil:
1. Descreva o ciclo de eficiência em 5 etapas (observar → agir → medir).
2. Papel da IA como copiloto — o que amplifica vs. o que não substitui.
3. Fluxo operacional orientado por dados: Prometheus → Grafana → OpenCost → IA → ação.
4. Onde humanos devem manter aprovação obrigatória (ex.: rightsizing em payments).
5. Exemplo de decisão que atravessa todo o ciclo no FinOps AI Lab."""),

    ("05", "5.3", "plano-90-dias", "Métricas que realmente importam", False,
     "Sem demo. Slide 7 — Métricas que Realmente Importam.",
     """Estou gravando o vídeo 5.3 (slide 7 — Métricas que Realmente Importam).

Contexto: operação Kubernetes com FinOps — payments (crítico, overprovisionado), users (saudável), staging (subutilizado).

Responda em português do Brasil:
1. As 5 métricas essenciais que conectam performance, eficiência e custo.
2. Para cada métrica: o que revela, fonte (Prometheus/OpenCost), exemplo de query.
3. Métricas que parecem importantes mas geram ruído — evite.
4. KPIs por persona: SRE, FinOps, Engineering Manager (1 KPI cada).
5. Dashboard mínimo viável para review semanal de eficiência."""),

    ("05", "5.4", "recomendacoes-executivas", "Roadmap de maturidade FinOps", False,
     "Sem demo. Slide 8 — Roadmap de Maturidade FinOps.",
     """Estou gravando o vídeo 5.4 (slide 8 — Roadmap de Maturidade FinOps).

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
5. Próximo marco recomendado para o lab em 90 dias."""),

    ("05", "5.5", "copiloto-eficiencia", "Hands-on — copiloto de eficiência e plano 30-60-90", False,
     "Hands-on final. Slides 9–10. Cole `./scripts/collect-lab-context.sh` na seção `[DADOS]`. Percorra os 4 dashboards Grafana e OpenCost antes de colar.",
     """A partir de agora, atue como meu copiloto de eficiência operacional em Kubernetes e FinOps.

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

## 5. Template de prompt reutilizável (slide 9) — salve como playbook da equipe"""),
]

AULA_TITLES = {
    "01": "Observabilidade de custos e comportamento operacional",
    "02": "Rightsizing e eficiência operacional automatizada",
    "03": "Anomalias de custo e capacity planning operacional",
    "04": "Governança operacional e visibilidade de custos",
    "05": "Operações cloud orientadas por eficiência",
}

AULA_DASHBOARDS = {
    "01": "`grafana/dashboards/finops-ai-lab.json`",
    "02": "`grafana/dashboards/finops-ai-rightsizing.json`",
    "03": "`grafana/dashboards/finops-ai-anomalies.json`",
    "04": "`grafana/dashboards/finops-ai-governance.json`",
    "05": "Todos os dashboards anteriores",
}


def render(aula, video, slug, title, optional, before, prompt):
    opt = " *(opcional)*" if optional else ""
    return f"""# Vídeo {video} — {title}{opt}

**Aula {int(aula)}** — {AULA_TITLES[aula]}  
**Roteiro:** `docs/manual-gravacao-completo.md` → Vídeo {video}  
**Dashboard:** {AULA_DASHBOARDS[aula]}

## Antes de colar

{before}

## Prompt

```
{prompt.strip()}
```
"""


def write_aula_readme(aula: str):
    folder = ROOT / f"aula-{aula}"
    rows = []
    for v in VIDEOS:
        if v[0] != aula:
            continue
        _, video, slug, title, optional, _, _ = v
        opt = " *(opcional)*" if optional else ""
        rows.append(f"| {video} | `{video}-{slug}.md` | {title}{opt} |")

    content = f"""# Aula {int(aula)} — {AULA_TITLES[aula]}

Prompts organizados **um por vídeo**. Abra o arquivo do vídeo que está gravando.

| Vídeo | Arquivo | Tema |
|-------|---------|------|
{chr(10).join(rows)}
"""
    (folder / "README.md").write_text(content, encoding="utf-8")


def main():
    for aula, video, slug, title, optional, before, prompt in VIDEOS:
        folder = ROOT / f"aula-{aula}"
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / f"{video}-{slug}.md"
        path.write_text(render(aula, video, slug, title, optional, before, prompt), encoding="utf-8")
        print(f"Wrote {path.relative_to(ROOT.parent)}")

    for aula in AULA_TITLES:
        write_aula_readme(aula)
        print(f"Wrote ai-prompts/aula-{aula}/README.md")

    print(f"\nTotal: {len(VIDEOS)} prompt files")


if __name__ == "__main__":
    main()
