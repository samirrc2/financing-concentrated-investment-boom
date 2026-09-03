# Investment Concentration and Internal Finance in the AI Boom

Replication archive for the Economics Letters submission.
Samir Chincholikar · Robin Chawla

## Reproduce

    ./reproduce.sh

Regenerates `claims.json` from the frozen source files, verifies every number in the
manuscript against it, and rebuilds the PDF. Requires Python 3.11+, `matplotlib`, and a
LaTeX installation with `elsarticle`, `siunitx`, `tabularx`, `microtype` and `booktabs`.

## Layout

| Path | Contents |
|---|---|
| `manuscript.tex` / `.pdf` | manuscript source and review copy |
| `highlights.txt` | Economics Letters highlights (separate upload) |
| `SUBMISSION.md` | checklist, key numbers, Guide-for-Authors audit, author actions |
| `figures/Figure_1.pdf` / `.png` | figure, vector and raster |
| `data/frozen/` | frozen source files, read-only |
| `data/SHA256SUMS.txt` | SHA-256 of every frozen file |
| `claims.json` | machine-generated source of every number in the manuscript |
| `code/` | collection scripts, analysis engine, claims builder, build gate |

## Data

Every input is public and free:

- Firm financials — SEC XBRL `frames` API, `https://data.sec.gov/api/xbrl/frames/`
- 10-K text for the AI-exposure measure and the filing reconciliation — SEC EDGAR
- Deflator — Bureau of Labor Statistics series WPUFD4131

Per-file provenance:

| file | source | key required |
|---|---|---|
| capex_frames.json      | SEC XBRL frames, PaymentsToAcquirePropertyPlantAndEquipment | no |
| composition_frames.json| SEC XBRL frames: R&D, buybacks, dividends, operating cash flow | no |
| financing_frames.json  | SEC XBRL frames: LT debt issued/repaid, cash paid for acquisitions | no |
| revenue_frames.json    | SEC XBRL frames: 3 revenue tags + continuing-ops cash flow | no |
| deflator_WPUFD4131.json| BLS PPI final demand, private capital equipment (flat-file archive) | no |
| employees.json         | Financial Modeling Prep historical-employee-count | yes (not committed) |

No proprietary database is used. `code/build_gate.py` fails the build if any number in the
manuscript disagrees with `claims.json`. Environment: Python 3.11, matplotlib; LaTeX with
`elsarticle`, `siunitx`, `tabularx`, `microtype`, `booktabs`, `seqsplit`, `caption`, `lmodern`.
