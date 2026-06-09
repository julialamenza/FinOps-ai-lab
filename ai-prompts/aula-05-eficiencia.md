# Aula 5 — Operações cloud orientadas por eficiência

## Objetivo dos prompts

Consolidar análise completa do laboratório, gerar plano de otimização contínua, priorizar ações por impacto e risco, e produzir recomendações executivas para liderança técnica e de produto.

## Como usar na gravação

1. Use este bloco na aula final, após revisar demos das aulas 1–4.
2. Cole o prompt consolidado com todos os dados atualizados do seu cluster.
3. Mostre como a IA acelera o relatório, mas a priorização final é humana.
4. Feche o curso com o plano de 90 dias e os KPIs de acompanhamento.

---

## Prompt 1 — Diagnóstico consolidado do laboratório

```
Você é consultor de FinOps e SRE. Faça diagnóstico consolidado do cluster FinOps AI Lab.

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
5. O que monitorar para provar que a eficiência melhorou (KPIs com metas numéricas).
```

---

## Prompt 2 — Plano de otimização contínua (90 dias)

```
Monte um plano de otimização contínua de 90 dias para o FinOps AI Lab, aplicável como modelo em produção real.

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
5. Como evitar regressão (requests voltarem a inflar após 6 meses).
```

---

## Prompt 3 — Priorização por matriz impacto × esforço

```
Priorize as ações abaixo usando matriz impacto × esforço × risco.

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
5. Qual ação você faria primeiro se tivesse apenas 1 dia de trabalho?
```

---

## Prompt 4 — Recomendações executivas (CTO / VP Engineering)

```
Transforme a análise técnica do FinOps AI Lab em recomendações executivas.

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
5. Uma métrica norte para acompanhar no board mensal.
```

---

## Prompt 5 — Copiloto de eficiência — prompt mestre reutilizável

```
A partir de agora, atue como meu copiloto de eficiência operacional em Kubernetes e FinOps.

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

[DADOS — cole aqui métricas do Grafana, OpenCost ou kubectl top]
```

**Instrução para gravação:** este é o prompt mestre do curso. Mostre como salvá-lo como template e reutilizá-lo no dia a dia, substituindo apenas a seção `[DADOS]` ao final.
