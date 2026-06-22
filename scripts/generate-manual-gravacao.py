#!/usr/bin/env python3
"""Gera docs/manual-gravacao-completo.md — setup, roteiro, comandos, prompts e checklist."""

from pathlib import Path

from recording_data import AULA_META, CHECKLIST_MD, PORT_FORWARDS, VIDEOS, load_prompt

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "manual-gravacao-completo.md"


def render_slides(slides: list[tuple[int, str]]) -> str:
    if not slides:
        return "Nenhum *(hands-on — apenas lab + dashboard + IA)*"
    return "\n".join(f"- Slide {n}: {title}" for n, title in slides)


def render_video(v: tuple) -> str:
    vid, title, tipo, tempo, objetivo, slides, mostrar, cmds, prompt_rel, opcional = v
    aula = vid.split(".")[0]
    _, dashboard = AULA_META[aula]
    prompt_path = f"ai-prompts/{prompt_rel}"
    opt = " *(opcional)*" if opcional else ""
    antes, prompt = load_prompt(prompt_rel)

    lines = [
        f"### Vídeo {vid} — {title}",
        "",
        "| Campo | Valor |",
        "|-------|-------|",
        f"| Tipo | **{tipo}** |",
        f"| Tempo | {tempo} |",
        f"| Dashboard | `{dashboard}` |",
        f"| Prompt | `{prompt_path}`{opt} |",
        "",
        f"**Objetivo:** {objetivo}",
        "",
        "**Slides:**",
        render_slides(slides),
        "",
        "**O que mostrar:**",
        *[f"- {item}" for item in mostrar],
        "",
    ]
    if cmds:
        lines.extend(["**Comandos:**", "", "```bash", cmds, "```", ""])
    else:
        lines.extend(["**Comandos:** Nenhum.", ""])
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
    return "\n".join(lines)


def main() -> None:
    parts = [
        "---",
        "title: FinOps com IA — Manual Completo de Gravação",
        "subtitle: Setup, roteiro, comandos, prompts e checklist dos 25 vídeos",
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
        "Documento **único** para gravação do curso: setup, slides, o que mostrar, comandos, prompts e checklist.",
        "",
        "> **Exportar PDF (opcional):** `./scripts/export-manual-gravacao-pdf.sh`",
        "",
        "> **Regenerar este arquivo** após editar `scripts/recording_data.py` ou prompts: `./scripts/generate-manual-gravacao.sh`",
        "",
        "> O lab é montado **na hora**. Use **Last 15 minutes** em todos os dashboards Grafana.",
        "",
        "---",
        "",
        "## Parte 1 — Preparação e setup",
        "",
        "### Setup global (início de cada dia)",
        "",
        "```bash",
        "minikube start --cpus=4 --memory=8192",
        "./scripts/deploy-lab.sh",
        "./scripts/install-opencost.sh",
        "./scripts/stop-all-anomalies.sh",
        "./scripts/warmup-lab-metrics.sh",
        "```",
        "",
        "### Port-forwards",
        "",
        "| Serviço | Comando | URL |",
        "|---------|---------|-----|",
        "| Grafana | `kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80` | http://localhost:3000 |",
        "| Prometheus | `kubectl port-forward -n monitoring svc/monitoring-kube-prometheus-prometheus 9090:9090` | http://localhost:9090 |",
        "| OpenCost | `kubectl port-forward -n opencost svc/opencost 9003:9090` | http://localhost:9003 |",
        "",
        "### Referência rápida por aula",
        "",
        "| Aula | Dashboard | Port-forwards |",
        "|------|-----------|---------------|",
    ]
    for aula, (_, dash) in AULA_META.items():
        parts.append(f"| {aula} | `{dash}` | {PORT_FORWARDS[aula]} |")
    parts.extend([
        "",
        "### Legenda de tipos",
        "",
        "| Tipo | Significado |",
        "|------|-------------|",
        "| **T** | Teoria — slides + prompt IA, sem lab |",
        "| **T+** | Teoria + demo leve — kubectl ou dashboard estático |",
        "| **T++** | Teoria + demo ativa — scripts, spikes, jobs |",
        "| **H** | Hands-on — demo completa (vídeo X.5) |",
        "",
        "---",
        "",
        "## Parte 2 — Roteiro e prompts por vídeo",
        "",
    ])

    current_aula = None
    for v in VIDEOS:
        aula = v[0].split(".")[0]
        if aula != current_aula:
            current_aula = aula
            titulo, dash = AULA_META[aula]
            parts.extend([
                f"## Aula {aula} — {titulo}",
                "",
                f"**Dashboard:** `{dash}` | **Port-forwards:** {PORT_FORWARDS[aula]}",
                "",
            ])
        parts.append(render_video(v))

    parts.extend([
        "---",
        "",
        "## Parte 3 — Checklist de gravação",
        "",
        CHECKLIST_MD,
        "",
        "*Gerado automaticamente por `scripts/generate-manual-gravacao.py`*",
    ])

    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"Gerado: {OUT.relative_to(ROOT)} ({len(VIDEOS)} vídeos)")


if __name__ == "__main__":
    main()
