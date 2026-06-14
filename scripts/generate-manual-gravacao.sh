#!/usr/bin/env bash
# Regenera docs/manual-gravacao-completo.md a partir do roteiro e dos prompts por vídeo.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/generate-manual-gravacao.py
