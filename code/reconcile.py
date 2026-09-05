#!/usr/bin/env python3
"""Appendix B. Reconciles each constructed observation to a 10-K-reported value for the SAME
fiscal period. The frames API assigns a fiscal year to the calendar year containing most of its
months, so off-calendar filers must be matched on period, not on label."""
import urllib.request, json, sys, time, datetime
sys.path.insert(0,"code")
UA={"User-Agent":"ralph-research samir.chincholikar@gmail.com"}
FIRMS={1652044:"Alphabet",1018724:"Amazon",1341439:"Oracle",1326801:"Meta",789019:"Microsoft"}
SERIES={"capex":["PaymentsToAcquirePropertyPlantAndEquipment","PaymentsToAcquireProductiveAssets"],
        "ocf":["NetCashProvidedByUsedInOperatingActivities",
               "NetCashProvidedByUsedInOperatingActivitiesContinuingOperations"],
        "buyback":["PaymentsForRepurchaseOfCommonStock","PaymentsForRepurchaseOfEquity"],
        "dividend":["PaymentsOfDividendsCommonStock","PaymentsOfDividends"],
        "rnd":["ResearchAndDevelopmentExpense",
               "ResearchAndDevelopmentExpenseExcludingAcquiredInProcessCost"],
        "debt_in":["ProceedsFromIssuanceOfLongTermDebt"],
        "debt_out":["RepaymentsOfLongTermDebt"]}
def J(u,tries=4):
    for i in range(tries):
        try: return json.loads(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=180).read())
        except Exception as e:
            if getattr(e,"code",None)==404: return None
            if i==tries-1: return None
            time.sleep(2*(i+1))
FR={}
for key,tags in SERIES.items():
    for t in tags:
        for y in (2021,2025):
            d=J(f"https://data.sec.gov/api/xbrl/frames/us-gaap/{t}/USD/CY{y}.json")
            if d: FR[(t,y)]={int(r["cik"]):r for r in d["data"]}
CF={c:J(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{c:010d}.json") for c in FIRMS}
rows=[]; period_note=[]
print(f"{'firm':<10}{'series':<9}{'yr':>5}{'frames $bn':>12}{'10-K $bn':>11}{'diff%':>8}  fiscal period matched")
for cik,name in FIRMS.items():
    cf=CF[cik]
    for key,tags in SERIES.items():
        for y in (2021,2025):
            fr=None; tag=None
            for t in tags:
                if (t,y) in FR and cik in FR[(t,y)]: fr=FR[(t,y)][cik]; tag=t; break
            if not fr: continue
            start,end,val=fr.get("start"),fr.get("end"),fr["val"]
            filed=None
            for u in cf["facts"]["us-gaap"].get(tag,{}).get("units",{}).get("USD",[]):
                if u.get("form")=="10-K" and u.get("start")==start and u.get("end")==end:
                    filed=u["val"]; break
            if filed is None: continue
            pct=(val-filed)/filed*100 if filed else 0.0
            rows.append(dict(firm=name,series=key,year=y,frames=val,filed=filed,pct=pct,start=start,end=end))
            print(f"{name:<10}{key:<9}{y:>5}{val/1e9:>12,.2f}{filed/1e9:>11,.2f}{pct:>8.2f}  {start}..{end}")
            if end[:4]!=str(y): period_note.append((name,y,start,end))
ok=sum(1 for r in rows if abs(r['pct'])<0.01)
print(f"\n  observations reconciled: {len(rows)}; exact match: {ok} ({ok/len(rows)*100:.0f}%)")
bad=[r for r in rows if abs(r['pct'])>=0.01]
print("  discrepancies:", "none" if not bad else "")
for r in bad: print(f"    {r['firm']} {r['series']} {r['year']}: {r['pct']:+.3f}%")
print("\n  FISCAL-PERIOD NOTE — observations whose fiscal year does not end in the labelled year:")
for n,y,s,e in sorted(set(period_note)): print(f"    {n} {y}: {s}..{e}")
json.dump(rows,open("tables/reconciliation.json","w"),indent=1)
