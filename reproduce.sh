#!/usr/bin/env bash
# Rebuilds every number, table and figure from the frozen source files.
set -euo pipefail
python3 code/make_claims.py      # regenerates claims.json from data/frozen/
python3 code/build_gate.py       # fails if any manuscript number disagrees with claims.json
pdflatex -interaction=nonstopmode manuscript.tex >/dev/null
pdflatex -interaction=nonstopmode manuscript.tex >/dev/null
echo "OK -> manuscript.pdf"
