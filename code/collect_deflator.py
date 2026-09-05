#!/usr/bin/env python3
"""Deflator: BLS series WPUFD41312, final demand--private capital equipment, annual averages.

Every dollar figure in the paper is deflated to 2025 dollars with this series. The BLS public
timeseries API needs no key for a request of this size; annual averages are the M13 period.
Series page: https://data.bls.gov/timeseries/WPUFD41312

Writes data/frozen/deflator_WPUFD41312.json read-only and refuses to overwrite an existing
freeze, matching the other collectors. Run with --check to compare the live series against the
committed freeze without writing anything.
"""
import json, os, sys, urllib.request

SERIES = "WPUFD41312"
API = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
OUT = "data/frozen/deflator_WPUFD41312.json"
YEARS = (2013, 2025)


def fetch():
    """Annual averages, in two requests: the public API caps a query at ten years."""
    out = {}
    for lo, hi in ((YEARS[0], YEARS[0] + 9), (YEARS[0] + 10, YEARS[1])):
        body = json.dumps({"seriesid": [SERIES], "startyear": str(lo), "endyear": str(hi),
                           "annualaverage": True}).encode()
        req = urllib.request.Request(API, data=body, headers={
            "Content-Type": "application/json",
            "User-Agent": "ralph-research samir.chincholikar@gmail.com"})
        d = json.load(urllib.request.urlopen(req, timeout=90))
        if d.get("status") != "REQUEST_SUCCEEDED":
            sys.exit(f"BLS API: {d.get('status')} {d.get('message')}")
        for s in d["Results"]["series"]:
            for r in s["data"]:
                if r["period"] == "M13":            # M13 is the annual average
                    out[r["year"]] = float(r["value"])
    return {str(y): out[str(y)] for y in range(YEARS[0], YEARS[1] + 1)}


if __name__ == "__main__":
    live = fetch()
    if "--check" in sys.argv:
        frozen = json.load(open(OUT))
        bad = [y for y in frozen if frozen[y] != live.get(y)]
        for y in bad:
            print(f"  {y}: frozen {frozen[y]}  live {live.get(y)}")
        print("live series MATCHES the freeze" if not bad
              else f"live series differs in {len(bad)} year(s) - BLS revision since the freeze")
        sys.exit(0)
    if os.path.exists(OUT):
        print("frozen, skipping"); sys.exit(0)
    json.dump(live, open(OUT, "w"), indent=1)
    os.chmod(OUT, 0o444)
    print("FROZEN", OUT)
