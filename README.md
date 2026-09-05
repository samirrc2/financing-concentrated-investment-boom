# Investment concentration and financing in the AI boom
### Reproducibility artifact — internal cash coverage of the 2022–2025 investment increase

**Authors:** Samir Chincholikar (Independent researcher) · Robin Chawla (Independent researcher, corresponding author)
**ORCID:** [0009-0007-2779-3492](https://orcid.org/0009-0007-2779-3492) · [0009-0007-2807-3948](https://orcid.org/0009-0007-2807-3948)
**Contact:** robin.chawla.cse14@iitbhu.ac.in · samir.chincholikar@gmail.com
**Zenodo DOI:** [[DOI PENDING]] — the permanent citable archive
**Repository:** https://github.com/samirrc2/financing-concentrated-investment-boom (working mirror)

## Reproducibility documentation

[`REPRODUCIBILITY_DOCUMENTATION.pdf`](REPRODUCIBILITY_DOCUMENTATION.pdf) is a single, self-contained
companion describing the entire archive: data inputs and provenance, every script and its outputs,
the one-command offline reproduction, the verification and determinism procedure, the environment,
and licensing. It is included in the Zenodo deposit. `DATA_AVAILABILITY.md` is the journal-facing
data statement.

This repository regenerates **every table, figure, and cited number** in the *Economics
Letters* submission *"Investment concentration and financing in the AI boom"* from a single
canonical results file (`claims.json`), and verifies the manuscript against it with a gate
that fails the build if any asserted number cannot be reproduced.

**Headline result.** Among the 500 largest U.S. public companies, ranking the 263 firms with
rising investment by their own cumulative incremental capital expenditure traces a
**rank–coverage gradient**: incremental operating cash flow covers **117%** of the 2022–2025
investment increase at the five largest investors and **102%** at the top ten — which account
for **52.8%** of the increase — but **−61%** across the remaining 213 firms. The pattern is not
a mechanical consequence of concentration: the **more** concentrated 2018–2021 window (41.9%
of its increase at the top five, against 38.9%) instead has the tail as its best-covered
group, as does 2014–2017. Nor is it sectoral composition — dropping regulated, extractive and
financial firms leaves the gradient intact and steeper (117%, 97%, 80%, −324%). Concentrated
investment booms are not internally financed booms as a rule; what is unusual about this one
is that the two coincide.

---

## Verify (one command, single pass/fail)

```bash
pip install -r requirements.txt      # only matplotlib, and only for the figure
./verify.sh
```

`verify.sh` is the referee path. It (1) checks every archived file against
`MANIFEST.sha256`, (2) re-runs the analysis from `data/frozen/`, (3) requires the regenerated
`claims.json` and `Figure_1.png` to be **byte-identical** to the committed ones and names the
offending claim if not, (4) audits every number in the manuscript against `claims.json`, and
(5) checks the length limit. It exits non-zero on any discrepancy and leaves the working tree
untouched. **Runtime: under 10 seconds** on a 2023 laptop.

`./reproduce.sh` is the author path: same pipeline, plus rebuilding `manuscript.pdf`.

**Software.** Python 3.11.5 (standard library only for every number), matplotlib 3.8.0 (figure
only), TeX Live 2024 / pdfTeX 1.40.26 with `elsarticle` (PDF only). Exact versions in
`environment.txt`. No network, no API key, no proprietary source.

`reproduce.sh` (1) regenerates `claims.json` from the frozen source files, (2) redraws
`figures/Figure_1.{pdf,png}` from the same inputs, (3) runs `code/build_gate.py` — which reads
every number out of `manuscript.tex` and **fails if any of them cannot be reproduced from
`claims.json`** — (4) reports the *Economics Letters* length count, and (5) rebuilds the PDF.

> **The numbers reproduce with the Python standard library alone.** `matplotlib` is used only
> to redraw the figure. `claims.json` is byte-identical across repeated runs, and so is
> `figures/Figure_1.png`.

**The deflator is an input, not an output.** The build gate prints the BLS series it used
(`WPUFD41312`, Final demand–Private capital equipment) on every successful run, because a
gate that only compares the manuscript against the code cannot catch the wrong series being
pulled in the first place.

## Repository structure

```
README.md                 this file
verify.sh                 REFEREE PATH: manifest -> re-run -> byte-diff -> gate -> length
reproduce.sh              author path: same pipeline, plus rebuilding manuscript.pdf
MANIFEST.sha256           SHA-256 of every archived file (checked by verify.sh)
.zenodo.json              Zenodo deposit metadata
requirements.txt          matplotlib (figure only); numbers need stdlib only
environment.txt           exact versions that produced the committed results
LICENSE                   code MIT · derived data/text CC-BY-4.0 · SEC and BLS data public domain
CITATION.cff              how to cite this artifact
SUBMISSION.md             Economics Letters requirement-by-requirement status and author actions
REPRODUCIBILITY_DOCUMENTATION.tex/.pdf   single-file companion documenting the whole archive
DATA_AVAILABILITY.md      journal-facing data statement

manuscript.tex / .pdf     THE SUBMISSION (elsarticle; reproducible source)
manuscript_blinded.tex/.pdf   blinded review copy (authors, ORCIDs, affiliation, CRediT removed)
COVER_LETTER.md/.tex/.pdf cover letter (markdown for pasting, LaTeX source, compiled PDF)
highlights.txt            Economics Letters highlights (5 bullets, <=85 chars each)
figures/Figure_1.pdf/.png figure, vector and 200-dpi raster

claims.json               CANONICAL single source of truth — every number the paper asserts
code/
  engine.py               measurement engine: tag unions, deflation, firm aggregation
  make_claims.py          frozen inputs -> claims.json (idempotent)
  make_figure.py          frozen inputs -> figures/Figure_1.{pdf,png}
  build_gate.py           manuscript -> claims.json audit; fails on any unbacked number
  wordcount.py            Economics Letters length count (main text, notes, captions, refs)
  make_manifest.py        regenerates MANIFEST.sha256 from the tracked file list
  reconcile.py            reconciliation of constructed values to as-filed 10-K values
  collect_capex.py        SEC XBRL frames: capital expenditure
  collect_composition.py  SEC XBRL frames: R&D, buybacks, dividends, operating cash flow
  collect_revenue.py      SEC XBRL frames: revenue tags + continuing-operations cash flow
  collect_alt_tags.py     SEC XBRL frames: alternate tags for every key series
  collect_ai_intensity.py SEC EDGAR 10-K text -> pre-specified AI-intensity score
  collect_sic.py          SEC submissions API -> registrant SIC classification

data/
  frozen/                 8 frozen source files, read-only
  SHA256SUMS.txt          SHA-256 of every frozen file
```

## What produces what

Every number in the manuscript comes from `claims.json`, which comes from `data/frozen/`.
Nothing is typed twice.

| Manuscript object | Produced by | Output |
|---|---|---|
| Table 1 (coverage by rank, 2022–2025) | `code/make_claims.py` → `ladder`, `funnel` | `claims.json` |
| Table 2 (earlier four-year windows) | `code/make_claims.py` → `placebo_ladder` | `claims.json` |
| Figure 1(a) internal financing margin | `code/make_figure.py` | `figures/Figure_1.pdf` / `.png` |
| Figure 1(b) Herfindahl concentration | `code/make_figure.py` | `figures/Figure_1.pdf` / `.png` |
| Figure 1(c) coverage through each year | `code/make_figure.py` → `annual` | `figures/Figure_1.pdf` / `.png` |
| §2 sample funnel (500 / 404 / 263 / 141 / 96) | `code/make_claims.py` → `funnel`, `excluded` | `claims.json` |
| §2 single-tag omission (454 filers, $404bn) | `code/make_claims.py` → `alt_tag` | `claims.json` |
| §3.1 leave-one-out and baseline B | `code/make_claims.py` → `leave_one_out_cum`, `cumulative` | `claims.json` |
| §3.2 sectoral decomposition and restricted sample | `code/make_claims.py` → `composition` | `claims.json` |
| Table A1 Panel A (filing attribution) | verbatim from the 10-Ks named in the table | — |
| Table A1 Panel B (AI-intensity cuts) | `code/collect_ai_intensity.py` → `ai_filter` | `claims.json` |
| Table A2 (reconciliation to as-filed values) | `code/reconcile.py` | `claims.json` |
| Table A3 Panels A–C | `code/make_claims.py` → `firm_level`, `composition` | `claims.json` |
| Every asserted number, audited | `code/build_gate.py` | pass/fail |
| Length against the EL limit | `code/wordcount.py` | pass/fail |
| Blinded review copy | `code/make_blinded.py` | `manuscript_blinded.pdf` |

**Raw data provenance.** Firm financials come from the SEC XBRL `frames` API
(`https://data.sec.gov/api/xbrl/frames/`); 10-K text for the AI-intensity measure and the
filing reconciliation from SEC EDGAR; registrant SIC codes from the SEC submissions API; the
deflator from BLS series **WPUFD41312** (Final demand–Private capital equipment). The
`code/collect_*.py` scripts fetch these once and write them read-only. **The results are built
from the frozen copies in `data/frozen/`, not from live endpoints** — re-running a collector
against today's SEC data would pick up subsequent restatements and is not part of
reproduction.

## Design in one paragraph

The unit is a *firm*; the statistic is **internal cash coverage of the incremental
investment**. For each firm, increments are cumulated against a baseline rather than
differenced between two annual observations: ΔX_i = Σ_{t=2022..2025}(X_it − X̄_i), with X̄_i
either the 2021 value (baseline A) or the 2017–2021 average (baseline B), and coverage_i =
ΔOCF_i / ΔCAPEX_i. A firm enters the analysis sample if it is among the 500 U.S. registrants
with the largest fiscal-2024 revenue, reports capital expenditure at both endpoints, and has a
positive cumulative increment — 263 of the 500, on $941 billion of incremental capital
expenditure. Every series unions its alternate XBRL tags, because a single-tag capital-
expenditure series would omit Amazon and 454 other filers representing $404 billion of 2025
spending. Aggregate coverage is the increment-weighted mean of firm-level coverage, so a
group's aggregate places greatest weight on its largest incremental investors — which is why
the aggregate can differ from the financing facing the typical project, and why the paper
reports the ladder rather than a single number.

## Provenance & integrity

- **Frozen inputs.** Every source file is collected once by `code/collect_*.py`, written
  read-only, and SHA-256 fingerprinted in `data/SHA256SUMS.txt`. The collectors refuse to
  overwrite an existing frozen file.
- **Single source of truth.** No number is typed twice. `claims.json` is the only place a
  result is computed; the manuscript is audited against it.
- **Determinism.** `claims.json` and `figures/Figure_1.png` are byte-identical across runs.
- **Audit direction.** The gate reads the manuscript and requires each number to be
  reproducible from `claims.json`, with exemptions listed explicitly in the source (years,
  structural cuts, figures inside quoted 10-K text, BLS series identifiers). It also
  cross-checks quantities reported in two places against each other.
- **Public sources only.** SEC XBRL `frames`, SEC EDGAR filings, and BLS series WPUFD41312.
  No proprietary database, no API key.

## How to cite

See `CITATION.cff`. The Zenodo DOI is recorded there, in the manuscript's Data availability
section, and in `SUBMISSION.md` once minted.

## License

Code: MIT. Derived data, analysis outputs and text: CC-BY-4.0. Underlying raw SEC and BLS
data: U.S. public domain. See `LICENSE`.
