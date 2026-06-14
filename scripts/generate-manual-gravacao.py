#!/usr/bin/env python3
"""Gera docs/manual-gravacao-completo.md — roteiro + comandos + prompts dos 25 vídeos."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
PROMPTS = ROOT / "ai-prompts"
OUT = DOCS / "manual-gravacao-completo.md"
ROTEIRO = DOCS / "roteiro-gravacao.md"
FOLHA = DOCS / "folha-gravacao.md"

# Tipo e notas operacionais por vídeo (folha-gravacao.md)
VIDEO_OPS = {
    "1.1": ("T", "Slides. Sem terminal."),
    "1.2": ("T+", "Slides + kubectl. Prompt opcional."),
    "1.3": ("T+", "Slides + Grafana. Opcional: business-hours 2 min antes."),
    "1.4": ("T+", "Slides + Grafana + menção Prometheus."),
    "1.5": ("H", "Hands-on — fluxo completo abaixo."),
    "2.1": ("T", "Slides. Citar payments-api."),
    "2.2": ("T+", "Slides + dashboard Usage vs Requests."),
    "2.3": ("T+", "Slides + kubectl describe opcional."),
    "2.4": ("T", "Slides. Citar staging-api. Prompt opcional."),
    "2.5": ("H", "Hands-on — fluxo completo abaixo."),
    "3.1": ("T+", "Slides + dashboard sem spike."),
    "3.2": ("T++", "Slides + ativar spike."),
    "3.3": ("T+", "Slides + Capacity Headroom."),
    "3.4": ("T++", "Slides + anomalia silenciosa staging."),
    "3.5": ("H", "Hands-on — fluxo completo abaixo."),
    "4.1": ("T+", "Slides + labels."),
    "4.2": ("T+", "Slides + Governance Matrix."),
    "4.3": ("T+", "Slides + Showback + OpenCost."),
    "4.4": ("T+", "Slides + Guardrails Checklist."),
    "4.5": ("H", "Hands-on — fluxo completo abaixo."),
    "5.1": ("T+", "Slides + tour nos 4 dashboards."),
    "5.2": ("T", "Slides + matriz impacto×esforço."),
    "5.3": ("T", "Slides. Sem lab."),
    "5.4": ("T", "Slides de fechamento."),
    "5.5": ("H", "Hands-on final — prompt mestre."),
}

# Comandos e passos extraídos da folha operacional
VIDEO_COMMANDS = {
    "1.2": """```bash
kubectl get ns --show-labels
kubectl get deploy -A
```""",
    "1.3": """```bash
./scripts/start-business-hours-load.sh
# aguarde 2–3 min
# Grafana → finops-ai-lab.json → Last 15 minutes
```""",
    "1.5": """```bash
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
./scripts/start-business-hours-load.sh
sleep 120
./scripts/collect-lab-context.sh
```

**Passos na tela:**
1. http://localhost:3000 → `finops-ai-lab.json` → **Last 15 minutes**
2. Gauges por namespace + Top CPU/Memory Consumers
3. Colar saída do `collect-lab-context.sh` no prompt abaixo
4. Comparar resposta da IA com o Grafana""",
    "2.2": """```bash
# Grafana → finops-ai-rightsizing.json → Last 15 minutes
# Painéis: Usage vs Requests, Waste %
```""",
    "2.3": """```bash
kubectl describe deployment payments-api -n payments
```""",
    "2.5": """```bash
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
./scripts/collect-lab-context.sh
kubectl describe deployment payments-api -n payments
kubectl top pods -n payments
```

**Passos na tela:**
1. `finops-ai-rightsizing.json` → CPU Waste, Top Overprovisioned, Candidates
2. Destacar **payments** (over) e **staging** (sub)
3. Colar `collect-lab-context.sh` no prompt abaixo
4. Enfatizar: não aplicaria em prod sem validar em staging""",
    "3.1": """```bash
# Grafana → finops-ai-anomalies.json → Last 15 minutes
# Painel: Payments CPU Timeline (sem cpu-spike ativo)
```""",
    "3.2": """```bash
./scripts/start-anomaly.sh
kubectl get pods -n payments
kubectl top pods -n payments
# Grafana → CPU Spike Detector (~30s)
./scripts/stop-anomaly.sh
```""",
    "3.4": """```bash
./scripts/start-staging-anomaly.sh
kubectl get jobs -n staging -l app=backup-sync
kubectl top pods -n staging
./scripts/stop-staging-anomaly.sh
```""",
    "3.5": """```bash
./scripts/stop-all-anomalies.sh
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
./scripts/start-business-hours-load.sh
sleep 120
./scripts/start-anomaly.sh
./scripts/collect-anomaly-context.sh
```

