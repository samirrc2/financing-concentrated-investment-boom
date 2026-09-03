#!/usr/bin/env python3
"""Single source of truth (v2, post-audit). Option B: resource-allocation decomposition.
Corrections vs v1: (1) capex/dividends/buybacks union alternate tags -- Amazon and 448 other
firms tag capex as PaymentsToAcquireProductiveAssets; (2) R&D is NOT a financed use (it is
already inside CFO) and is reported only as an allocation ratio; (3) no closure claim."""
import sys, json, statistics as st; sys.path.insert(0,"code")
from engine import *
F=f500(); AI5={1652044,1018724,1341439,1326801,789019}
NAME={1652044:"Alphabet",1018724:"Amazon",1341439:"Oracle",1326801:"Meta",789019:"Microsoft"}
REST=set(F)-AI5
def sh(ciks,y,k,den="ocf"): return agg(k,ciks,y)/agg(den,ciks,y)*100
def blk(ciks,y,den="ocf"): return {k:round(sh(ciks,y,k,den),1) for k in ("capex","buyback","rnd","dividend")}
C={"universe":{"n":len(F),"rev_fy2024_tn":round(sum(S[2024]['rev'][c] for c in F)/1e12,2),
   "ai5":[NAME[c] for c in sorted(AI5,key=lambda c:-(S[2025]['capex'].get(c,0)*R(2025)-S[2021]['capex'].get(c,0)*R(2021)))],
   "n_rest":len(REST),"deflator":"BLS PPI WPUFD4131","years":[2013,2025]}}
# mechanical rule
inc={c:(S[2025]['capex'].get(c,0)*R(2025)-S[2021]['capex'].get(c,0)*R(2021)) for c in F}
rk=sorted(inc.items(),key=lambda kv:-kv[1]); tot=agg('capex',F,2025)-agg('capex',F,2021)
C["rule"]={"aggregate_increase_bn":round(tot/1e9),
  "top5_share_pct":round(sum(v for _,v in rk[:5])/tot*100,1),
  "rank":[{"n":NAMES.get(c,'?')[:28],"inc_bn":round(v/1e9,1)} for c,v in rk[:7]],
  "gap_5_to_6":round(rk[4][1]/rk[5][1],1)}
# main allocation shares
C["shares"]={g:{str(y):blk(ck,y) for y in YEARS} for g,ck in (("ai5",AI5),("rest",REST))}
C["levels_bn"]={g:{str(y):{k:round(agg(k,ck,y)/1e9) for k in ("capex","buyback","rnd","dividend","ocf","rev")}
                for y in YEARS} for g,ck in (("ai5",AI5),("rest",REST))}
# R1 placebo windows
C["placebo"]={g:{f"{a}_{b}":{k:round(blk(ck,b)[k]-blk(ck,a)[k],1) for k in ("capex","buyback","rnd")}
    for a,b in ((2013,2017),(2017,2021),(2021,2025))} for g,ck in (("ai5",AI5),("rest",REST))}
# R2 revenue denominator
C["rev_denom"]={g:{str(y):blk(ck,y,"rev") for y in (2021,2025)} for g,ck in (("ai5",AI5),("rest",REST))}
# R3 leave-one-out
loo={}
for c in AI5:
    s=AI5-{c}
    loo[NAME[c]]={k:round(blk(s,2025)[k]-blk(s,2021)[k],1) for k in ("capex","buyback","rnd")}
C["leave_one_out"]=loo
C["loo_range"]={k:[min(v[k] for v in loo.values()),max(v[k] for v in loo.values())] for k in ("capex","buyback","rnd")}
# AI-4 (drop Amazon) for comparability with v1
AI4=AI5-{1018724}
C["ai4_check"]={k:round(blk(AI4,2025)[k]-blk(AI4,2021)[k],1) for k in ("capex","buyback","rnd")}
# R4 balanced panel
BAL=set.intersection(*[set(S[y]['capex']) for y in YEARS])
C["balanced"]={"n":len(BAL),
  **{g:{k:round(blk(ck&BAL,2025)[k]-blk(ck&BAL,2021)[k],1) for k in ("capex","buyback","rnd")}
     for g,ck in (("ai5",AI5),("rest",REST))}}
