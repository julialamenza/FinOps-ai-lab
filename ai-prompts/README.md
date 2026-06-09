# Prompts de IA — FinOps com IA

Coleção de prompts reutilizáveis para gravação do curso **FinOps com IA**. Cada arquivo corresponde a uma aula e contém prompts prontos para copiar e colar em ferramentas como ChatGPT, Claude, Cursor ou Copilot.

## Como usar durante o curso

1. **Antes da gravação**, leia o arquivo da aula e identifique qual prompt combina com o momento do roteiro (demo, slide ou discussão).
2. **Durante a gravação**, copie o bloco completo do prompt — incluindo os dados de exemplo — e cole na ferramenta de IA escolhida.
3. **Substitua os dados de exemplo** pelos valores reais coletados no laboratório (Grafana, Prometheus, OpenCost ou `kubectl top`).
4. **Comente a resposta da IA** em voz alta ou na tela: valide se faz sentido operacionalmente antes de apresentar como conclusão.
5. **Salve respostas úteis** como referência para a aula seguinte ou para montar dashboards e runbooks.

---

## Arquivos por aula

| Arquivo                      | Tema                                                  |
| ---------------------------- | ----------------------------------------------------- |
| `aula-01-observabilidade.md` | Observabilidade de custos e comportamento operacional |
| `aula-02-rightsizing.md`     | Rightsizing e eficiência operacional automatizada     |
| `aula-03-anomalias.md`       | Anomalias de custo e capacity planning operacional    |
| `aula-04-governanca.md`      | Governança operacional e visibilidade de custos       |
| `aula-05-eficiencia.md`      | Operações cloud orientadas por eficiência             |

---

## Dados didáticos vs. dados reais

Os valores nos prompts (CPU, memória, custo estimado, réplicas) são **exemplos didáticos** calibrados para o laboratório local:

* **payments** — `payments-api` overprovisionado (2 réplicas, requests altos)
* **users** — `users-api` saudável (2 réplicas, requests alinhados ao uso)
* **staging** — `staging-api` com baixa utilização (1 réplica, ambiente não produtivo)

Eles não representam métricas ao vivo do seu cluster. Para demos autênticas, substitua pelos números reais coletados durante a gravação.

### Coletando dados do laboratório

```bash
# Uso atual por pod
kubectl top pods -A

# Uso atual por namespace
kubectl top pods -A

# Deployments
kubectl get deploy -A

# Labels de governança
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
