# Aula 4 — Governança operacional e visibilidade de custos

## Objetivo dos prompts

Avaliar qualidade de labels, ownership, cost-center, environment, modelos de showback/chargeback e guardrails para manter visibilidade de custo sem travar a velocidade dos times.

## Como usar na gravação

1. Rode `kubectl get ns --show-labels` e mostre os labels na tela.
2. Cole o prompt escolhido e substitua labels ou gaps reais que encontrar no cluster.
3. Use a resposta para discutir showback vs. chargeback e políticas de namespace.
4. Conecte com o dashboard Grafana filtrado por label `team` ou `environment`.

---

## Prompt 1 — Auditoria de labels e ownership

```
Você é Platform Engineer responsável por governança de custos em Kubernetes.

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
5. Plano de 30 dias para corrigir governança sem bloquear deploys (admission policy gradual).
```

---

## Prompt 2 — Showback vs. chargeback

```
Preciso explicar showback e chargeback para times de produto usando dados do lab.

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
5. Script de 1 minuto para gravar no curso explicando a diferença dos modelos.
```

---

## Prompt 3 — Guardrails sem atrito

```
Proponha guardrails de governança para o cluster FinOps AI Lab.

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
5. Como medir se os guardrails estão funcionando (KPIs em 60 dias).
```

---

## Prompt 4 — Visibilidade por persona

```
Desenhe visibilidade de custos para três personas usando payments, users e staging.

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
5. Erros comuns ao expor custo para engenharia (e como evitar).
```

---

## Prompt 5 — Política de ambientes (prod vs. staging)

```
Avalie a governança do ambiente staging frente a payments e users (prod).

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
5. Indicadores para revisar a política trimestralmente.
```