# concentration (corrected)
con={}
for y in YEARS:
    d={c:S[y]['capex'].get(c,0) for c in F if S[y]['capex'].get(c,0)>0}
    t=sum(d.values()); v=sorted(d.values(),reverse=True)
    e={c:x for c,x in d.items() if c not in AI5}; te=sum(e.values()); ev=sorted(e.values(),reverse=True)
    con[str(y)]={"hhi":round(sum((x/t)**2 for x in d.values())*10000),
      "hhi_ex":round(sum((x/te)**2 for x in e.values())*10000),
      "top5":round(sum(v[:5])/t*100,1),"top5_ex":round(sum(ev[:5])/te*100,1),"total_bn":round(t/1e9)}
C["concentration"]=con

# --- added: transparency on cash-flow growth, and mean-base robustness (2021 peak concern) ---
gg=lambda k,y,ck: agg(k,ck,y)/1e9
dC=gg('ocf',2025,AI5)-gg('ocf',2021,AI5); dX=gg('capex',2025,AI5)-gg('capex',2021,AI5)
dB=gg('buyback',2025,AI5)-gg('buyback',2021,AI5)
C["cfo_check"]={"d_ocf_bn":round(dC),"d_capex_bn":round(dX),"d_buyback_bn":round(dB),
  "ocf_covers_pct":round(dC/dX*100)}
BASE=[2017,2018,2019,2020,2021]
C["meanbase"]={g:{**{k:round(sum(agg(k,ck,y)/agg('ocf',ck,y)*100 for y in BASE)/len(BASE),1) for k in ("capex","buyback","rnd")},
   **{k+"_25":round(agg(k,ck,2025)/agg('ocf',ck,2025)*100,1) for k in ("capex","buyback","rnd")}}
   for g,ck in (("ai5",AI5),("rest",REST))}
for g in C["meanbase"]:
    for k in ("capex","buyback","rnd"):
        C["meanbase"][g]["d_"+k]=round(C["meanbase"][g][k+"_25"]-C["meanbase"][g][k],1)


# --- cross-section of the 500 in real log growth (no common denominator) ---
import math as _m, statistics as _st
def _lg(k,c):
    a=S[2021][k].get(c,0)*R(2021); b=S[2025][k].get(c,0)*R(2025)
    return _m.log(b/a) if a>0 and b>0 else None
_rows=[]
for c in F:
    x,v=_lg('capex',c),_lg('rev',c)
    if x is None or v is None: continue
    _rows.append(dict(cik=c,cap=x,rnd=_lg('rnd',c),bb=_lg('buyback',c),rev=v))
def _ols(p):
    a=[r[0] for r in p]; b=[r[1] for r in p]; ma,mb=_st.mean(a),_st.mean(b)
    sxx=sum((u-ma)**2 for u in a); bt=sum((u-ma)*(w-mb) for u,w in zip(a,b))/sxx
    res=[w-(mb+bt*(u-ma)) for u,w in zip(a,b)]
    se=_m.sqrt(sum(e*e for e in res)/(len(a)-2)/sxx)
    cr=sum((u-ma)*(w-mb) for u,w in zip(a,b))/_m.sqrt(sxx*sum((w-mb)**2 for w in b))
    return dict(slope=round(bt,3),se=round(se,3),t=round(bt/se,1),n=len(a),corr=round(cr,3))
def _res(key,sub):
    a=[r['rev'] for r in sub]; b=[r[key] for r in sub]; ma,mb=_st.mean(a),_st.mean(b)
    sxx=sum((u-ma)**2 for u in a); bt=sum((u-ma)*(w-mb) for u,w in zip(a,b))/sxx
    return [w-(mb+bt*(u-ma)) for u,w in zip(a,b)]
_sr=[r for r in _rows if r['rnd'] is not None]; _sb=[r for r in _rows if r['bb'] is not None]
C["xsec"]={"rnd":_ols([(r['cap'],r['rnd']) for r in _sr]),
           "bb":_ols([(r['cap'],r['bb']) for r in _sb]),
           "rnd_net":_ols(list(zip(_res('cap',_sr),_res('rnd',_sr)))),
           "bb_net":_ols(list(zip(_res('cap',_sb),_res('bb',_sb)))),
           "n_capex_up":sum(1 for r in _sr if r['cap']>0),
           "n_rnd_data":len(_sr),
           "pct_cut_rnd":round(sum(1 for r in _sr if r['cap']>0 and r['rnd']<0)/sum(1 for r in _sr if r['cap']>0)*100),
           "median_rnd_growth":round(_m.exp(_st.median(r['rnd'] for r in _sr if r['cap']>0))*100-100,1)}
