# AWS Cost Explorer, Billing e alertas — gravação sem EKS

O curso roda em **Minikube local**. **Não é obrigatório** ter Kubernetes na AWS (EKS), conta AWS ativa, nem abrir o console AWS ao vivo.

## O que demo ao vivo vs conceitual

| Ferramenta AWS | Demo ao vivo? | Vídeos |
|----------------|---------------|--------|
| **Cost Explorer** | Opcional (screenshot ou console) | **4.4** (principal), menção em 5.3 |
| **Billing (fatura)** | Não — conceitual ou screenshot | 4.4, 5.3, 5.5 (plano 90 dias) |
| **Budgets / alertas de billing** | Não — conceitual ou screenshot | 4.3, 5.3, 5.5 |
| **OpenCost** (no Minikube) | **Sim** — demo principal | 4.5, 5.5 |

**Hands-on (4.5 e 5.5):** use **OpenCost** (`http://localhost:9003`) + Grafana. **Não abra** Cost Explorer nem Billing durante o hands-on — fica confuso e não reflete o lab.

## Três modos de gravação

### Modo A — Sem conta AWS *(recomendado)*

- Use **slides** + painel *OpenCost + AWS Cost Explorer* no dashboard `finops-ai-governance.json`.
- Fale: *"Nosso lab é Minikube local; em produção o Cost Explorer mostraria a fatura cloud e o OpenCost alocaria por namespace."*
- Caso EKS +30% do slide = **cenário ilustrativo**, não precisa existir na sua conta.

### Modo B — Com conta AWS, sem EKS

- **Screenshot** do Cost Explorer (*Cost by Service*, últimos 30 dias) — qualquer serviço (EC2, S3, etc.) serve para mostrar visão de conta.
- **Budgets:** screenshot de um budget de exemplo ou slide; explique alertas por e-mail/SNS quando custo > 80% do budget.
- **Não precisa** linha EKS na fatura — o cruzamento com namespace continua sendo explicado com OpenCost local.

### Modo C — Com EKS *(opcional, produção)*

- Cost Explorer filtrado em *Elastic Kubernetes Service* + OpenCost por namespace.
- Mostre cruzamento real: fatura EKS subiu → OpenCost aponta namespace/workload.

## Script de fala (~30 s) — vídeo 4.4

> "O lab roda em Minikube — não temos cluster na AWS. O OpenCost simula custo por namespace com preços públicos AWS. O Cost Explorer, em produção, mostra o custo **real da infra cloud** — EC2, EKS, load balancers, storage. As duas ferramentas se complementam: a fatura sobe no Billing → Cost Explorer aponta o **serviço** → OpenCost aponta o **namespace/workload**. Budgets e alertas de billing avisam **antes** da surpresa na fatura; alertas no Grafana/OpenCost avisam **dentro** do cluster."

## Onde cada conceito aparece

| Vídeo | Slide | AWS console? | O que fazer |
|-------|-------|--------------|-------------|
| 1.4 | 10–12 | Não | Alertas = Grafana/Prometheus; mencione que em produção **Billing alerts** complementam |
| 4.3 | 7 | Não | FinOps persona: budget vs actual — **conceitual**; cite AWS Budgets como exemplo |
| **4.4** | **8** | **Opcional** | **Cost Explorer + Billing + Budgets** — teoria; screenshot ou Modo A |
| 4.5 | 9–10 | **Não** | OpenCost + Grafana ao vivo; painel comparativo no dashboard = referência |
| 5.3 | 7 | Não | OpenCost vs Cost Explorer — complementares; sem abrir AWS |
| 5.4 | 8 | Não | Estágio Governança = budgets — conceitual |
| 5.5 | 9–10 | **Não** | Plano 90 dias cita budgets/alertas — OpenCost + 4 dashboards ao vivo |

## Screenshots sugeridos (Modo A ou B)

Salve em `docs/screenshots/` (não commitar dados sensíveis):

| Arquivo sugerido | Conteúdo | Usar em |
|------------------|----------|---------|
| `cost-explorer-by-service.png` | Cost Explorer → Cost by Service | 4.4 |
| `aws-billing-monthly.png` | Billing → Bills → Total (valores borrados se necessário) | 4.4 |
| `aws-budget-alert.png` | Budgets → budget com threshold 80%/100% | 4.3 ou 4.4 |

## Checklist AWS (antes de gravar 4.3–4.4)

- [ ] Decidi o modo: **A** (sem AWS), **B** (screenshots) ou **C** (conta com EKS)
- [ ] Screenshots preparados *(Modo A/B)* — ou usar apenas slides
- [ ] Console AWS **fora** da gravação do hands-on 4.5
- [ ] Conta ID, nomes de conta e valores reais **borrados** se usar screenshot
- [ ] OpenCost testado em `localhost:9003` *(4.5)*
