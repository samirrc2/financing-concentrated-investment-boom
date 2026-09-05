#!/usr/bin/env bash
# Rebuilds every number, table, figure and the PDF from the frozen source files.
set -euo pipefail
python3 code/make_claims.py      # regenerates claims.json from data/frozen/
python3 code/make_figure.py      # regenerates figures/ from data/frozen/
python3 code/build_gate.py       # fails if any manuscript number disagrees with claims.json
python3 code/wordcount.py || echo "WARNING: over the Economics Letters length limit"
pdflatex -interaction=nonstopmode manuscript.tex >/dev/null
pdflatex -interaction=nonstopmode manuscript.tex >/dev/null
python3 code/make_docx.py           # Word version, generated from the same .tex
echo "OK -> manuscript.pdf, manuscript.docx"
