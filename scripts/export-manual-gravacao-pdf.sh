#!/usr/bin/env bash
# Exporta docs/manual-gravacao-completo.md para PDF.
set -euo pipefail
cd "$(dirname "$0")/.."

MD="docs/manual-gravacao-completo.md"
PDF="docs/manual-gravacao-completo.pdf"

if [[ ! -f "$MD" ]]; then
  echo "Gerando manual..."
  ./scripts/generate-manual-gravacao.sh
fi

if ! command -v pandoc >/dev/null 2>&1; then
  echo "Erro: pandoc não encontrado."
  echo ""
  echo "Instale no Mac:"
  echo "  brew install pandoc basictex"
  echo ""
  echo "Alternativa sem pandoc — abra o Markdown e exporte:"
  echo "  1. VS Code / Cursor: extensão 'Markdown PDF'"
  echo "  2. Ou abra $MD no Typora / MacDown → Exportar PDF"
  echo "  3. Ou: npx md-to-pdf $MD"
  exit 1
fi

echo "Exportando $PDF ..."
pandoc "$MD" -o "$PDF" \
  --pdf-engine=pdflatex \
  -V geometry:margin=2cm \
  -V fontsize=11pt \
  -V documentclass=article \
  --toc \
  --toc-depth=2 \
  -V lang=pt-BR \
  2>/dev/null || pandoc "$MD" -o "$PDF" \
  --pdf-engine=xelatex \
  -V geometry:margin=2cm \
  -V fontsize=11pt \
  -V mainfont="Helvetica" \
  --toc \
  --toc-depth=2

echo "Pronto: $PDF"