C["five_growth"]={NAME[c]:{k:(round(_m.exp(r[k])*100-100,1) if r[k] is not None else None)
    for k in ("cap","rnd","bb")} for c in AI5 for r in _rows if r['cik']==c}


# --- cross-section across windows, excluding the five, and quintiles (500-firm focus) ---
def _mk(a,b,drop=set()):
    o=[]
    for c in F:
        if c in drop: continue
        def L(k):
            x=S[a][k].get(c,0)*R(a); y=S[b][k].get(c,0)*R(b)
            return _m.log(y/x) if x>0 and y>0 else None
        x,v=L('capex'),L('rev')
        if x is None or v is None: continue
        o.append(dict(cap=x,rnd=L('rnd'),bb=L('buyback'),rev=v))
    return o
def _fit(p):
    A=[r[0] for r in p]; B=[r[1] for r in p]
    ma,mb=_st.mean(A),_st.mean(B); sxx=sum((u-ma)**2 for u in A)
    bt=sum((u-ma)*(w-mb) for u,w in zip(A,B))/sxx
    r=[w-(mb+bt*(u-ma)) for u,w in zip(A,B)]
    se=_m.sqrt(sum(e*e for e in r)/(len(A)-2)/sxx)
    return dict(slope=round(bt,3),se=round(se,3),t=round(bt/se,1),n=len(A))
def _nr(key,sub):
    a=[r['rev'] for r in sub]; b=[r[key] for r in sub]; ma,mb=_st.mean(a),_st.mean(b)
    sxx=sum((u-ma)**2 for u in a); bt=sum((u-ma)*(w-mb) for u,w in zip(a,b))/sxx
    return [w-(mb+bt*(u-ma)) for u,w in zip(a,b)]
def _pair(a,b,drop=set()):
    rw=_mk(a,b,drop); sr=[r for r in rw if r['rnd'] is not None]; sb=[r for r in rw if r['bb'] is not None]
    return {"rnd":_fit([(r['cap'],r['rnd']) for r in sr]),
            "rnd_net":_fit(list(zip(_nr('cap',sr),_nr('rnd',sr)))),
            "bb":_fit([(r['cap'],r['bb']) for r in sb]),
            "bb_net":_fit(list(zip(_nr('cap',sb),_nr('bb',sb))))}
C["windows"]={"w2125":_pair(2021,2025),"w1721":_pair(2017,2021),"w1317":_pair(2013,2017),
              "w2125_ex5":_pair(2021,2025,AI5)}
_rw=_mk(2021,2025); _rw.sort(key=lambda r:r['cap']); _n=len(_rw); _q=_n//5
C["quintiles"]=[]
for i in range(5):
    g=_rw[i*_q:(i+1)*_q if i<4 else _n]
    rr=[r['rnd'] for r in g if r['rnd'] is not None]; bb=[r['bb'] for r in g if r['bb'] is not None]
    md=lambda v: round(_m.exp(_st.median(v))*100-100,1) if v else None
    C["quintiles"].append({"q":i+1,"n":len(g),"capex":md([r['cap'] for r in g]),
                           "rnd":md(rr),"bb":md(bb),"n_rnd":len(rr)})


# --- complete cash-flow account with an EXPLICIT residual line (closes by construction) ---
_DC="CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalentsPeriodIncreaseDecreaseIncludingExchangeRateEffect"
def _acct(ck,y):
    o=agg('ocf',ck,y); nd=agg('debt_in',ck,y)-agg('debt_out',ck,y); ne=agg('eq_in',ck,y)
    cx=agg('capex',ck,y); mn=agg('mna',ck,y); bb=agg('buyback',ck,y); dv=agg('dividend',ck,y)
    dc=sum(raw(_DC,y).get(c,0) for c in ck)*R(y)
    return dict(ocf=o,netdebt=nd,neteq=ne,capex=cx,mna=mn,bb=bb,div=dv,dcash=dc,
                other=(o+nd+ne)-(cx+mn+bb+dv+dc))
