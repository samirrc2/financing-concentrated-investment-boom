#!/usr/bin/env python3
"""Trace any reported figure back to the SEC endpoint it came from.

    python3 code/trace.py --firm Alphabet --series capex --year 2025
    python3 code/trace.py --firm Alphabet --series capex --year 2025 --live
    python3 code/trace.py --firm Amazon --series ocf --year 2021 --live
    python3 code/trace.py --list

For a firm, series and year it prints every XBRL tag the series unions, the value held in the
frozen archive under each tag, the exact URL that value came from, which tag wins the union, and
the deflated figure the paper uses. With --live it re-fetches from the SEC and reports whether the
live value still matches -- a difference reflects a later filing or revised presentation, not an
error, and is exactly why the archive is built from the frozen copies.
"""
import argparse, json, sys, urllib.request
sys.path.insert(0, "code")
from engine import S, P, raw, NAMES, CAPEX, OCF, BUYB, DIV, RND, REV, f500

FRAMES = "https://data.sec.gov/api/xbrl/frames/us-gaap/{tag}/USD/CY{year}.json"
UA = {"User-Agent": "ralph-research (replication check)"}
SERIES = {"capex": ("capital expenditure", CAPEX), "ocf": ("operating cash flow", OCF),
          "buyback": ("share repurchases", BUYB), "dividend": ("dividends", DIV),
          "rnd": ("research and development", RND), "revenue": ("revenue", REV),
          "debt_in": ("long-term debt issued", ["ProceedsFromIssuanceOfLongTermDebt"]),
          "debt_out": ("long-term debt repaid", ["RepaymentsOfLongTermDebt"])}
FOCAL = {"Alphabet": 1652044, "Amazon": 1018724, "Oracle": 1341439,
         "Meta": 1326801, "Microsoft": 789019}


def resolve(name):
    if name in FOCAL:
        return FOCAL[name]
    hits = [(c, NAMES.get(c, "")) for c in f500() if name.lower() in NAMES.get(c, "").lower()]
    if not hits:
        sys.exit(f"no firm in the 500-firm universe matches {name!r}")
    if len(hits) > 1:
        print("matches:", *[f"\n  {c}  {n}" for c, n in hits[:12]]); sys.exit(1)
    return hits[0][0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--firm"); ap.add_argument("--cik", type=int)
    ap.add_argument("--series", default="capex", choices=sorted(SERIES))
    ap.add_argument("--year", type=int, default=2025)
    ap.add_argument("--live", action="store_true", help="re-fetch from the SEC and compare")
    ap.add_argument("--list", action="store_true", help="list series and the five focal firms")
    a = ap.parse_args()

    if a.list:
        print("series:")
        for k, (d, tags) in sorted(SERIES.items()):
            print(f"  {k:9s} {d:28s} unions {len(tags)} tag(s)")
        print("\nfive largest incremental investors:")
        for n, c in FOCAL.items():
            print(f"  {n:10s} CIK {c}")
        return 0

    cik = a.cik or (resolve(a.firm) if a.firm else sys.exit("give --firm or --cik"))
    desc, tags = SERIES[a.series]
    print(f"{NAMES.get(cik, '?')}  (CIK {cik})   {desc}   fiscal year {a.year}\n")
    print(f"{'XBRL tag':58s}{'frozen value':>18}   source")
    best = None
    for t in tags:
        d = raw(t, a.year)
        v = d.get(cik)
        url = FRAMES.format(tag=t, year=a.year)
        print(f"  {t:56s}{('$%.3fbn' % (v / 1e9)) if v is not None else 'not filed':>18}")
        print(f"  {'':56s}{'':18}   {url}")
        if v is not None and (best is None or v > best[1]):
            best = (t, v)
    if best is None:
        print("\n  this firm does not report the series in that year")
        return 0
    print(f"\n  union takes the maximum across tags -> {best[0]}: ${best[1]/1e9:.3f}bn (nominal)")
    if a.year in P:
        print(f"  deflated to 2025 dollars (WPUFD41312, {P[2025]}/{P[a.year]}): "
              f"${best[1] * P[2025] / P[a.year] / 1e9:.3f}bn")

    if a.live:
        print("\n  re-fetching from the SEC ...")
        for t in tags:
            url = FRAMES.format(tag=t, year=a.year)
            try:
                d = json.load(urllib.request.urlopen(
                    urllib.request.Request(url, headers=UA), timeout=90))
            except Exception as e:
                print(f"  {t}: fetch failed ({e})"); continue
            hit = [r for r in d["data"] if r["cik"] == cik]
            frozen = raw(t, a.year).get(cik)
            if not hit:
                print(f"  {t}: not present live" + ("  (was frozen)" if frozen else ""))
                continue
            live = hit[0]["val"]
            same = "MATCHES the frozen copy" if live == frozen else \
                   f"DIFFERS from the frozen ${frozen/1e9:.3f}bn - later filing or revised presentation"
            print(f"  {t}: live ${live/1e9:.3f}bn  accession {hit[0].get('accn')}  -> {same}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
