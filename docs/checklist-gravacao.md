# FinOps com IA — Checklist de Gravação

Checklist operacional para garantir qualidade técnica e consistência em cada sessão de gravação.

---

## Checklist antes da gravação (geral)

### Ambiente local

- [ ] Minikube rodando (`minikube status`)
- [ ] `kubectl cluster-info` responde sem erro
- [ ] Helm instalado e funcional
- [ ] Repositório clonado e atualizado na máquina de gravação

### Stack do laboratório

- [ ] Prometheus instalado (`kubectl get pods -n monitoring`)
- [ ] Grafana acessível via port-forward (`localhost:3000`)
- [ ] OpenCost instalado (`kubectl get pods -n opencost`)
- [ ] Workloads do lab rodando (`kubectl get deploy -A | grep -E 'payments|users|staging'`)
- [ ] `./scripts/warmup-lab-metrics.sh` executado (metricas nos dashboards)
- [ ] Anomalias **desativadas** (`./scripts/stop-all-anomalies.sh` executado)

### Dashboards

- [ ] `finops-ai-lab.json` importado no Grafana
- [ ] `finops-ai-rightsizing.json` importado no Grafana
- [ ] `finops-ai-anomalies.json` importado no Grafana
- [ ] `finops-ai-governance.json` importado no Grafana
- [ ] Datasource Prometheus selecionado em todos os dashboards
- [ ] Painéis exibindo dados (sem "No data")

### Materiais de apoio

- [ ] Prompt do vídeo aberto (`ai-prompts/aula-XX/<video>-*.md`)
- [ ] Slides da aula abertos e revisados
- [ ] `docs/folha-gravacao.md` ou PDF `docs/manual-gravacao-completo.pdf` aberto
- [ ] `docs/roteiro-gravacao.md` aberto para consulta
- [ ] `docs/guia-gravacao.md` consultado para comandos da demo

### Setup de gravação

- [ ] Terminal limpo (sem histórico confuso ou credenciais visíveis)
- [ ] Navegador sem abas pessoais (apenas Grafana, Prometheus, OpenCost, IA)
- [ ] Notificações do sistema desativadas (modo Não Perturbe)
- [ ] Microfone testado e nível de áudio adequado
- [ ] Zoom da tela entre 100% e 125% (texto legível)
- [ ] Credenciais sensíveis escondidas (senha Grafana, tokens, `.env`)
- [ ] Resolução de gravação configurada (mín. 1280×720)
- [ ] Port-forwards necessários abertos em terminais separados

---

## Checklist por aula

### Aula 1 — Observabilidade

- [ ] Dashboard principal (`finops-ai-lab.json`) importado e com dados
- [ ] Port-forward do Grafana ativo
- [ ] `kubectl get ns --show-labels` testado
- [ ] `kubectl get deploy -A` testado
- [ ] `kubectl top pods -A` retorna métricas
- [ ] Prompts da Aula 1 revisados (`ai-prompts/aula-01/`)

### Aula 2 — Rightsizing

- [ ] Dashboard rightsizing (`finops-ai-rightsizing.json`) importado e com dados
- [ ] Painel CPU Waste Percentage mostra payments com waste alto
- [ ] `kubectl describe deployment payments-api -n payments` testado
- [ ] Prompts da Aula 2 revisados (`ai-prompts/aula-02/`)

### Aula 3 — Anomalias

- [ ] Dashboard anomalies (`finops-ai-anomalies.json`) importado e com dados
- [ ] `./scripts/start-anomaly.sh` testado — spike visível no Grafana em ~30s
- [ ] `./scripts/start-staging-anomaly.sh` testado — job `backup-sync` criado imediatamente
- [ ] `./scripts/stop-all-anomalies.sh` testado — baseline restaurado
- [ ] `./scripts/collect-anomaly-context.sh` testado — saída utilizável nos prompts
- [ ] Prompts da Aula 3 revisados (`ai-prompts/aula-03/`)

### Aula 4 — Governança

- [ ] Dashboard governance (`finops-ai-governance.json`) importado e com dados
- [ ] Port-forward do OpenCost ativo (`localhost:9003`)
- [ ] `kubectl get ns --show-labels` mostra labels team, environment, cost-center
- [ ] Prompts da Aula 4 revisados (`ai-prompts/aula-04/`)
- [ ] *(Opcional)* Screenshot do AWS Cost Explorer preparado

### Aula 5 — Eficiência operacional

- [ ] Todos os 4 dashboards acessíveis no Grafana
- [ ] Port-forwards Grafana + OpenCost ativos
- [ ] **Prompt mestre** revisado (`ai-prompts/aula-05/5.5-copiloto-eficiencia.md`)
- [ ] Achados das aulas 1–4 anotados para o fluxo completo
- [ ] *(Opcional)* Screenshot do AWS Cost Explorer preparado

---

## Checklist durante a gravação

- [ ] Nome do vídeo anunciado no início (ex.: "Vídeo 2.5 — Hands-on rightsizing")
- [ ] Dados reais do lab mencionados (não apenas exemplos dos slides)
- [ ] Gráficos de slide explicados como exemplos conceituais quando aplicável
- [ ] Resposta da IA comentada criticamente (não aceitar cegamente)
- [ ] Comandos executados em ritmo legível (pausar após output importante)
- [ ] Erros técnicos anotados em tempo real para revisão posterior

---

## Checklist pós-gravação

Preencha para **cada vídeo** gravado:

| Campo | Vídeo ___ |
|-------|-----------|
| Arquivo salvo | [ ] Sim |
| Nome padronizado | [ ] `aula-XX-video-XX-titulo-curto.mp4` |
| Vídeo revisado (assistido pelo menos 1x) | [ ] Sim |
| Erro técnico anotado | [ ] Sim / [ ] Não — descrição: ___________ |
| Regravação necessária? | [ ] Sim / [ ] Não |

### Critérios para marcar regravação

Marque **Sim** se:

- Comando falhou visivelmente e não foi corrigido na gravação
- Dashboard mostrou "No data" durante a demo principal
- Credencial sensível apareceu na tela
- Áudio inaudível por mais de 10 segundos
- Demo principal (hands-on) não foi concluída

### Nome padronizado sugerido

```text
aula-01-video-01-desafio-eficiencia.mp4
aula-01-video-05-hands-on-observabilidade.mp4
aula-03-video-05-hands-on-anomalias.mp4
aula-05-video-05-hands-on-fluxo-completo.mp4
```

---

## Checklist de entrega final (após os 25 vídeos)

- [ ] 25 vídeos gravados e nomeados
- [ ] Todos os vídeos revisados
- [ ] Regravações concluídas
- [ ] Screenshots exportados (ver `docs/assets-gravacao.md`)
- [ ] `docs/cronograma-gravacao.md` atualizado com status final
- [ ] Erros técnicos documentados para melhoria do lab
