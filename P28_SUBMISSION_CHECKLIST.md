# P28 — SUBMISSION CHECKLIST (Economics Letters)

**Manuscript:** *Financing a Concentrated Investment Boom: Evidence from AI*
Samir Chincholikar · Robin Chawla · prepared 2026-09-02

## Hard requirements
| Item | Requirement | Status |
|---|---|---|
| Body word count | ≤2,000 excl. references | **1,997** ✓ |
| Abstract | ≤100 words | **98** ✓ |
| Highlights | separate file, 3–5 bullets, ≤85 chars | 5 bullets, longest **82** ✓ |
| Tables | editable, no vertical rules | 1 table, 0 vertical rules ✓ |
| Figures | separate files, vector | `Figure_1.pdf` + `.png` ✓ |
| References | all cited ↔ all listed | **16**, 0 orphans ✓ |
| JEL codes | present | G31, G32, E22, O32 ✓ |
| Keywords | 1–7, no "and/of" | 5 ✓ |
| Source file | .tex, not PDF | `P28_main.tex` ✓ |
| Declarations | competing interest, funding, GenAI, data, CRediT | all present ✓ |
| Build | 0 errors, 0 overfull boxes, 0 undefined refs | ✓ |
| Numbers | every manuscript figure machine-verified | `build_gate.py` **319 assertions, 181 cited, all reconcile** ✓ |

## Files to upload
| File | Role |
|---|---|
| `P28_main.tex` | manuscript source (required; PDF is not accepted as source) |
| `P28_main.pdf` | review copy |
| `P28_highlights.txt` | highlights (separate item in Editorial Manager) |
| `figures/Figure_1.pdf` | figure, vector |
| `figures/Figure_1.png` | figure, raster fallback |
| `P28_SSRN_abstract.txt` | for the optional SSRN preprint |

## Replication archive (for the data statement / Zenodo)
| Path | Contents |
|---|---|
| `data/frozen/` | 11 frozen source files, read-only |
| `data/SHA256SUMS.txt` | SHA-256 of every frozen file |
| `claims.json` | machine-generated source of every number in the manuscript |
| `code/` | collection scripts, `engine.py`, `make_claims.py`, `build_gate.py`, `reconcile.py` |
| `reproduce.sh` | regenerates all numbers, then the PDF |
| `CITATION.cff`, `environment.txt`, `requirements.txt` | citation and environment metadata |

## Numbers a referee will check first
- Coverage ladder: 118% (top 5) → 104% (top 10) → 84% (top 20) → 55% (top 50) → **−7%** (remaining 217).
- Net new debt: −$3bn at the top five against **+$280bn** in the tail.
- Top ten = **52.5%** of the $959bn cumulative incremental capital expenditure.
- AI-exposed top decile: coverage **128%**, net new debt −$24bn (27 firms).
- Sample: 500 universe → 404 report capex both years → **267** analysis firms → 87% of 2025 capex.
- Reconciliation: 49 observations for the five focal firms, 48 exact, 1 matches Meta's restated figure.

## Known limitations stated in the paper
1. Accounting decomposition of realised flows; no counterfactual identified.
2. Debt reporting covers only 25% of the universe at both endpoints.
3. Listed registrants only; silent on private firms and off-balance-sheet vehicles.
4. Coverage is not monotone across the first three cuts (67%, 70%, 118%) — stated explicitly in §3.1.
5. Oracle's fiscal year ends in May, so its 2025 observation runs to May 2026 (SEC convention retained).
6. The AI-intensity filter admits firms that discuss AI without building infrastructure; disclosed in Appendix D.

## Author actions before submitting (5)
1. Add **postal address** to the affiliation (`P28_main.tex`, `\affiliation`).
2. Supply corresponding-author postal address and phone in Editorial Manager.
3. Affirm the submission declaration.
4. Complete the Elsevier declarations tool.
5. Pay the USD 125 fee (USD 67.50 if PhD-student or Research4Life eligible).

## Not done
- No `.docx` version. EL accepts LaTeX source, so this is optional; produce one only if the editor asks.
- Zenodo DOI not minted; the Data availability section will need the DOI inserted once it is.
