#!/usr/bin/env python3
"""Write data/SOURCE_URLS.txt: the exact, working URL behind every frozen data point.

One line per call actually made. A reviewer can open any of these in a browser and compare the
value against the frozen copy, or run code/trace.py to do the comparison automatically.
"""
import json, os, sys
sys.path.insert(0, "code")

FRAMES = "https://data.sec.gov/api/xbrl/frames/us-gaap/{tag}/USD/CY{year}.json"
SUBS = "https://data.sec.gov/submissions/CIK{cik:010d}.json"
FILES = ["capex_frames", "composition_frames", "revenue_frames", "financing_frames", "alt_frames"]

out = ["# Exact source URLs behind every frozen data point in this archive.",
       "# Retrieved 2-4 September 2026. No API key required; the SEC asks only for a",
       "# descriptive User-Agent header. See https://www.sec.gov/search-filings/edgar-application-programming-interfaces",
       "#", "# Format:  <frozen file>  <tag>|<year>  <url>", ""]

n_frames = 0
out.append("## SEC XBRL frames - one call per tag and calendar year")
for f in FILES:
    d = json.load(open(f"data/frozen/{f}.json"))
    for key in sorted(d, key=lambda k: (k.split("|")[0], int(k.split("|")[1]))):
        tag, year = key.split("|")
        out.append(f"data/frozen/{f}.json  {key}  " + FRAMES.format(tag=tag, year=year))
        n_frames += 1

sic = json.load(open("data/frozen/sic_codes.json"))
out += ["", "## SEC submissions API - registrant classification and 10-K location, one call per firm"]
for cik in sorted(sic, key=int):
    nm = (sic[cik] or {}).get("name", "")
    out.append(f"data/frozen/sic_codes.json  CIK{int(cik):010d}  {SUBS.format(cik=int(cik))}  # {nm}")

ai = json.load(open("data/frozen/ai_intensity.json"))
scored = [c for c, v in ai.items() if v]
out += ["", "## SEC EDGAR 10-K documents - AI-intensity scoring",
        f"# {len(scored)} filings were scored. Each firm's most recent 10-K is located through the",
        "# submissions URL above; the filing period scored is recorded in ai_intensity.json.",
        "# Document URLs follow https://www.sec.gov/Archives/edgar/data/<CIK>/<accession>/<document>"]
for c in sorted(scored, key=int):
    out.append(f"data/frozen/ai_intensity.json  CIK{int(c):010d}  period {ai[c]['period']}  "
               f"{SUBS.format(cik=int(c))}  # {ai[c]['name']}")

out += ["", "## BLS deflator",
        "data/frozen/deflator_WPUFD41312.json  WPUFD41312  https://data.bls.gov/timeseries/WPUFD41312"
        "  # Final demand-Private capital equipment, annual averages"]

open("data/SOURCE_URLS.txt", "w").write("\n".join(out) + "\n")
print(f"data/SOURCE_URLS.txt: {n_frames} frames calls, {len(sic)} submissions calls, "
      f"{len(scored)} scored filings, 1 BLS series")
