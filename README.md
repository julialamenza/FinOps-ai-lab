# FinOps AI Lab

Laboratório local para demonstrações de FinOps com IA usando Minikube, Prometheus, Grafana, OpenCost e workloads Kubernetes simulados.

## Objetivo

Demonstrar:

* observabilidade de custos
* over-provisioning
* rightsizing
* anomalias operacionais
* governança por labels
* análise com IA

---

## Arquitetura

```text
                    +------------------+
                    |     OpenCost     |
                    +--------+---------+
                             |
                             |
+-------------+     +--------v---------+
| Kubernetes  |---->|   Prometheus     |
|  Minikube   |     +--------+---------+
+------+------+              |
       |                     |
       |                     |
       |            +--------v---------+
       |            |     Grafana      |
       |            +------------------+
       |
       +-- payments
       +-- users
       +-- staging
```

Objetivo do laboratório:

* payments → workload overprovisionado para exercícios de rightsizing
* users → workload saudável utilizado como baseline
* staging → workload subutilizado para exercícios de scheduling e otimização
* cpu-spike → workload temporário para demonstrações de anomalias de CPU
* backup-sync → CronJob em staging para anomalia silenciosa de custo (Aula 3)
* business-hours-load → geradores de tráfego HTTP que simulam padrões de uso por horário comercial

---

## Stack

* Minikube
* Kubernetes
* Prometheus
* Grafana
* OpenCost

---

## Pré-requisitos

Instale as ferramentas abaixo antes de subir o laboratório:

| Ferramenta | Uso                                     |
| ---------- | --------------------------------------- |
| Minikube   | Cluster Kubernetes local                |
| kubectl    | Gerenciar recursos no cluster           |
| Helm       | Instalar Prometheus, Grafana e OpenCost |

Recomendações de recursos para o Minikube:

```bash
minikube start --cpus=4 --memory=8192 --driver=docker
```

---

## Como rodar o laboratório

Execute os passos na ordem abaixo, a partir da raiz do repositório.

### 1. Subir o cluster

```bash
minikube start --cpus=4 --memory=8192
kubectl cluster-info
```

---

### 2. Instalar Prometheus e Grafana

