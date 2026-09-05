#!/usr/bin/env python3
"""Collect the USES-OF-CASH composition tags from SEC XBRL frames. Free, no key."""
import urllib.request, json, time, os, hashlib, sys
UA={"User-Agent":"ralph-research samir.chincholikar@gmail.com"}
TAGS=["ResearchAndDevelopmentExpense","PaymentsForRepurchaseOfCommonStock",
      "PaymentsOfDividendsCommonStock","NetCashProvidedByUsedInOperatingActivities"]
YEARS=list(range(2013,2026)); OUT="data/frozen/composition_frames.json"
if os.path.exists(OUT): print("frozen file exists — refusing to regenerate."); sys.exit(0)
raw={}
for t in TAGS:
    for y in YEARS:
        u=f"https://data.sec.gov/api/xbrl/frames/us-gaap/{t}/USD/CY{y}.json"
        d=None
        for i in range(4):
            try: d=json.loads(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=90).read()); break
            except Exception as e:
                if getattr(e,"code",None)==404: break
                if i==3: print(f"  FAIL {t} CY{y}",file=sys.stderr)
                time.sleep(2*(i+1))
        raw[f"{t}|{y}"]=[{"cik":r["cik"],"val":r["val"]} for r in d["data"]] if d else []
        time.sleep(0.2)
    print(f"  {t[:44]:46s} done ({sum(len(raw[f'{t}|{y}']) ) for y in YEARS if 0} if 0 else '')".replace("()",""))
json.dump(raw,open(OUT,"w"))
h=hashlib.sha256(open(OUT,"rb").read()).hexdigest(); os.chmod(OUT,0o444)
open("data/frozen/composition_frames.sha256","w").write(h+"  "+OUT+"\n")
print("FROZEN",OUT,"\nSHA256",h)
