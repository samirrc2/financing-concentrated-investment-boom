#!/usr/bin/env python3
"""Industry classification for the 500-firm universe, from the SEC submissions API.

Collected to support the tail-composition decomposition: the rank-coverage gradient places
utilities, airlines and pipelines at the bottom of the distribution, and the paper needs to say
how much of the gradient is that composition rather than the boom. SIC is the registrant's own
classification as filed, so no judgement enters here.

Writes data/frozen/sic_codes.json: {cik: {"sic": "4911", "desc": "...", "name": "..."}}
"""
import urllib.request, json, time, os, hashlib, sys
sys.path.insert(0, "code")
UA = {"User-Agent": "ralph-research samir.chincholikar@gmail.com"}
OUT = "data/frozen/sic_codes.json"

def get(u, t=60):
    for i in range(3):
        try:
            return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=t).read()
        except Exception as e:
            if getattr(e, "code", None) == 404:
                return None
            if i == 2:
                return None
            time.sleep(1.5 * (i + 1))

from engine import *
F = f500()
res = json.load(open(OUT)) if os.path.exists(OUT) else {}
print(f"resolving SIC for {len(F)} registrants")
for n, cik in enumerate(F, 1):
    if str(cik) in res:
        continue
    sub = get(f"https://data.sec.gov/submissions/CIK{cik:010d}.json")
    if not sub:
        res[str(cik)] = None
    else:
        s = json.loads(sub)
        res[str(cik)] = {"sic": s.get("sic", ""), "desc": s.get("sicDescription", ""),
                         "name": s.get("name", "")}
    if n % 50 == 0:
        json.dump(res, open(OUT, "w"), indent=0); print(f"  {n}/{len(F)}")
    time.sleep(0.12)
json.dump(res, open(OUT, "w"), indent=0)
ok = [v for v in res.values() if v and v.get("sic")]
print(f"DONE: {len(ok)} classified, {len(res)-len(ok)} unavailable")
print("SHA256", hashlib.sha256(open(OUT, "rb").read()).hexdigest()[:16])
