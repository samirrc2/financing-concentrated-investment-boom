#!/usr/bin/env python3
"""Alternate tags for every key series — the Amazon defect proved single-tag measures are unsafe.
Also pulls the components needed to test whether a full cash-flow bridge closes."""
import urllib.request,json,time,os,hashlib,sys
UA={"User-Agent":"ralph-research samir.chincholikar@gmail.com"}
TAGS=["PaymentsForRepurchaseOfEquity","PaymentsOfDividends",
      "PaymentsOfDividendsCommonStockAndPreferredStock",
      "ProceedsFromIssuanceOfCommonStock","ProceedsFromStockOptionsExercised",
      "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalentsPeriodIncreaseDecreaseIncludingExchangeRateEffect",
      "NetCashProvidedByUsedInInvestingActivities","NetCashProvidedByUsedInFinancingActivities",
      "ResearchAndDevelopmentExpenseExcludingAcquiredInProcessCost"]
OUT="data/frozen/alt_frames.json"
if os.path.exists(OUT): print("frozen, skipping"); sys.exit(0)
raw={}
for t in TAGS:
    n=0
    for y in range(2013,2026):
        d=None
        for i in range(4):
            try:
                d=json.loads(urllib.request.urlopen(urllib.request.Request(
                  f"https://data.sec.gov/api/xbrl/frames/us-gaap/{t}/USD/CY{y}.json",headers=UA),timeout=90).read()); break
            except Exception as e:
                if getattr(e,"code",None)==404: break
                time.sleep(2*(i+1))
        raw[f"{t}|{y}"]=[{"cik":r["cik"],"val":r["val"]} for r in d["data"]] if d else []
        n+=len(raw[f"{t}|{y}"]); time.sleep(0.2)
    print(f"  {t[:58]:60s} {n:,}")
json.dump(raw,open(OUT,"w")); os.chmod(OUT,0o444)
print("FROZEN",hashlib.sha256(open(OUT,"rb").read()).hexdigest()[:16])
