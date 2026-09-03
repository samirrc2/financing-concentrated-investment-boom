#!/usr/bin/env python3
"""Corrected measurement engine. Unions alternate tags (the Amazon defect). Frozen inputs only."""
import json, collections
D="data/frozen/"
ST={n:json.load(open(D+n+".json")) for n in
    ["capex_frames","composition_frames","financing_frames","revenue_frames","alt_frames"]}
P={int(k):v for k,v in json.load(open(D+"deflator_WPUFD4131.json")).items()}
YEARS=list(range(2013,2026))
def raw(tag,y):
    for s in ST.values():
        if f"{tag}|{y}" in s:
            d={}
            for r in s[f"{tag}|{y}"]:
                if r["val"] is not None: d[int(r["cik"])]=r["val"]
            return d
    return {}
def union(tags,y,pos=True):
    """max across tags; firms report capex/dividends under different tags."""
    out={}
    for t in tags:
        for c,v in raw(t,y).items():
            if pos and v<=0: continue
            out[c]=max(out.get(c,0),v)
    return out
CAPEX=["PaymentsToAcquirePropertyPlantAndEquipment","PaymentsToAcquireProductiveAssets"]
BUYB =["PaymentsForRepurchaseOfCommonStock","PaymentsForRepurchaseOfEquity"]
DIV  =["PaymentsOfDividendsCommonStock","PaymentsOfDividends"]
OCF  =["NetCashProvidedByUsedInOperatingActivities",
       "NetCashProvidedByUsedInOperatingActivitiesContinuingOperations"]
RND  =["ResearchAndDevelopmentExpense","ResearchAndDevelopmentExpenseExcludingAcquiredInProcessCost"]
REV  =["RevenueFromContractWithCustomerExcludingAssessedTax","Revenues",
       "RevenueFromContractWithCustomerIncludingAssessedTax"]
def series(y):
    return dict(capex=union(CAPEX,y),buyback=union(BUYB,y),dividend=union(DIV,y),
        ocf=union(OCF,y),rnd=union(RND,y),rev=union(REV,y),
        mna=union(["PaymentsToAcquireBusinessesNetOfCashAcquired"],y),
        debt_in=union(["ProceedsFromIssuanceOfLongTermDebt"],y),
        debt_out=union(["RepaymentsOfLongTermDebt"],y),
        eq_in=union(["ProceedsFromIssuanceOfCommonStock","ProceedsFromStockOptionsExercised"],y))
S={y:series(y) for y in YEARS}
R=lambda y:P[2025]/P[y]
def agg(k,ciks,y): return sum(S[y][k].get(c,0) for c in ciks)*R(y)
def names():
    nm={}
    for y in (2024,2025):
        for t in REV:
            for s in ST.values():
                for r in s.get(f"{t}|{y}",[]): nm[int(r["cik"])]=r.get("name","")
    return nm
NAMES=names()
def f500(rank_year=2024,n=500):
    r=S[rank_year]["rev"]
    return [c for c,_ in sorted(r.items(),key=lambda kv:-kv[1])[:n]]