C["account"]={}
for g,ck in (("five",AI5),("rest",REST)):
    a,b=_acct(ck,2021),_acct(ck,2025); d={k:round((b[k]-a[k])/1e9) for k in a}
    src=d['ocf']+d['netdebt']+d['neteq']
    C["account"][g]={**d,"sources_total":src,
        "uses_total":d['capex']+d['mna']+d['bb']+d['div']+d['dcash']+d['other'],
        "pct_ocf":round(d['ocf']/src*100,1),"pct_debt":round(d['netdebt']/src*100,1),
        "pct_eq":round(d['neteq']/src*100,1),
        "d_rnd":round((agg('rnd',ck,2025)-agg('rnd',ck,2021))/1e9),
        "ocf_covers_capex_pct":round(d['ocf']/d['capex']*100) if d['capex'] else None}


# ================= v7 UPGRADES =================
_DC2="CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalentsPeriodIncreaseDecreaseIncludingExchangeRateEffect"
def _v(k,ck,y):
    if k=="netdebt": return agg('debt_in',ck,y)-agg('debt_out',ck,y)
    if k=="dcash":   return sum(raw(_DC2,y).get(c,0) for c in ck)*R(y)
    return agg(k,ck,y)
_KE=["capex","ocf","netdebt","eq_in","rnd","buyback","dividend","dcash"]
def _cum(ck,bl):
    base={k:(_v(k,ck,2021) if bl=="A" else sum(_v(k,ck,y) for y in range(2017,2022))/5) for k in _KE}
    return {k:round(sum(_v(k,ck,t)-base[k] for t in range(2022,2026))/1e9) for k in _KE}
C["cumulative"]={}
for bl in ("A","B"):
    for g,ck in (("five",AI5),("rest",REST)):
        d=_cum(ck,bl); d["coverage"]=round(d["ocf"]/d["capex"]*100) if d["capex"] else None
        C["cumulative"][f"{g}_{bl}"]=d
_NM={1652044:"Alphabet",1018724:"Amazon",1341439:"Oracle",1326801:"Meta",789019:"Microsoft"}
C["firm_level"]={_NM[c]:{**_cum({c},"A"),"coverage":round(_cum({c},"A")["ocf"]/_cum({c},"A")["capex"]*100)} for c in AI5}
C["leave_one_out_cum"]={_NM[c]:{**_cum(AI5-{c},"A"),
    "coverage":round(_cum(AI5-{c},"A")["ocf"]/_cum(AI5-{c},"A")["capex"]*100)} for c in AI5}
# STRICT: rank on cumulative incremental capex within the analysis sample, so the share
# denominator matches Table 1 rather than the 2021->2025 level change.
_elig=[c for c in F if S[2021]['capex'].get(c,0)>0 and S[2025]['capex'].get(c,0)>0]
def _raw_inc(c):                                # unrounded, identical basis to Table 1
    b=_v('capex',{c},2021); return sum(_v('capex',{c},t)-b for t in range(2022,2026))/1e9
_inc={c:_raw_inc(c) for c in _elig}
_inc={c:v for c,v in _inc.items() if v>0}
_rk=[c for c,_ in sorted(_inc.items(),key=lambda kv:-kv[1])]; _tot=sum(_inc.values())
C["group_size"]={}
for n in (3,5,10,20):
    g=set(_rk[:n]); d=_cum(g,"A")
    C["group_size"][f"top{n}"]={**d,"coverage":round(d["ocf"]/d["capex"]*100),
        "share_of_increase":round(sum(_inc[x] for x in g)/_tot*100,1)}
C["path"]={str(y):{"capex":round(agg('capex',AI5,y)/1e9),"ocf":round(agg('ocf',AI5,y)/1e9),
   "netdebt":round((agg('debt_in',AI5,y)-agg('debt_out',AI5,y))/1e9),
   "capex_over_ocf":round(agg('capex',AI5,y)/agg('ocf',AI5,y)*100)} for y in range(2017,2026)}
C["rnd_sample"]={"n_report_both":sum(1 for c in F if S[2021]['rnd'].get(c,0)>0 and S[2025]['rnd'].get(c,0)>0),
  "n_regression":C["xsec"]["rnd"]["n"],"n_capex_2025":sum(1 for c in F if S[2025]['capex'].get(c,0)>0),
  "n_no_rnd":500-sum(1 for c in F if S[2021]['rnd'].get(c,0)>0 and S[2025]['rnd'].get(c,0)>0)}
