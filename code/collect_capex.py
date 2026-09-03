#!/usr/bin/env python3
"""Paper 28 PILOT collection. Public data only. Zero API cost, zero LLM calls.
Source: SEC XBRL 'frames' API (data.sec.gov) — free, no key, all filers.
Writes data/frozen/capex_frames.json (raw, hashed, never regenerated)."""
import urllib.request, json, time, os, hashlib, sys

UA = {"User-Agent": "ralph-research samir.chincholikar@gmail.com"}
TAGS = ["PaymentsToAcquirePropertyPlantAndEquipment",   # primary
        "PaymentsToAcquireProductiveAssets"]            # robustness alternate
YEARS = list(range(2009, 2026))
OUT = "data/frozen/capex_frames.json"

def frame(tag, year, tries=4):
    u = f"https://data.sec.gov/api/xbrl/frames/us-gaap/{tag}/USD/CY{year}.json"
    for i in range(tries):
        try:
            return json.loads(urllib.request.urlopen(
                urllib.request.Request(u, headers=UA), timeout=90).read())
        except Exception as e:
            code = getattr(e, "code", None)
            if code == 404: return None                 # tag not reported that year
            if i == tries - 1:
                print(f"  FAIL {tag} CY{year}: {code or e}", file=sys.stderr); return None
            time.sleep(2 * (i + 1))

if os.path.exists(OUT):
    print("frozen file already exists — refusing to regenerate (guardrail).")
    sys.exit(0)

raw = {}
for tag in TAGS:
    for y in YEARS:
        d = frame(tag, y)
        n = len(d["data"]) if d else 0
        raw[f"{tag}|{y}"] = [
            {"cik": r["cik"], "name": r["entityName"], "val": r["val"]}
            for r in d["data"]] if d else []
        print(f"  {tag[:38]:40s} CY{y}: {n:5d} filers")
        time.sleep(0.25)

os.makedirs("data/frozen", exist_ok=True)
with open(OUT, "w") as f:
    json.dump(raw, f)
h = hashlib.sha256(open(OUT, "rb").read()).hexdigest()
os.chmod(OUT, 0o444)
print(f"\nFROZEN {OUT}\nSHA256 {h}")
open("data/frozen/capex_frames.sha256", "w").write(h + "  " + OUT + "\n")
