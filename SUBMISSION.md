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

---

# Guide-for-Authors audit

Checked programmatically against the manuscript source on 2026-09-02.

## A. Format and scope
| # | EL requirement | Status | Evidence |
|---|---|---|---|
| 1 | Letter format, **≤2,000 words excl. references** | ✓ | **1,997** words, Introduction–Conclusion; excludes references, declarations, tables, figures, appendices |
| 2 | Editable source; PDF not accepted as source | ✓ | `P28_main.tex` supplied; `P28_main.pdf` is the review copy |
| 3 | Single column | ✓ | `elsarticle` `preprint` option |
| 4 | No strikethrough/underline | ✓ | none present |
| 5 | One English variety | ✓ | British spelling throughout (`characterise`, `-ised`) |

## B. Title page
| # | Requirement | Status | Evidence |
|---|---|---|---|
| 6 | Concise title, no unestablished abbreviations | ✓ | "AI" is established |
| 7 | Given + family names | ✓ | Samir Chincholikar; Robin Chawla |
| 8 | Affiliation: full name + **postal address + country** | ▲ | Currently "Independent researcher, New York, USA". **Add street address and postal code before submission.** |
| 9 | Corresponding author indicated | ✓ | Robin Chawla, marked with `\cortext` |

## C. Abstract, keywords, highlights, codes
| # | Requirement | Status | Evidence |
|---|---|---|---|
| 10 | Abstract **≤100 words**, self-contained | ✓ | **98** words |
| 11 | No references or non-standard abbreviations in abstract | ✓ | none |
| 12 | Keywords 1–7, avoid "and/of" constructions | ✓ | 5 keywords, none using and/of |
| 13 | **Highlights: separate file, 3–5 bullets, ≤85 characters** | ✓ | `P28_highlights.txt`, 5 bullets, longest **82** characters |
| 14 | JEL codes | ✓ | G31, G32, E22, O32 |

## D. Body, tables, figures
| # | Requirement | Status | Evidence |
|---|---|---|---|
| 15 | Equations editable, numbered; powers of e as `exp` | ✓ | Eqs. (1)–(2) numbered; no `e^` forms present |
| 16 | Tables editable, captioned, notes below, **no vertical rules or shading** | ✓ | 1 table, `booktabs` rules only; 0 vertical rules detected |
| 17 | Figures as separate files with logical names, cited, captioned | ✓ | `figures/Figure_1.pdf` and `.png`; cited as Figure 1 |
| 18 | Vector figures; accessible colour | ✓ | vector PDF plus 200 dpi PNG; two-colour red/grey, distinguished also by line style and marker |
| 19 | GenAI-in-figures disclosure | N/A | figures are matplotlib output from the frozen data; covered by row 24 |
| 20 | Numbered sections; abstract unnumbered | ✓ | §1–§4 numbered, appendices lettered |
| 21 | Conclusion with limitations | ✓ | three limitations stated: no counterfactual, incomplete debt reporting (25%), listed universe only |

## E. References
| # | Requirement | Status | Evidence |
|---|---|---|---|
| 22 | Author–year, alphabetical, **all cited ↔ all listed** | ✓ | **16** references, alphabetical, 0 orphans (verified programmatically) |
| 23 | DOIs where available | ✓ | DOIs on the four working papers; journal articles carry volume and pages |
| 24 | Reference count in line with the field | ✓ | 16, within the 16–30 range of recent accepted EL empirical papers |

## F. Declarations
| # | Requirement | Status | Evidence |
|---|---|---|---|
| 25 | Declaration of competing interest | ✓ | present |
| 26 | Funding statement | ✓ | present, states none |
| 27 | Declaration of generative AI use | ✓ | present, EL wording; states no AI produced or altered any datum, estimate, table or figure |
| 28 | Data statement | ✓ | Data availability section; all inputs public (SEC XBRL, SEC EDGAR, BLS WPUFD4131) |
| 29 | CRediT statement | ✓ | present |
| 30 | Submission declaration (not under review elsewhere) | ▲ | affirm in Editorial Manager |
| 31 | Inclusive language | ✓ | neutral throughout |
| 32–34 | SGBA / human subjects / jurisdictional claims | N/A | none |

## G. Submission mechanics
| # | Requirement | Status | Evidence |
|---|---|---|---|
| 35 | Corresponding author full contact incl. postal and phone | ▲ | supply in Editorial Manager |
| 36 | All files: manuscript, separate figures, highlights | ✓ | see `P28_SUBMISSION_CHECKLIST.md` |
| 37 | Declarations tool completed at submission | ▲ | complete at submission |
| 38 | Permissions for third-party material | ✓ | all data public; quotations from 10-Ks are short and attributed |
| 39 | Submission fee USD 125 (67.50 if eligible) | ▲ | payable at submission |

## Items requiring author action (5)
1. **Postal address** for the affiliation (row 8).
2. Corresponding-author postal address and phone in Editorial Manager (row 35).
3. Submission declaration (row 30).
4. Elsevier declarations tool (row 37).
5. Submission fee, and check PhD/Research4Life eligibility (row 39).