C["failed_checks"]={
 "other495_contrast":{"coverage_baseA":C["cumulative"]["rest_A"]["coverage"],
   "coverage_baseB":C["cumulative"]["rest_B"]["coverage"],
   "verdict":"FAIL - sign flips with baseline; dropped from the paper"},
 "repurchase_decline":{"cum_baseA":C["cumulative"]["five_A"]["buyback"],
   "cum_baseB":C["cumulative"]["five_B"]["buyback"],
   "verdict":"MIXED - negative on 2021 base, positive on 2017-21 mean base; demoted"}}


# --- distributional coverage: does concentration EXPLAIN the aggregate financing result? ---
def _cf(c,k):
    b=(agg('debt_in',{c},2021)-agg('debt_out',{c},2021)) if k=="netdebt" else agg(k,{c},2021)
    f=lambda y:(agg('debt_in',{c},y)-agg('debt_out',{c},y)) if k=="netdebt" else agg(k,{c},y)
    return sum(f(t)-b for t in range(2022,2026))/1e9
# STRICT SAMPLE: capex must be OBSERVED in both endpoint years, otherwise the baseline is a
# spurious zero and the firm's entire spending counts as 'incremental' (25 firms, $36bn).
_R=[]
for c in F:
    if not (S[2021]['capex'].get(c,0)>0 and S[2025]['capex'].get(c,0)>0): continue
    dx=_cf(c,'capex')
    if dx>0: _R.append(dict(cik=c,dx=dx,do=_cf(c,'ocf'),dd=_cf(c,'netdebt')))
_T=sum(r['dx'] for r in _R)
_R.sort(key=lambda r:-r['dx'])
C["distribution"]={"n_positive":len(_R),"total_positive_capex_bn":round(_T),
 "buckets":{lab:round(sum(r['dx'] for r in _R if lo<=r['do']/r['dx']<hi)/_T*100,1)
   for lab,lo,hi in (("ge100",1.0,9e9),("b75_100",0.75,1.0),("b50_75",0.50,0.75),("lt50",-9e9,0.50))},
 "cum_ge100":round(sum(r['dx'] for r in _R if r['do']/r['dx']>=1.0)/_T*100,1),
 "cum_ge75":round(sum(r['dx'] for r in _R if r['do']/r['dx']>=0.75)/_T*100,1),
 "cum_ge50":round(sum(r['dx'] for r in _R if r['do']/r['dx']>=0.50)/_T*100,1)}
_x=[r for r in _R if r['cik'] not in AI5]; _TX=sum(r['dx'] for r in _x)
C["distribution"]["ex5_ge100"]=round(sum(r['dx'] for r in _x if r['do']/r['dx']>=1.0)/_TX*100,1)
C["ladder"]=[]
for n in (1,3,5,10,20,50):
    g=_R[:n]; sx=sum(r['dx'] for r in g)
    C["ladder"].append({"group":f"top{n}","share":round(sx/_T*100,1),
      "coverage":round(sum(r['do'] for r in g)/sx*100),"netdebt":round(sum(r['dd'] for r in g))})
g=_R[50:]; sx=sum(r['dx'] for r in g)
C["ladder"].append({"group":f"remaining{len(g)}","share":round(sx/_T*100,1),
  "coverage":round(sum(r['do'] for r in g)/sx*100),"netdebt":round(sum(r['dd'] for r in g))})


# --- AI-exposure filter (pre-specified dictionary; see collect_ai_intensity.py header) ---
_SC=json.load(open("data/frozen/ai_intensity.json"))
def _cfx(c,k):
    b=(agg('debt_in',{c},2021)-agg('debt_out',{c},2021)) if k=="netdebt" else agg(k,{c},2021)
    f=lambda y:(agg('debt_in',{c},y)-agg('debt_out',{c},y)) if k=="netdebt" else agg(k,{c},y)
    return sum(f(t)-b for t in range(2022,2026))/1e9
_rw=[]
for c in F:
    if not (S[2021]['capex'].get(c,0)>0 and S[2025]['capex'].get(c,0)>0): continue
    dx=_cfx(c,'capex'); sc=_SC.get(str(c))
    if dx>0 and sc: _rw.append(dict(cik=c,dx=dx,do=_cfx(c,'ocf'),dd=_cfx(c,'netdebt'),ai=sc["ai_intensity"]))
_ints=sorted(r['ai'] for r in _rw)
C["ai_filter"]={"n_scored":len([v for v in _SC.values() if v]),"n_in_analysis":len(_rw),
  "median":round(_st.median(_ints),2),"p80":round(_ints[int(len(_ints)*.8)],2),
  "p90":round(_ints[int(len(_ints)*.9)],2),
  "top10_names":[ _SC[str(r['cik'])]["name"][:24] for r in sorted(_rw,key=lambda r:-r['ai'])[:10]]}
