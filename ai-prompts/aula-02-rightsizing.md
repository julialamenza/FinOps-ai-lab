# Aula 2 — Rightsizing e eficiência operacional automatizada

## Objetivo dos prompts

Gerar recomendações de requests/limits com base em CPU e memória (média e P95), avaliar risco operacional de cada mudança e priorizar otimizações por impacto financeiro e esforço de implementação.

## Como usar na gravação

O lab é montado na hora — use intervalo **Last 15 minutes** no dashboard `finops-ai-rightsizing.json`.

1. Rode `./scripts/collect-lab-context.sh` para obter requests/limits e consumo ao vivo
2. Copie o prompt que combina com o workload em discussão (`payments-api` é o caso principal de over-provisioning)
3. Cole a saída do script no prompt ou substitua os valores de exemplo
4. Peça à IA que justifique cada recomendação com margem de segurança (headroom)
5. Na gravação, mostre que você **não aplicaria** a mudança sem validar em staging e sem acordo do time

---

## Prompt 1 — Rightsizing do payments-api (over-provisioning)

```
Você é um SRE com foco em rightsizing de workloads Kubernetes em produção.

Analise o deployment payments-api (namespace payments) e sugira novos requests/limits.

Dados atuais (2 réplicas):
- Requests: CPU 1000m, Memória 1 Gi
- Limits: CPU 1500m, Memória 2 Gi

Uso observado (7 dias, por pod):
- CPU média: 72m | CPU P95: 95m | CPU pico isolado: 120m
- Memória média: 88 Mi | Memória P95: 110 Mi | Pico: 125 Mi

Restrições:
- Manter margem de ~30% acima do P95 para requests
- Limits devem absorver picos sem OOMKill ou throttling agressivo
- Serviço é crítico (pagamentos), rollout gradual obrigatório

Responda em português do Brasil:
1. Valores sugeridos de requests e limits (CPU e memória) com justificativa.
2. Risco operacional de cada mudança (baixo/médio/alto) e mitigação.
3. Impacto estimado de capacidade liberada no cluster (CPU e memória agregadas).
4. Plano de rollout: ordem, monitoração durante 48h, critério de rollback.
5. Estimativa de economia relativa se o custo for proporcional aos requests (compare antes/depois em %).
```

---

## Prompt 2 — Comparativo entre os três workloads

```
Compare rightsizing entre três deployments e priorize por impacto financeiro.

| Workload      | NS       | Réplicas | CPU req | CPU P95 | Mem req | Mem P95 | Criticidade |
|---------------|----------|----------|---------|---------|---------|---------|-------------|
| payments-api  | payments | 2        | 1000m   | 95m     | 1 Gi    | 110 Mi  | Alta        |
| users-api     | users    | 2        | 100m    | 62m     | 128 Mi  | 92 Mi   | Alta        |
| staging-api   | staging  | 1        | 500m    | 35m     | 512 Mi  | 72 Mi   | Baixa       |

Premissa de custo (didática): custo alocável ≈ soma dos requests × preço unitário do cluster.

Responda em português do Brasil para um Platform Engineer:
1. Ranking de oportunidade de economia (1º ao 3º) com % estimado de redução de requests.
2. Para cada workload: requests/limits recomendados.
3. Qual mudança você faria na primeira sprint e qual deixaria para depois — e por quê.
4. O users-api precisa de alteração ou serve como baseline saudável?
5. staging-api: rightsizing ou scale-to-zero / desligamento noturno?
```

---

## Prompt 3 — Análise de risco operacional

```
Após sugerir redução de requests do payments-api de 1000m → 150m CPU e 1 Gi → 256 Mi RAM, avalie riscos operacionais.

Contexto adicional:
- HPA não configurado; réplicas fixas em 2
- Sem VPA instalado no cluster
- Time de payments resiste a mudanças perto de datas de alto volume (Black Friday simulada em +40% CPU P95)

Responda em português do Brasil:
1. Cenários de falha possíveis após o rightsizing (throttling, eviction, latência, scheduling).
2. Que sinais no Prometheus/Grafana indicariam que a mudança foi agressiva demais?
3. Qual margem de headroom você manteria em produção vs. staging?
4. Recomendação: aplicar em staging primeiro? em uma réplica canário? ambos?
5. Template de comunicação curto para o time de payments explicando a mudança.
```

---

## Prompt 4 — Automação e VPA/Recommendation

```
Sou DevOps avaliando automação de rightsizing no cluster FinOps AI Lab (payments, users, staging).

Hoje os requests são definidos manualmente no YAML. Uso Prometheus para métricas reais.

Responda em português do Brasil:
1. Quando faz sentido usar VPA (Vertical Pod Autoscaler) vs. recomendações manuais assistidas por IA?
2. Para payments-api, users-api e staging-api, qual abordagem você recomenda e por quê?
3. Desenhe um fluxo simples: métrica → IA analisa → humano aprova → PR no GitOps.
4. Que guardrails impedem que automação reduza requests de serviço crítico sem aprovação?
5. Liste 3 anti-patterns comuns de rightsizing em Kubernetes que a IA não deve perpetuar.
```

---

## Prompt 5 — Business case para Engineering Manager

```
Preciso traduzir uma otimização técnica de rightsizing em linguagem de negócio.

Dados:
- payments-api: economia estimada de 85% nos requests de CPU e 75% em memória após ajuste
- staging-api: economia adicional se desligado 12h/dia nos fins de semana
- users-api: já eficiente, sem ação imediata
- Esforço: 2 dias de engenharia + 1 semana de observação

Responda em português do Brasil:
1. Resumo executivo em 5 linhas para um Engineering Manager.
2. Tabela impacto vs. esforço vs. risco para as três iniciativas.
3. KPIs para medir sucesso após 30 dias (utilização, incidentes, custo alocado).
4. Uma frase de "por que agora" conectando eficiência operacional e margem do produto.
```