O OpenCost e os dashboards dependem do Prometheus instalado via `kube-prometheus-stack` no namespace `monitoring`.

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm upgrade --install monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace
```

Aguarde os pods ficarem prontos:

```bash
kubectl get pods -n monitoring
```

---

### 3. Instalar o OpenCost

```bash
chmod +x scripts/*.sh
./scripts/install-opencost.sh
```

O script instala o OpenCost via Helm e aponta para o Prometheus do stack de monitoramento.

Verifique:

```bash
kubectl get pods -n opencost
```

---

### 4. Subir os workloads do laboratório

```bash
./scripts/deploy-lab.sh
```

Isso cria os namespaces e aplica os deployments.

| Workload     | Namespace | Cenário                             |
| ------------ | --------- | ----------------------------------- |
| payments-api | payments  | Over-provisioning de CPU e memória  |
| users-api    | users     | Workload saudável (baseline)        |
| staging-api  | staging   | Ambiente de staging para scale down |
| cpu-spike    | payments  | Geração de anomalias sob demanda    |

Verifique:

```bash
kubectl get deploy -A
kubectl get ns --show-labels
```

Gere métricas para os dashboards (lab fresco — ~3 min):

```bash
./scripts/warmup-lab-metrics.sh
```

> O cluster local **não tem histórico de dias**. Use **Last 15 minutes** no Grafana e **Today** no OpenCost. `Last 7 days` ficará vazio — comportamento esperado.

---

### 5. Importar os dashboards no Grafana

Abra o Grafana:

```bash
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
```

Acesse:

```text
http://localhost:3000
```

Recupere a senha:

```bash
kubectl get secret -n monitoring monitoring-grafana \
-o jsonpath="{.data.admin-password}" | base64 -d
```

Importe cada JSON (Dashboards → New → Import → Upload JSON → datasource Prometheus):

| Dashboard | Arquivo | Aula |
| --------- | ------- | ---- |
| Principal | `grafana/dashboards/finops-ai-lab.json` | 1 |
| Rightsizing | `grafana/dashboards/finops-ai-rightsizing.json` | 2 |
| Anomalies | `grafana/dashboards/finops-ai-anomalies.json` | 3 |
| Governance | `grafana/dashboards/finops-ai-governance.json` | 4 |

> O lab é montado na hora da gravação. Rode `./scripts/warmup-lab-metrics.sh` e use **Last 15 minutes** nos dashboards. Se já importou dashboards antes, **reimporte** os JSONs após atualizações.

---

### 6. Simular carga por horário comercial

Gera tráfego HTTP realista contra as APIs do laboratório para demonstrar padrões de uso ao longo do dia. Útil para exercícios de observabilidade e comparação entre workloads.

Requer que `./scripts/deploy-lab.sh` já tenha sido executado.

Iniciar (modo demo — padrão):

```bash
./scripts/start-business-hours-load.sh
```

O modo **demo** comprime um dia inteiro em ~12 minutos e repete automaticamente:

| Fase      | Duração | Comportamento de `payments` |
| --------- | ------- | --------------------------- |
| Comercial | 0–6 min | Alto (rajadas de requisições) |
| Fora do pico | 6–9 min | Médio |
| Noite/fim de semana | 9–12 min | Baixo |

Para usar o relógio real (seg–sex 09h–18h, `America/Sao_Paulo`):

```bash
./scripts/start-business-hours-load.sh --real
```

Parar:

```bash
./scripts/stop-business-hours-load.sh
```

| Gerador de carga        | Namespace | Comportamento                          |
| ----------------------- | --------- | -------------------------------------- |
| payments-business-load  | payments  | Oscila conforme horário comercial     |
| users-steady-load       | users     | Tráfego estável o dia todo             |
| staging-idle-load       | staging   | Quase ocioso (1 requisição/min)        |

Manifest: `k8s/workloads/business-hours-load.yaml`

Para ver a tendência no Grafana após iniciar o modo demo:

1. **Gravação:** aguarde 2–3 minutos e abra `finops-ai-lab.json` com **Last 15 minutes**
2. **Demo completa:** aguarde ~12 minutos para ver o ciclo inteiro
3. Compare: `payments` oscila, `users` estável, `staging` quase flat

Coletar dados para prompts de IA:

```bash
./scripts/collect-lab-context.sh
```

---

### 7. Simular anomalias (Aula 3)

#### 7a. Spike de CPU em payments

Fluxo recomendado para gravação (baseline realista + spike):

```bash
./scripts/start-business-hours-load.sh
sleep 120
./scripts/start-anomaly.sh
```

Ou apenas o spike (visível em ~30s):

```bash
./scripts/start-anomaly.sh
./scripts/start-anomaly.sh --duration 180   # spike de 3 min
```

Parar:

```bash
./scripts/stop-anomaly.sh
```

Coletar dados para colar nos prompts de IA:

```bash
./scripts/collect-anomaly-context.sh
```

Dashboard: `finops-ai-anomalies.json` — painéis **CPU Spike Detector** e **Top CPU Consumers**.

#### 7b. Anomalia silenciosa em staging (vídeo 3.4)

CronJob `backup-sync` que sobe custo/CPU em rajadas sem incidente de disponibilidade. Um job é disparado imediatamente — não precisa esperar o schedule.

```bash
./scripts/start-staging-anomaly.sh
```

Parar:

```bash
./scripts/stop-staging-anomaly.sh
```

Parar todas as anomalias de uma vez:

```bash
./scripts/stop-all-anomalies.sh
```

---

## Acessos úteis

### Prometheus

```bash
kubectl port-forward -n monitoring \
svc/monitoring-kube-prometheus-prometheus \
9090:9090
```

Acesse:

```text
http://localhost:9090
```

---

### Grafana

```bash
kubectl port-forward -n monitoring \
svc/monitoring-grafana \
3000:80
```

Acesse:

```text
http://localhost:3000
```

---

### OpenCost

```bash
kubectl port-forward -n opencost \
svc/opencost \
9003:9090
```

Acesse:

```text
http://localhost:9003
```

Utilize principalmente:

* Allocation
* Assets
* Namespace Costs
* Workload Costs

No OpenCost, use a janela **Today** ou **Last 24h**. Aguarde 2–3 min após `warmup-lab-metrics.sh` para os primeiros valores aparecerem.

---

## IA no laboratório

O laboratório foi projetado para demonstrar como Large Language Models podem atuar como copilotos de análise operacional e FinOps.

Os prompts utilizados durante as aulas estão disponíveis em:

```text
ai-prompts/
```

Exemplos de uso:

* Detecção de desperdício operacional
* Recomendações de rightsizing
* Investigação de anomalias
* Capacity planning
* Governança de custos
* Relatórios executivos

Importante:

A IA auxilia a análise e geração de hipóteses, mas não substitui:

* validação humana
* testes em staging
* processos formais de mudança
* revisão operacional

---

## Comandos úteis para demos

```bash
# Consumo por pod
kubectl top pods -A

# Deployments
kubectl get deploy -A

# Namespaces e labels
kubectl get ns --show-labels

# Requests e limits
kubectl describe deployment payments-api -n payments
kubectl describe deployment users-api -n users
kubectl describe deployment staging-api -n staging

# Pods
kubectl get pods -A

# Geradores de carga por horário comercial
kubectl get pods -n payments -l app=payments-business-load
kubectl get pods -n users -l app=users-steady-load
kubectl get pods -n staging -l app=staging-idle-load

# Contexto para prompts de IA
./scripts/collect-lab-context.sh
./scripts/collect-anomaly-context.sh
```

---

## Mapeamento com o curso

| Aula   | Tema                                                  | Recursos utilizados                          |
| ------ | ----------------------------------------------------- | -------------------------------------------- |
| Aula 1 | Observabilidade de custos e comportamento operacional | Grafana, Prometheus, Namespaces, OpenCost, business-hours-load |
| Aula 2 | Rightsizing e eficiência operacional automatizada     | Grafana, OpenCost, payments-api, staging-api |
| Aula 3 | Anomalias de custo e capacity planning                | cpu-spike, backup-sync, finops-ai-anomalies.json, collect-anomaly-context |
| Aula 4 | Governança operacional e visibilidade de custos       | Labels, Cost Centers, Namespaces             |
| Aula 5 | Operações cloud orientadas por eficiência             | Fluxo completo de análise, otimização e IA   |

---

## Limpar o laboratório

Remove workloads e namespaces:

```bash
./scripts/cleanup-lab.sh
```

Remover também monitoramento e OpenCost:

```bash
helm uninstall monitoring -n monitoring
helm uninstall opencost -n opencost

minikube stop
```

---

## Estrutura do repositório

```text
finops-ai-lab/
├── ai-prompts/              # Prompts utilizados nas aulas
├── docs/                    # Cronograma, roteiro e checklist
├── grafana/
│   └── dashboards/
│       ├── finops-ai-lab.json
│       ├── finops-ai-rightsizing.json
│       ├── finops-ai-anomalies.json
│       └── finops-ai-governance.json
├── k8s/
│   ├── anomalies/
│   ├── namespaces/
│   └── workloads/
├── scripts/
│   ├── deploy-lab.sh
│   ├── cleanup-lab.sh
│   ├── install-opencost.sh
│   ├── start-anomaly.sh
│   ├── stop-anomaly.sh
│   ├── start-staging-anomaly.sh
│   ├── stop-staging-anomaly.sh
│   ├── stop-all-anomalies.sh
│   ├── collect-anomaly-context.sh
│   ├── collect-lab-context.sh
│   ├── warmup-lab-metrics.sh
│   ├── start-business-hours-load.sh
│   └── stop-business-hours-load.sh
├── helm/
│   └── opencost-values.yaml
└── README.md
```

---

## Documentação do curso

* docs/folha-gravacao.md — **folha operacional rápida** (comandos, port-forwards)
* docs/manual-gravacao-completo.md — **manual completo** (roteiro + prompts dos 25 vídeos, exportável em PDF)
* docs/cronograma-curso.md
* docs/roteiro-gravacao.md
* docs/checklist-repo.md

Prompts de IA (um arquivo por vídeo):

* ai-prompts/README.md
* ai-prompts/aula-01/ … ai-prompts/aula-05/ (25 prompts, ex.: `aula-01/1.1-narrativa-abertura.md`)
* ai-prompts/aula-0X-*.md — índices de compatibilidade

---

## Fluxo de FinOps com IA

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

Objetivo final:

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

Mantendo a IA como copiloto e os engenheiros responsáveis pelas decisões finais.
