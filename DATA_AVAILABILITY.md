# Data availability — Paper 28
All raw inputs are public and free. No proprietary database (no WRDS/Compustat) is used.

| file | source | key required |
|---|---|---|
| capex_frames.json      | SEC XBRL frames, PaymentsToAcquirePropertyPlantAndEquipment | no |
| composition_frames.json| SEC XBRL frames: R&D, buybacks, dividends, operating cash flow | no |
| financing_frames.json  | SEC XBRL frames: LT debt issued/repaid, cash paid for acquisitions | no |
| revenue_frames.json    | SEC XBRL frames: 3 revenue tags + continuing-ops cash flow | no |
| deflator_WPUFD4131.json| BLS PPI final demand, private capital equipment (flat-file archive) | no |
| employees.json         | Financial Modeling Prep historical-employee-count | yes (not committed) |

Every file is chmod 444 with its SHA-256 recorded in claims.json. Analysis reads only frozen
files. `scripts/build_gate.py` fails the build if any manuscript number disagrees.
