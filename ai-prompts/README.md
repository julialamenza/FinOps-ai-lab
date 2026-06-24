# Prompts de IA — FinOps com IA

Coleção de prompts reutilizáveis para gravação do curso **FinOps com IA**. Cada prompt corresponde a **um vídeo** — abra o arquivo do vídeo que está gravando e copie o bloco completo.

## Como usar durante o curso

**Na gravação**, use só `docs/manual-gravacao-completo.md` (ou o PDF). Cada vídeo já traz slides, comandos, o que mostrar e o prompt completo.

A pasta `ai-prompts/` é opcional — serve para editar prompts fora do manual, se preferir.

---

## Estrutura

```text
ai-prompts/
├── aula-01/          # 5 prompts (vídeos 1.1–1.5)
├── aula-02/          # 5 prompts (vídeos 2.1–2.5)
├── aula-03/          # 5 prompts (vídeos 3.1–3.5)
├── aula-04/          # 5 prompts (vídeos 4.1–4.5)
├── aula-05/          # 5 prompts (vídeos 5.1–5.5)
└── aula-0X-*.md      # Índices de compatibilidade (links para aula-0X/)
```

Cada pasta `aula-XX/` tem um `README.md` com a tabela vídeo → arquivo.

---

## Mapa completo (25 vídeos)

| Vídeo | Arquivo | Tema |
|-------|---------|------|
| 1.1 | `aula-01/1.1-narrativa-abertura.md` | Narrativa de abertura |
| 1.2 | `aula-01/1.2-desperdicios-operacionais.md` | Desperdícios operacionais *(opcional)* |
| 1.3 | `aula-01/1.3-padroes-sazonalidade.md` | Padrões de uso e sazonalidade |
| 1.4 | `aula-01/1.4-metricas-essenciais.md` | Métricas essenciais FinOps |
| 1.5 | `aula-01/1.5-panorama-consumo.md` | Panorama de consumo *(hands-on)* |
| 2.1 | `aula-02/2.1-business-case-em.md` | Business case para EM |
| 2.2 | `aula-02/2.2-rightsizing-payments-api.md` | Rightsizing payments-api |
| 2.3 | `aula-02/2.3-automacao-vpa.md` | Automação e VPA |
| 2.4 | `aula-02/2.4-rollout-hpa-vpa.md` | HPA, VPA e rollout gradual *(opcional)* |
| 2.5 | `aula-02/2.5-rightsizing-hands-on.md` | Rightsizing *(hands-on)* |
| 3.1 | `aula-03/3.1-deteccao-anomalia-cpu.md` | Detecção de anomalia |
| 3.2 | `aula-03/3.2-investigacao-anomalia-cpu.md` | Investigação com spike ao vivo |
| 3.3 | `aula-03/3.3-capacity-planning.md` | Capacity planning |
| 3.4 | `aula-03/3.4-anomalia-silenciosa-staging.md` | Anomalia silenciosa staging |
| 3.5 | `aula-03/3.5-runbook-anomalias.md` | Runbook *(hands-on)* |
| 4.1 | `aula-04/4.1-auditoria-labels.md` | Auditoria de labels |
| 4.2 | `aula-04/4.2-politica-ambientes.md` | Política prod vs staging |
| 4.3 | `aula-04/4.3-showback-chargeback.md` | Showback vs chargeback |
| 4.4 | `aula-04/4.4-guardrails.md` | Guardrails |
| 4.5 | `aula-04/4.5-visibilidade-persona.md` | Visibilidade por persona *(hands-on)* |
| 5.1 | `aula-05/5.1-diagnostico-consolidado.md` | Diagnóstico consolidado |
| 5.2 | `aula-05/5.2-priorizacao-matriz.md` | Matriz impacto × esforço |
| 5.3 | `aula-05/5.3-plano-90-dias.md` | Plano 90 dias |
| 5.4 | `aula-05/5.4-recomendacoes-executivas.md` | Recomendações executivas |
| 5.5 | `aula-05/5.5-copiloto-eficiencia.md` | **Prompt mestre** *(hands-on)* |