**Passos na tela:**
1. `finops-ai-anomalies.json` → **Last 15 minutes**
2. Baseline → spike → Top CPU Consumers → Capacity Headroom
3. Colar `collect-anomaly-context.sh` no prompt abaixo
4. `./scripts/stop-all-anomalies.sh` → confirmar retorno ao baseline""",
    "4.1": """```bash
kubectl get ns --show-labels
```""",
    "4.3": """```bash
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
kubectl port-forward -n opencost svc/opencost 9003:9090
# Grafana → Showback View | http://localhost:9003
```""",
    "4.5": """```bash
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
kubectl port-forward -n opencost svc/opencost 9003:9090
./scripts/collect-lab-context.sh
kubectl get ns --show-labels
```

**Passos na tela:**
1. `finops-ai-governance.json` → Matrix, Showback, Guardrails
2. http://localhost:9003 → custo por namespace/workload
3. Colar `collect-lab-context.sh` no prompt abaixo
4. *(Opcional)* screenshot AWS Cost Explorer""",
    "5.1": """```bash
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
# finops-ai-lab → rightsizing → anomalies → governance
```""",
    "5.5": """```bash
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
kubectl port-forward -n opencost svc/opencost 9003:9090
./scripts/collect-lab-context.sh
kubectl top pods -A
```

