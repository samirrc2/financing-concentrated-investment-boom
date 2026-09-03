#!/usr/bin/env python3
"""AI-exposure filter, constructed from 10-K text BEFORE any financing outcome is examined.

PRE-SPECIFICATION (declared here, frozen before the subsample analysis is run):
  Dictionary follows the text-based AI-disclosure approach used in the firm-level AI-engagement
  literature (Ante & Saggu; earnings-call AI-terminology measures). Terms fixed in advance:
    AI_TERMS      -- model/method vocabulary
    COMPUTE_TERMS -- buildout/infrastructure vocabulary
  Score: AI_INTENSITY = 10,000 * (AI term occurrences) / (total words in the 10-K).
  Cutoffs fixed in advance: AI-exposed = top decile; robustness at top quintile.
  No term was added, removed, or reweighted after inspecting any financing result.
"""
import urllib.request, json, re, time, os, sys, hashlib
sys.path.insert(0,"scripts")
UA={"User-Agent":"ralph-research samir.chincholikar@gmail.com"}
AI_TERMS=["artificial intelligence","machine learning","generative ai","deep learning",
          "neural network","large language model","foundation model","ai model",
          "ai capabilities","ai infrastructure","accelerated computing"]
COMPUTE_TERMS=["data center","data centre","graphics processing unit","gpu",
               "compute capacity","accelerator","training cluster","inference capacity"]
OUT="data/frozen/ai_intensity.json"
CACHE="data/ai_text_cache.json"
def get(u,t=120):
    for i in range(3):
        try: return urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=t).read()
        except Exception as e:
            if getattr(e,"code",None)==404: return None
            if i==2: return None
            time.sleep(1.5*(i+1))
from engine import *
F=f500()
# score only firms that enter the coverage analysis (positive cumulative incremental capex)
def cf(c,k):
    b=agg(k,{c},2021); return sum(agg(k,{c},t)-b for t in range(2022,2026))/1e9
TARGETS=[c for c in F if cf(c,'capex')>0]
print(f"scoring {len(TARGETS)} firms (those with positive cumulative incremental capex)")
res=json.load(open(OUT)) if os.path.exists(OUT) else {}
for n,cik in enumerate(TARGETS,1):
    if str(cik) in res: continue
    sub=get(f"https://data.sec.gov/submissions/CIK{cik:010d}.json")
    if not sub: res[str(cik)]=None; continue
    s=json.loads(sub); r=s["filings"]["recent"]
    idx=[i for i,f in enumerate(r["form"]) if f=="10-K"]
    if not idx: res[str(cik)]=None; continue
    i=idx[0]
    url=f"https://www.sec.gov/Archives/edgar/data/{cik}/{r['accessionNumber'][i].replace('-','')}/{r['primaryDocument'][i]}"
    raw=get(url,180)
    if not raw: res[str(cik)]=None; continue
    txt=re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",raw.decode("utf8","ignore"))).lower()
    tot=len(txt.split())
    if tot<1000: res[str(cik)]=None; continue
    ai=sum(txt.count(t) for t in AI_TERMS)
    cp=sum(txt.count(t) for t in COMPUTE_TERMS)
    res[str(cik)]={"name":s.get("name",""),"words":tot,"ai_hits":ai,"compute_hits":cp,
                   "ai_intensity":round(10000*ai/tot,3),"compute_intensity":round(10000*cp/tot,3),
                   "period":r["reportDate"][i]}
    if n%25==0:
        json.dump(res,open(OUT,"w")); print(f"  {n}/{len(TARGETS)} scored")
    time.sleep(0.12)
json.dump(res,open(OUT,"w"))
ok=[v for v in res.values() if v]
print(f"\nDONE: {len(ok)} scored, {len(res)-len(ok)} unavailable")
print("SHA256",hashlib.sha256(open(OUT,"rb").read()).hexdigest()[:16])