for cut,lab in ((0.90,"decile"),(0.80,"quintile")):
    thr=_ints[int(len(_ints)*cut)]
    U=sorted([r for r in _rw if r['ai']>=thr],key=lambda r:-r['dx']); T=sum(r['dx'] for r in U)
    X=[r for r in U if r['cik'] not in AI5]
    C["ai_filter"][lab]={"threshold":round(thr,2),"n":len(U),"capex":round(T),
      "five_share":round(sum(r['dx'] for r in U if r['cik'] in AI5)/T*100,1),
      "coverage_all":round(sum(r['do'] for r in U)/T*100),
      "netdebt_all":round(sum(r['dd'] for r in U)),
      "coverage_ex5":round(sum(r['do'] for r in X)/sum(r['dx'] for r in X)*100) if X else None,
      "netdebt_ex5":round(sum(r['dd'] for r in X)) if X else None,
      "coverage_top10":round(sum(r['do'] for r in U[:10])/sum(r['dx'] for r in U[:10])*100)}


# --- sample attrition and data provenance, for the manuscript's data section ---
_step={"universe":500,
 "capex_2025":sum(1 for c in F if S[2025]['capex'].get(c,0)>0),
 "capex_both":sum(1 for c in F if S[2021]['capex'].get(c,0)>0 and S[2025]['capex'].get(c,0)>0),
 "rnd_both":sum(1 for c in F if S[2021]['rnd'].get(c,0)>0 and S[2025]['rnd'].get(c,0)>0)}
_strict=[c for c in F if S[2021]['capex'].get(c,0)>0 and S[2025]['capex'].get(c,0)>0 and _cf(c,'capex')>0]
_step["analysis"]=len(_strict)
_step["ai_scored"]=len([c for c in _strict if _SC.get(str(c))])
_tot25=sum(S[2025]['capex'].get(c,0) for c in F)/1e9
_step["capex_2025_total_bn"]=round(_tot25)
_step["analysis_capex_bn"]=round(sum(S[2025]['capex'].get(c,0) for c in _strict)/1e9)
_step["analysis_capex_share"]=round(sum(S[2025]['capex'].get(c,0) for c in _strict)/1e9/_tot25*100)
_step["coverage_pct"]={k:round(sum(1 for c in F if S[2021][k].get(c,0)>0 and S[2025][k].get(c,0)>0)/5)
                       for k in ("capex","ocf","rev","rnd","buyback","debt_in")}
C["sample"]=_step

C["hashes"]={f:__import__("hashlib").sha256(open("data/frozen/"+f,"rb").read()).hexdigest()[:16]
   for f in sorted(__import__("os").listdir("data/frozen")) if f.endswith(".json")}
json.dump(C,open("claims.json","w"),indent=1)
p=lambda t:print("\n"+t)
p("MECHANICAL RULE"); print(" ",C["rule"]["rank"]); print("  top5 =",C["rule"]["top5_share_pct"],"% of $",C["rule"]["aggregate_increase_bn"],"bn increase; gap5/6 =",C["rule"]["gap_5_to_6"],"x")
p("MAIN — allocation shares (% of operating cash flow)")
for g in ("ai5","rest"):
    print(f"  {g}: 2021 {C['shares'][g]['2021']}  ->  2025 {C['shares'][g]['2025']}")
p("R1 PLACEBO — change in shares (pp)")
for g in ("ai5","rest"): print(f"  {g}: {C['placebo'][g]}")
p("R2 REVENUE DENOMINATOR (% of revenue)")
for g in ("ai5","rest"): print(f"  {g}: 2021 {C['rev_denom'][g]['2021']} -> 2025 {C['rev_denom'][g]['2025']}")
p("R3 LEAVE-ONE-OUT (drop each firm; change 2021->2025, pp)")
for k,v in C["leave_one_out"].items(): print(f"  drop {k:10s} {v}")
print("  range:",C["loo_range"]); print("  AI-4 (no Amazon):",C["ai4_check"])
p("R4 BALANCED PANEL"); print(" ",C["balanced"])
p("CONCENTRATION"); print("  2021",con["2021"]); print("  2025",con["2025"])
