# Data availability

All data required to reproduce every result are included in this archive. No proprietary data, no
API key and no paid service is needed to reproduce the paper. The archived, citable reproducibility
artifact is deposited on Zenodo: **DOI [10.5281/zenodo.22392416](https://doi.org/10.5281/zenodo.22392416)**. This is the concept DOI: it
represents all versions and always resolves to the latest.

See **[`REPRODUCIBILITY_DOCUMENTATION.pdf`](REPRODUCIBILITY_DOCUMENTATION.pdf)** for the single-file
companion that explains the whole archive (inputs, code, one-command reproduction, verification,
environment, licensing).

## Frozen inputs

All eight live in `data/frozen/`, are written read-only, and are fixed by
`data/SHA256SUMS.txt`. Retrieved recently and frozen.

- `capex_frames.json` — firm-year capital expenditure, 2009–2025, both XBRL tags
  (`PaymentsToAcquirePropertyPlantAndEquipment`, `PaymentsToAcquireProductiveAssets`); 88,097 records.
- `composition_frames.json` — operating cash flow, R&D, repurchases, dividends, 2013–2025; 161,802 records.
- `revenue_frames.json` — revenue (three tags) and continuing-operations cash flow, 2013–2025; 95,605
  records. Revenue ranks the 500-firm universe.
- `financing_frames.json` — long-term-debt issuance and repayment, cash paid for acquisitions,
  2013–2025; 63,293 records.
- `alt_frames.json` — alternate tags for every key series (nine tags), 2013–2025; 270,979 records. The
  union is what makes the measure tag-robust: a single-tag capital-expenditure series would omit
  Amazon and 454 other filers representing $404 billion of 2025 spending.
- `ai_intensity.json` — one scored 10-K per firm (285 scored): dictionary occurrences, total words,
  AI intensity, filing period. The dictionary and cutoffs were fixed before any financing result was
  computed.
- `sic_codes.json` — registrant SIC code and description as filed, for all 500.
- `deflator_WPUFD41312.json` — BLS annual index values, 2013–2025.

## Canonical results

- `claims.json` — the single source of truth. Every number in the manuscript is computed here and
  nowhere else; the manuscript is audited against it.

## Integrity

- `MANIFEST.sha256` fixes every file in the archive; `data/SHA256SUMS.txt` fixes the frozen inputs.
- Verified: `./verify.sh` checks both manifests, re-runs the analysis, and confirms the regenerated
  `claims.json` and `figures/Figure_1.png` are **byte-for-byte** identical to the committed ones —
  offline, in under ten seconds.
- The analysis has no stochastic component: no sampling, no bootstrap, no seed.

## Tracing a figure to its source

`data/SOURCE_URLS.txt` lists the exact URL behind every frozen data point — one line per call
actually made (294 XBRL `frames` calls, 500 submissions-API calls, 285 scored filings, the BLS
series). `code/trace.py` goes the other way: give it a firm, series and year and it prints the
tags, the frozen values, the source URLs, and — with `--live` — whether the SEC still returns the
same figure today.

```
python3 code/trace.py --firm Alphabet --series capex --year 2025 --live
```

## Re-fetchable (not required)

The frozen inputs are the data of record. They are re-fetchable for free from public endpoints — the
SEC requires only a descriptive `User-Agent` header and no API key
(https://www.sec.gov/edgar/sec-api-documentation):

- **XBRL frames:** `https://data.sec.gov/api/xbrl/frames/us-gaap/<tag>/USD/CY<year>.json`, one call
  per tag and calendar year. Collectors: `code/collect_capex.py`, `collect_composition.py`,
  `collect_revenue.py`, `collect_alt_tags.py`.
- **Filing submissions index:** `https://data.sec.gov/submissions/CIK<10-digit-CIK>.json`.
  Collectors: `code/collect_sic.py`, `code/collect_ai_intensity.py`.
- **10-K documents:** `https://www.sec.gov/Archives/edgar/data/<CIK>/<accession>/<document>`.
- **Company facts (audit only):** `https://data.sec.gov/api/xbrl/companyfacts/CIK<10-digit-CIK>.json`,
  used by `code/reconcile.py` for the five focal firms.
- **Deflator:** BLS series `WPUFD41312`, final demand–private capital equipment, annual averages
  via the BLS public timeseries API `https://api.bls.gov/publicAPI/v2/timeseries/data/` (no key
  required at this volume). Collector: `code/collect_deflator.py`; `--check` compares the live series
  against the freeze. Series page: https://data.bls.gov/timeseries/WPUFD41312

**On re-collecting.** The `frames` interface returns the *most recently filed* value for each fact.
Re-collecting today would pick up any filings or revised presentations made since the freeze and
would **not**
reproduce the frozen inputs. That is expected and is why collection sits outside the reproducible
core: the frozen copies are the basis for every figure reported in the paper. Table A2 documents the
one observation where this matters — Meta's 2021 capital expenditure, where a later filing presents
gross purchases alongside the related proceeds.

## Licensing

Code MIT (`LICENSE`); derived data, analysis outputs and text CC-BY-4.0. Underlying raw SEC and BLS
SEC EDGAR public filing content is freely accessible and reusable;
BLS published material is in the U.S. public domain.
