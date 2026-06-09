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
* cpu-spike → workload temporário para demonstrações de anomalias

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

---

### 5. Importar o dashboard no Grafana

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

Importe:

```text
grafana/dashboards/finops-ai-lab.json
```

Passos:

1. Dashboards
2. New
3. Import
4. Upload JSON
5. Selecionar datasource Prometheus

---

### 6. Simular anomalias de CPU

Iniciar:

```bash
./scripts/start-anomaly.sh
```

Parar:

```bash
./scripts/stop-anomaly.sh
```

O workload `cpu-spike` utiliza a imagem `polinux/stress` para gerar carga artificial.

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
```

---

## Mapeamento com o curso

| Aula   | Tema                                                  | Recursos utilizados                          |
| ------ | ----------------------------------------------------- | -------------------------------------------- |
| Aula 1 | Observabilidade de custos e comportamento operacional | Grafana, Prometheus, Namespaces, OpenCost    |
| Aula 2 | Rightsizing e eficiência operacional automatizada     | Grafana, OpenCost, payments-api, staging-api |
| Aula 3 | Anomalias de custo e capacity planning                | cpu-spike, Grafana, Prometheus               |
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
│       └── finops-ai-lab.json
├── k8s/
│   ├── anomalies/
│   ├── namespaces/
│   └── workloads/
├── scripts/
│   ├── deploy-lab.sh
│   ├── cleanup-lab.sh
│   ├── install-opencost.sh
│   ├── start-anomaly.sh
│   └── stop-anomaly.sh
└── README.md
```

---

## Documentação do curso

* docs/cronograma-curso.md
* docs/roteiro-gravacao.md
* docs/checklist-repo.md

Prompts de IA:

* ai-prompts/README.md
* ai-prompts/aula-01-observabilidade.md
* ai-prompts/aula-02-rightsizing.md
* ai-prompts/aula-03-anomalias.md
* ai-prompts/aula-04-governanca.md
* ai-prompts/aula-05-eficiencia.md

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