---

## Dados didáticos vs. dados reais

Os valores nos prompts (CPU, memória, custo estimado, réplicas) são **exemplos didáticos** calibrados para o laboratório local:

* **payments** — `payments-api` overprovisionado (2 réplicas, requests altos)
* **users** — `users-api` saudável (2 réplicas, requests alinhados ao uso)
* **staging** — `staging-api` com baixa utilização (1 réplica, ambiente não produtivo)

Eles não representam métricas ao vivo do seu cluster. Para demos autênticas, substitua pelos números reais coletados durante a gravação.

### Coletando dados do laboratório

O lab é montado na hora da gravação. Use os scripts abaixo para gerar um bloco pronto para colar nos prompts:

```bash
# Aulas 1, 2, 4 e 5 — panorama geral do cluster
./scripts/collect-lab-context.sh

# Aula 3 — contexto de anomalias (cpu-spike, backup-sync)
./scripts/collect-anomaly-context.sh
```

Comandos manuais úteis:

```bash
kubectl top pods -A
kubectl get deploy -A
kubectl get ns --show-labels

# Requests e limits
kubectl describe deployment payments-api -n payments
kubectl describe deployment users-api -n users
kubectl describe deployment staging-api -n staging
```

### Grafana

Utilize os dashboards do diretório:

```text
grafana/dashboards/
```

Exemplos de métricas:

* CPU por namespace
* Memória por namespace
* Top CPU consumers
* Top Memory consumers
* Requests vs utilização
* Tendências de crescimento

### OpenCost

Acesse via port-forward:

```bash
kubectl port-forward svc/opencost 9003:9090 -n opencost
```

Depois abra:

```text
http://localhost:9003
```

Utilize principalmente:

* Allocation
* Assets
* Namespace Costs
* Workload Costs

---

## Como substituir valores por métricas reais

Ao colar um prompt, atualize a seção **Dados do ambiente** com valores reais:

| Campo                | Fonte                        |
| -------------------- | ---------------------------- |
| CPU média            | Grafana / Prometheus         |
| CPU P95              | Grafana / Prometheus         |
| Memória média        | Grafana                      |
| Memória P95          | Grafana                      |
| Requests e Limits    | kubectl describe deployment  |
| Custos por namespace | OpenCost Allocation          |
| Labels               | kubectl get ns --show-labels |
| Réplicas             | kubectl get deploy -A        |

Mantenha o restante do prompt intacto.

A IA responde melhor quando recebe:

✅ tabelas

✅ séries temporais

✅ métricas reais

✅ contexto operacional

Evite fornecer apenas números isolados.

---

## IA como copiloto, não como decisão automática

Os prompts deste diretório foram criados para acelerar análises de:

* FinOps
* Kubernetes
* Observabilidade
* Capacity Planning
* Governança
* Rightsizing

A IA deve atuar como:

* copiloto de análise
* gerador de hipóteses
* assistente de investigação
* apoio à comunicação técnica e executiva

A IA **não substitui**:

* validação humana
* conhecimento do time dono do workload
* revisão operacional
* gestão de risco
* plano de rollback

### Sempre valide

Antes de aplicar qualquer recomendação:

1. Verifique os dados no Grafana e Prometheus.
2. Confirme com o time responsável pelo workload.
3. Teste em staging quando possível.
4. Monitore após a mudança.
5. Tenha um plano de rollback.

---

## Fluxo recomendado do curso

```text
Observabilidade
        ↓
Análise com IA
        ↓
Rightsizing
        ↓
Detecção de Anomalias
        ↓
Governança
        ↓
Eficiência Contínua
```

O objetivo do curso não é automatizar decisões, mas mostrar como a IA pode acelerar o ciclo:

```text
Observar
    ↓
Analisar
    ↓
Decidir
    ↓
Executar
    ↓
Medir
```

mantendo o ser humano responsável pelas decisões finais.
