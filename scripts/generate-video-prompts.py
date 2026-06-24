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
    ("03", "3.1", "deteccao-anomalia-cpu", "Detecção de anomalia de CPU", False,
     "Dashboard sem spike ativo — baseline. Use dados de exemplo abaixo.",
     """Você é um SRE investigando um spike de CPU no namespace payments.

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
5. Como documentar o incidente em um postmortem leve (template 5 linhas)."""),

    ("03", "3.2", "investigacao-anomalia-cpu", "Investigação de anomalia de CPU (dados ao vivo)", False,
     "Com spike ativo. Rode `./scripts/start-anomaly.sh` e `./scripts/collect-anomaly-context.sh` — cole a saída no lugar dos dados de exemplo.",
     """Você é um SRE investigando um spike de CPU no namespace payments.

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
5. Como documentar o incidente em um postmortem leve (template 5 linhas)."""),

    ("03", "3.3", "capacity-planning", "Capacity planning após incidente", False,
     "Painel Capacity Headroom no dashboard `finops-ai-anomalies.json`.",
     """Após o incidente com cpu-spike no namespace payments, projete capacidade do cluster para os próximos 90 dias.

Estado atual do cluster (Minikube, 4 CPU / 8 Gi RAM):
- Alocação por requests: payments ~2200m, users ~200m, staging ~500m, sistema ~800m
- Uso real médio: payments ~200m, users ~100m, staging ~30m
- Crescimento esperado: users-api +30% tráfego em 90 dias; payments estável; staging pode ganhar novo workload de testes

Responda em português do Brasil:
1. O cluster tem headroom suficiente hoje? Quantifique em CPU e memória.
2. Em que cenário um novo spike como cpu-spike derruba scheduling (Pending pods)?
3. Projeção de uso em 90 dias (tabela por namespace).
4. Recomendações: expandir cluster, quotas por namespace, limitRange, PriorityClass?
5. Quando escalar horizontalmente o node pool vs. rightsizing primeiro?"""),

    ("03", "3.4", "anomalia-silenciosa-staging", "Anomalia silenciosa em staging", False,
     "Com `./scripts/start-staging-anomaly.sh` ativo. Encerre com `./scripts/stop-staging-anomaly.sh`.",
     """O namespace staging não teve spike de CPU, mas o custo alocado subiu 22% na última semana sem deploy novo visível.

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
5. Mensagem para o time platform: tom colaborativo, foco em eficiência."""),

    ("03", "3.5", "runbook-anomalias", "Runbook de resposta a anomalias", False,
     "Hands-on. Cole a saída de `./scripts/collect-anomaly-context.sh` no final do prompt, se disponível.",
     """Crie um runbook operacional para anomalias de custo/consumo no FinOps AI Lab.

Ambiente: Kubernetes, Prometheus, Grafana, OpenCost, namespaces payments/users/staging, script start-anomaly.sh dispara cpu-spike.

Responda em português do Brasil, formato runbook para SRE on-call:
1. Sintomas (o que o alerta ou dashboard mostra).
2. Diagnóstico em 10 minutos (comandos kubectl e queries Prometheus sugeridas).
3. Mitigação imediata (scale down, delete pod, isolate namespace).
4. Comunicação (quem acionar: payments, platform, FinOps).
5. Encerramento e follow-up (ticket, ajuste de alerta, lição aprendida).
6. Seção "Quando NÃO agir" — falsos positivos comuns."""),

    # --- Aula 4 ---
    ("04", "4.1", "auditoria-labels", "Auditoria de labels e ownership", False,
     "Rode `./scripts/collect-lab-context.sh` e substitua a tabela de labels pelos dados reais.",
     """Você é Platform Engineer responsável por governança de custos em Kubernetes.

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
5. Plano de 30 dias para corrigir governança sem bloquear deploys (admission policy gradual)."""),

    ("04", "4.2", "politica-ambientes", "Política de ambientes (prod vs. staging)", False,
     "Painel Governance Matrix no dashboard `finops-ai-governance.json`.",
     """Avalie a governança do ambiente staging frente a payments e users (prod).

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
5. Indicadores para revisar a política trimestralmente."""),

    ("04", "4.3", "showback-chargeback", "Showback vs. chargeback", False,
     "Painel Showback View + OpenCost (`localhost:9003`).",
     """Preciso explicar showback e chargeback para times de produto usando dados do lab.

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
5. Script de 1 minuto para gravar no curso explicando a diferença dos modelos."""),

    ("04", "4.4", "guardrails", "Guardrails sem atrito", False,
     "Painel Guardrails Checklist no dashboard governance.",
     """Proponha guardrails de governança para o cluster FinOps AI Lab.

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
5. Como medir se os guardrails estão funcionando (KPIs em 60 dias)."""),

    ("04", "4.5", "visibilidade-persona", "Visibilidade por persona", False,
     "Hands-on. Rode `./scripts/collect-lab-context.sh` e substitua dados de exemplo, se aplicável.",
     """Desenhe visibilidade de custos para três personas usando payments, users e staging.

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
5. Erros comuns ao expor custo para engenharia (e como evitar)."""),

    # --- Aula 5 ---
    ("05", "5.1", "diagnostico-consolidado", "Diagnóstico consolidado do laboratório", False,
     "Tour rápido nos 4 dashboards. Opcional: `./scripts/collect-lab-context.sh`.",
     """Você é consultor de FinOps e SRE. Faça diagnóstico consolidado do cluster FinOps AI Lab.

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
5. O que monitorar para provar que a eficiência melhorou (KPIs com metas numéricas)."""),

    ("05", "5.2", "priorizacao-matriz", "Priorização por matriz impacto × esforço", False,
     "Conceitual. Resumir achados do lab em tabela antes de colar.",
     """Priorize as ações abaixo usando matriz impacto × esforço × risco.

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
5. Qual ação você faria primeiro se tivesse apenas 1 dia de trabalho?"""),

    ("05", "5.3", "plano-90-dias", "Plano de otimização contínua (90 dias)", False,
     "Sem demo. Slides de eficiência contínua.",
     """Monte um plano de otimização contínua de 90 dias para o FinOps AI Lab, aplicável como modelo em produção real.

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
5. Como evitar regressão (requests voltarem a inflar após 6 meses)."""),

    ("05", "5.4", "recomendacoes-executivas", "Recomendações executivas (CTO / VP Engineering)", False,
     "Sem demo. Slides de cultura FinOps e KPIs.",
     """Transforme a análise técnica do FinOps AI Lab em recomendações executivas.

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
5. Uma métrica norte para acompanhar no board mensal."""),

    ("05", "5.5", "copiloto-eficiencia", "Copiloto de eficiência — prompt mestre", False,
     "Hands-on final. Cole `./scripts/collect-lab-context.sh` na seção `[DADOS]`. Mostre como salvar como template reutilizável.",
     """A partir de agora, atue como meu copiloto de eficiência operacional em Kubernetes e FinOps.

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

[DADOS — cole aqui métricas do Grafana, OpenCost ou kubectl top]"""),
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
