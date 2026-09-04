# Investment concentration and financing in the AI boom
### Reproducibility artifact — internal cash coverage of the 2022–2025 investment increase

**Authors:** Samir Chincholikar (Independent researcher) · Robin Chawla (Independent researcher, corresponding author)
**ORCID:** [0009-0007-2779-3492](https://orcid.org/0009-0007-2779-3492) · [0009-0007-2807-3948](https://orcid.org/0009-0007-2807-3948)
**Contact:** robin.chawla.cse14@iitbhu.ac.in · samir.chincholikar@gmail.com
**Repository:** https://github.com/samirrc2/financing-concentrated-investment-boom
**Zenodo DOI:** _not yet minted — insert before submission_

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

## Reproduce (offline, deterministic, $0 — no network, no API keys)

```bash
pip install -r requirements.txt      # only matplotlib, and only for the figure
./reproduce.sh
```

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
reproduce.sh              one-command reproduction: claims -> figure -> gate -> length -> PDF
requirements.txt          matplotlib (figure only); numbers need stdlib only
environment.txt           exact versions that produced the committed results
LICENSE                   code MIT · derived data/text CC-BY-4.0 · SEC and BLS data public domain
CITATION.cff              how to cite this artifact
SUBMISSION.md             Economics Letters requirement-by-requirement status and author actions

manuscript.tex / .pdf     THE SUBMISSION (elsarticle; reproducible source)
manuscript_blinded.tex/.pdf   blinded review copy (authors, ORCIDs, affiliation, CRediT removed)
highlights.txt            Economics Letters highlights (5 bullets, <=85 chars each)
figures/Figure_1.pdf/.png figure, vector and 200-dpi raster

claims.json               CANONICAL single source of truth — every number the paper asserts
code/
  engine.py               measurement engine: tag unions, deflation, firm aggregation
  make_claims.py          frozen inputs -> claims.json (idempotent)
  make_figure.py          frozen inputs -> figures/Figure_1.{pdf,png}
  build_gate.py           manuscript -> claims.json audit; fails on any unbacked number
  wordcount.py            Economics Letters length count (main text, notes, captions, refs)
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
