#!/usr/bin/env python3
"""Long-run BEA context via FRED CSV (no key). Annual, 1947-2025."""
import urllib.request,json,os,hashlib,sys,collections
UA={"User-Agent":"Mozilla/5.0 (research; samir.chincholikar@gmail.com)"}
OUT="data/frozen/longrun.json"
if os.path.exists(OUT): print("frozen, skipping"); sys.exit(0)
# Series titles verified against fred.stlouisfed.org/series/<id> before use.
# NOTE: Y033 is ALL equipment, not information processing -- an earlier draft used it in error.
SER={"pnfi":"PNFI",                 # Private Nonresidential Fixed Investment
     "infoproc":"A679RC1Q027SBEA",  # Private fixed investment in INFORMATION PROCESSING equip & software
     "gdp":"GDP",
     "struct":"B009RC1Q027SBEA",    # Nonresidential: Structures
     "equip":"Y033RC1Q027SBEA",     # Nonresidential: Equipment (all)
     "ipp":"Y001RC1Q027SBEA"}       # Nonresidential: Intellectual Property Products
out={}
for k,sid in SER.items():
    try:
        b=urllib.request.urlopen(urllib.request.Request(
          f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}",headers=UA),timeout=90).read().decode()
        ann=collections.defaultdict(list)
        for ln in b.splitlines()[1:]:
            p=ln.split(",")
            if len(p)<2 or p[1] in ("",".") : continue
            ann[int(p[0][:4])].append(float(p[1]))
        out[k]={y:sum(v)/len(v) for y,v in ann.items()}
        ys=sorted(out[k]); print(f"  {k:9s} {sid:22s} {ys[0]}-{ys[-1]}  n={len(ys)}")
    except Exception as e: print(f"  {k}: FAIL {getattr(e,'code',e)}")
json.dump(out,open(OUT,"w")); os.chmod(OUT,0o444)
print("FROZEN",hashlib.sha256(open(OUT,"rb").read()).hexdigest()[:16])
