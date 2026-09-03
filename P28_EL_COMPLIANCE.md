# Economics Letters — Guide-for-Authors compliance audit

**Manuscript:** *Financing a Concentrated Investment Boom: Evidence from AI* —
S. Chincholikar and R. Chawla. Audited 2026-09-02. Every row below was checked
programmatically against the manuscript source, not asserted from memory; the raw check
output is in `_audit.json`.

Key: **✓ met** · **▲ needs author input before submission** · **N/A**

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
