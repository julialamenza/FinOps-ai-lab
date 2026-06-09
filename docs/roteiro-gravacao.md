# FinOps com IA — Roteiro de Gravação

## Aula 1 — Observabilidade de custos e comportamento operacional

### Vídeo 1.1 — O desafio da eficiência operacional em cloud

Objetivo:
Explicar por que ambientes distribuídos aumentam complexidade operacional e dificultam controle de custos.

Slides:
- Slide 1: Introdução
- Slide 2: O desafio da eficiência operacional em cloud
- Slide 3: Crescimento da complexidade

Demo:
Nenhuma.

Prompt IA:
"Analise este cenário de cloud com múltiplos namespaces e explique onde podem surgir desperdícios operacionais."

Tempo estimado:
8-10 min

---

### Vídeo 1.2 — Entendendo comportamento de consumo em cloud

Objetivo:
Explicar como workloads, escalabilidade, ambientes e pipelines influenciam padrões de utilização e custo.

Slides:
- Slide 4: Observabilidade + FinOps
- Slide 5: Workloads, requests, limits, HPA/VPA e namespaces

Demo:
```bash
kubectl get ns --show-labels
kubectl get deploy -A
````