**Passos na tela:**
1. Percorrer 4 dashboards (1 min cada) → **Last 15 minutes**
2. Resumo: payments over, users ok, staging sub, anomalias = lição
3. http://localhost:9003 → visão consolidada
4. Colar `collect-lab-context.sh` no prompt mestre abaixo
5. Plano de 90 dias + KPIs da resposta da IA""",
}

AULA_HEADERS = {
    "1": ("Observabilidade de custos e comportamento operacional", "finops-ai-lab.json"),
    "2": ("Rightsizing e eficiência operacional automatizada", "finops-ai-rightsizing.json"),
    "3": ("Anomalias de custo e capacity planning operacional", "finops-ai-anomalies.json"),
    "4": ("Governança operacional e visibilidade de custos", "finops-ai-governance.json"),
    "5": ("Operações cloud orientadas por eficiência", "Todos os dashboards"),
}


def extract_folha_preamble() -> str:
    text = FOLHA.read_text(encoding="utf-8")
    end = text.find("# AULA 1 —")
    if end == -1:
        end = len(text)
    body = text[:end].strip()
    # Remove cabeçalho da folha (já está no manual)
    body = re.sub(
        r"^# FinOps com IA — Folha Operacional de Gravação\n\n"
        r"Documento de consulta \*\*rápida\*\*.*?\n\n"
        r"> \*\*PDF com tudo.*?\n\n"
        r"> O lab é montado \*\*na hora\*\*.*?\n\n"
        r"---\n\n",
        "",
        body,
        count=1,
        flags=re.DOTALL,
    )
    body = re.sub(r"\n---\s*$", "", body)
    return body


def parse_videos():
    text = ROTEIRO.read_text(encoding="utf-8")
    pattern = re.compile(
        r"### Vídeo (\d\.\d) — (.+?)\n\n(.*?)(?=\n---\n\n### Vídeo|\n---\n\n## Aula|\Z)",
        re.DOTALL,
    )
    videos = []
    for vid, title, body in pattern.findall(text):
        sections = {}
        current = None
        lines_buf = []
        for line in body.splitlines():
            if line.endswith(":") and not line.startswith(" ") and not line.startswith("-"):
                if current:
                    sections[current] = "\n".join(lines_buf).strip()
                current = line[:-1]
                lines_buf = []
            else:
                lines_buf.append(line)
        if current:
            sections[current] = "\n".join(lines_buf).strip()

        prompt_path = ""
        m = re.search(r"`(ai-prompts/[^`]+)`", sections.get("Prompt IA", ""))
        if m:
            prompt_path = m.group(1)

        videos.append({
            "id": vid,
            "title": title.strip(),
            "objetivo": sections.get("Objetivo", ""),
            "slides": sections.get("Slides", ""),
            "demo": sections.get("Demo", ""),
            "tempo": sections.get("Tempo estimado", ""),
            "prompt_path": prompt_path,
        })
    return videos


def load_prompt_content(prompt_path: str) -> tuple[str, str]:
    if not prompt_path:
        return "", ""
    full = ROOT / prompt_path
    if not full.exists():
        return "", f"*(arquivo não encontrado: {prompt_path})*"
    text = full.read_text(encoding="utf-8")
    antes = ""
    prompt = ""
    if "## Antes de colar" in text:
        parts = text.split("## Antes de colar", 1)[1]
        if "## Prompt" in parts:
            antes, rest = parts.split("## Prompt", 1)
            antes = antes.strip()
            m = re.search(r"```\n(.*?)```", rest, re.DOTALL)
            if m:
                prompt = m.group(1).strip()
    return antes, prompt


def render_video(v: dict) -> str:
    vid = v["id"]
    tipo, notas = VIDEO_OPS.get(vid, ("", ""))
    aula = vid.split(".")[0]
    _, dashboard = AULA_HEADERS.get(aula, ("", ""))

    lines = [
        f"### Vídeo {vid} — {v['title']}",
        "",
        f"| Campo | Valor |",
        f"|-------|-------|",
        f"| Tipo | **{tipo}** |" if tipo else "",
        f"| Tempo | {v['tempo']} |",
        f"| Dashboard | `{dashboard}` |",
        f"| Notas | {notas} |",
        "",
        f"**Objetivo:** {v['objetivo']}",
        "",
        f"**Slides:**",
        v["slides"] or "—",
        "",
    ]

    demo = v["demo"]
    extra_cmds = VIDEO_COMMANDS.get(vid, "")
    if demo and demo.lower() not in ("nenhuma.", "nenhuma"):
        lines.extend(["**Demo / roteiro:**", demo, ""])
    if extra_cmds:
        lines.extend(["**Comandos e passos (folha operacional):**", extra_cmds, ""])

    antes, prompt = load_prompt_content(v["prompt_path"])
    if antes:
        lines.extend(["**Antes de colar o prompt:**", antes, ""])
    lines.extend([
        "**Prompt IA — copiar e colar:**",
        "",
        "```",
        prompt or "*(prompt vazio)*",
        "```",
        "",
        "\\newpage",
        "",
    ])
    return "\n".join(line for line in lines if line is not None)


def main():
    videos = parse_videos()
    preamble = extract_folha_preamble()

    parts = [
        "---",
        "title: FinOps com IA — Manual Completo de Gravação",
        "subtitle: Roteiro, comandos e prompts dos 25 vídeos",
        "lang: pt-BR",
        "geometry: margin=2cm",
        "fontsize: 11pt",
        "documentclass: article",
        "toc: true",
        "toc-depth: 2",
        "---",
        "",
        "# FinOps com IA — Manual Completo de Gravação",
        "",
        "Documento consolidado para gravação do curso: **setup do lab**, **roteiro dos 25 vídeos**, **comandos** e **prompts completos** prontos para copiar.",
        "",
        "> **Exportar PDF:** `./scripts/export-manual-gravacao-pdf.sh`",
        ">",
        "> **Regenerar este arquivo** após editar roteiro ou prompts: `./scripts/generate-manual-gravacao.sh`",
        "",
        "> O lab é montado **na hora**. Use **Last 15 minutes** em todos os dashboards Grafana.",
        "",
        "---",
        "",
        "## Parte 1 — Preparação e setup",
        "",
        preamble,
        "",
        "---",
        "",
        "## Parte 2 — Roteiro e prompts por vídeo",
        "",
    ]

    current_aula = None
    for v in videos:
        aula = v["id"].split(".")[0]
        if aula != current_aula:
            current_aula = aula
            title, dash = AULA_HEADERS[aula]
            parts.extend([
                f"## Aula {aula} — {title}",
                "",
                f"**Dashboard:** `{dash}` | **Prompts:** `ai-prompts/aula-{aula.zfill(2)}/`",
                "",
            ])
        parts.append(render_video(v))

    parts.extend([
        "---",
        "",
        "## Apêndice — Legenda de tipos de vídeo",
        "",
        "| Tipo | Significado |",
        "|------|-------------|",
        "| **T** | Teoria pura — slides + prompt IA, sem lab |",
        "| **T+** | Teoria + demo leve — kubectl ou dashboard estático |",
        "| **T++** | Teoria + demo ativa — scripts, spikes, jobs |",
        "| **H** | Hands-on — demo completa (vídeo X.5) |",
        "",
        "*Gerado automaticamente por `scripts/generate-manual-gravacao.py`*",
    ])

    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"Gerado: {OUT.relative_to(ROOT)} ({len(videos)} vídeos)")


if __name__ == "__main__":
    main()
