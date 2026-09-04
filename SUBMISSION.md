# Submission checklist — Economics Letters

**Manuscript:** *Investment concentration and financing in the AI boom*
Samir Chincholikar · Robin Chawla · prepared 2026-09-04

## Hard requirements
| Item | Requirement | Status |
|---|---|---|
| Word count | ≤2,000 incl. main text, table notes, captions, references | **1,953** ✓ (`code/wordcount.py`) |
| Abstract | ≤100 words | **97** ✓ |
| Highlights | separate file, 3–5 bullets, ≤85 chars | 5 bullets, longest **81** ✓ |
| Tables | editable, no vertical rules | 2 tables, 0 vertical rules ✓ |
| Figures | separate files, vector | `Figure_1.pdf` + `.png`, three panels ✓ |
| References | all cited ↔ all listed | **13**, 0 orphans ✓ |
| JEL codes | present | G31, G32, E22, O32 ✓ |
| Keywords | 1–7, no "and/of" | 5 ✓ |
| Source file | .tex, not PDF | `manuscript.tex` ✓ |
| Declarations | competing interest, funding, GenAI, data | all present ✓ |
| Build | 0 errors, 0 overfull boxes, 0 undefined refs | ✓ (8 pages) |
| Numbers | every manuscript figure machine-verified | `build_gate.py` **174 asserted, 174 reproduced** ✓ |
| Determinism | repeated runs byte-identical | `claims.json` and `Figure_1.png` ✓ |

## Files to upload
| File | Role |
|---|---|
| `manuscript.tex` | manuscript source (required; PDF is not accepted as source) |
| `manuscript.pdf` | review copy |
| `manuscript_blinded.pdf` | blinded copy, if the journal requests one |
| `highlights.txt` | highlights (separate item in Editorial Manager) |
| `figures/Figure_1.pdf` | figure, vector |
| `figures/Figure_1.png` | figure, raster fallback |

## Replication archive (for the data statement / Zenodo)
| Path | Contents |
|---|---|
| `data/frozen/` | 8 frozen source files, read-only |
| `data/SHA256SUMS.txt` | SHA-256 of every frozen file |
| `claims.json` | machine-generated source of every number in the manuscript |
| `code/` | collectors, engine, claims builder, figure builder, build gate, word count |
| `reproduce.sh` | regenerates all numbers and the figure, gates the manuscript, rebuilds the PDF |
| `CITATION.cff`, `environment.txt`, `requirements.txt`, `LICENSE` | citation, environment, licence |

## Numbers a referee will check first
- Coverage ladder: 117% (top 5) → 102% (top 10) → 82% (top 20) → 53% (top 50) → **−61%** (remaining 213).
- Top ten = **52.8%** of the $941bn cumulative incremental capital expenditure.
- Placebo: 2018–2021 is **more** concentrated (41.9% vs 38.9%) yet has the tail best covered.
- Sectoral: dropping regulated, extractive and financial firms gives 117 / 97 / 90 / 80 / **−324%**.
- Sample funnel reconciles: 500 = 404 both endpoints + 96 missing an endpoint; 404 = 263 positive + 141 not.
- Leave-one-out: coverage remains at least **79%** omitting any single one of the five.
- Reconciliation: 49 observations for the five focal firms, 48 exact, 1 matches Meta's restated figure.

## Known limitations stated in the paper
1. Accounting decomposition of realised flows; no counterfactual identified (§3.3 ii).
2. Selection on an observed 2021 baseline and a positive increment (§3.3 i); §3.1 reports the unrestricted contrast.
3. Listed registrants only; private firms and special-purpose vehicles outside by construction (§3.3 iii).
4. Cumulative coverage is not monotone across the first three cuts (63%, 68%, 117%) — stated in §3.1.
5. Microsoft's and Oracle's fiscal years fall either side of the December endpoint (Table A2).
6. The AI-intensity cut is a relabelled sample, not an independent one — the five are 92.8% of the top decile (Table A1).

## Author actions before submitting
1. Add **postal address** to the affiliation (`manuscript.tex`, `\affiliation`).
2. Supply corresponding-author postal address and phone in Editorial Manager.
3. Affirm the submission declaration.
4. Complete the Elsevier declarations tool.
5. Pay the USD 125 fee (USD 67.50 if PhD-student or Research4Life eligible).
6. Mint the Zenodo DOI and insert it in `CITATION.cff`, `README.md` and the Data availability section.
7. Decide whether the GitHub repository stays public during review (a distinctive phrase search de-anonymises the blinded copy).

## Not done
- No `.docx` version. EL accepts LaTeX source, so this is optional; produce one only if the editor asks.
- Zenodo DOI not minted; the Data availability section currently says the archive is withheld during review.
