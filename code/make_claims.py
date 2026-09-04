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
   "n_rest":len(REST),"deflator":"BLS PPI WPUFD41312","years":[2013,2025]}}
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
def _cumx(ck,bl):
    """Unrounded cumulative increments, $bn. Every ratio is formed from these, never from the
    rounded columns a table displays, so the same quantity cannot round two different ways."""
    base={k:(_v(k,ck,2021) if bl=="A" else sum(_v(k,ck,y) for y in range(2017,2022))/5) for k in _KE}
    return {k:sum(_v(k,ck,t)-base[k] for t in range(2022,2026))/1e9 for k in _KE}
def _cum(ck,bl):
    return {k:round(v) for k,v in _cumx(ck,bl).items()}
def _cov(ck,bl):
    x=_cumx(ck,bl); return round(x["ocf"]/x["capex"]*100) if x["capex"] else None
C["cumulative"]={}
for bl in ("A","B"):
    for g,ck in (("five",AI5),("rest",REST)):
        d=_cum(ck,bl); d["coverage"]=_cov(ck,bl)
        C["cumulative"][f"{g}_{bl}"]=d
_NM={1652044:"Alphabet",1018724:"Amazon",1341439:"Oracle",1326801:"Meta",789019:"Microsoft"}
C["firm_level"]={_NM[c]:{**_cum({c},"A"),"coverage":_cov({c},"A")} for c in AI5}
C["leave_one_out_cum"]={_NM[c]:{**_cum(AI5-{c},"A"),"coverage":_cov(AI5-{c},"A")} for c in AI5}
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
    C["group_size"][f"top{n}"]={**d,"coverage":_cov(g,"A"),
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


# --- placebo: the coverage ladder in earlier four-year windows (Appendix) ---
def _pl(base,yrs):
    R=[]
    for c in F:
        if not (S[base]['capex'].get(c,0)>0 and S[yrs[-1]]['capex'].get(c,0)>0): continue
        b=_v('capex',{c},base); dx=sum(_v('capex',{c},t)-b for t in yrs)/1e9
        if dx<=0: continue
        bo=_v('ocf',{c},base); do=sum(_v('ocf',{c},t)-bo for t in yrs)/1e9
        R.append((dx,do))
    R.sort(reverse=True); T=sum(r[0] for r in R)
    out={"n":len(R),"total_bn":round(T),"top5_share":round(sum(r[0] for r in R[:5])/T*100,1)}
    for n in (5,10,20,50):
        g=R[:n]; out[f"cov{n}"]=round(sum(r[1] for r in g)/sum(r[0] for r in g)*100)
    g=R[50:]; out["cov_rest"]=round(sum(r[1] for r in g)/sum(r[0] for r in g)*100)
    return out
C["placebo_ladder"]={"w2225":_pl(2021,[2022,2023,2024,2025]),
                     "w1821":_pl(2017,[2018,2019,2020,2021]),
                     "w1417":_pl(2013,[2014,2015,2016,2017])}


# ================= v8: aggregation identity, unrestricted sample, tail composition =========
# Phase 0 diagnostics, promoted into the claims file so the build gate covers them.
_SIC=json.load(open("data/frozen/sic_codes.json"))
def _mg(c):
    v=_SIC.get(str(c)) or {}
    try: return int(str(v.get("sic") or "0")[:2].zfill(2))
    except ValueError: return 0
_REG={13,29,40,44,45,46,47,49}      # oil and gas, refining, rail, water/air transport, pipelines, utilities
_FIN=set(range(60,68))              # banks and insurers: operating cash flow is not a comparable object
def _bucket(c):
    m=_mg(c)
    return "regulated" if m in _REG else ("financial" if m in _FIN else "other")

def _panel(base,yrs,positive=True):
    o=[]
    for c in F:
        if not (S[base]['capex'].get(c,0)>0 and S[yrs[-1]]['capex'].get(c,0)>0): continue
        b=_v('capex',{c},base); dx=sum(_v('capex',{c},t)-b for t in yrs)/1e9
        if positive and dx<=0: continue
        bo=_v('ocf',{c},base); do=sum(_v('ocf',{c},t)-bo for t in yrs)/1e9
        bd=_v('netdebt',{c},base); dd=sum(_v('netdebt',{c},t)-bd for t in yrs)/1e9
        o.append({"cik":c,"dx":dx,"do":do,"dd":dd,"sic":_mg(c),"b":_bucket(c)})
    o.sort(key=lambda r:-r["dx"]); return o

def _rung(rows,tot):
    sx=sum(r["dx"] for r in rows)
    return {"n":len(rows),"share":round(sx/tot*100,1),
            "coverage":round(sum(r["do"] for r in rows)/sx*100),
            "netdebt":round(sum(r["dd"] for r in rows))}
def _ladder(rows):
    t=sum(r["dx"] for r in rows)
    d={f"top{n}":_rung(rows[:n],t) for n in (5,10,20,50)}
    d["remaining"]=_rung(rows[50:],t); d["all"]=_rung(rows,t)
    d["total_bn"]=round(t); d["n"]=len(rows)
    return d

# 0.1 unrestricted sample: observed 2021 baseline, signed increments, negatives retained
_U=_panel(2021,[2022,2023,2024,2025],positive=False)
C["unrestricted"]=_ladder(_U)
_P=_panel(2021,[2022,2023,2024,2025])
C["unrestricted"]["n_dropped_by_filter"]=len(_U)-len(_P)
C["unrestricted"]["dropped_capex_bn"]=round(sum(r["dx"] for r in _U if r["dx"]<=0))

# 0.3 the aggregation identity, window by window
def _sp(a,b):
    def rk(v):
        o=sorted(range(len(v)),key=lambda i:v[i]); r=[0]*len(v)
        for j,i in enumerate(o): r[i]=j
        return r
    ra,rb=rk(a),rk(b); n=len(a); ma,mb=_st.mean(ra),_st.mean(rb)
    num=sum((x-ma)*(y-mb) for x,y in zip(ra,rb))
    den=(sum((x-ma)**2 for x in ra)*sum((y-mb)**2 for y in rb))**.5
    return round(num/den,3)
C["identity"]={}
for k,(base,yrs) in {"w2225":(2021,[2022,2023,2024,2025]),"w1821":(2017,[2018,2019,2020,2021]),
                     "w1417":(2013,[2014,2015,2016,2017])}.items():
    rows=_panel(base,yrs); t=sum(r["dx"] for r in rows); n=len(rows)
    sh=[r["dx"]/t for r in rows]; cv=[r["do"]/r["dx"]*100 for r in rows]
    wt=sum(a*b for a,b in zip(sh,cv)); mn=_st.mean(cv)
    f5=rows[:5]; s5=sum(r["dx"] for r in f5)
    w5=sum(r["do"] for r in f5)/s5*100; m5=_st.median(r["do"]/r["dx"]*100 for r in f5)
    C["identity"][k]={"n":n,"weighted":round(wt,1),"mean":round(mn,1),
        "median":round(_st.median(cv),1),
        "n_cov":round(sum((a-1/n)*(b-mn) for a,b in zip(sh,cv)),1),
        "spearman":_sp([-r["dx"] for r in rows],cv),
        "weighted_int":round(wt),"mean_int":round(mn),"median_int":round(_st.median(cv)),
        "ncov_int":round(wt-mn),
        "top5_weighted":round(w5),"top5_median":round(m5),"top5_gap":round(w5-m5)}

# 0.2 tail composition and the gradient net of it
_T=sum(r["dx"] for r in _P); _tail=_P[50:]; _tt=sum(r["dx"] for r in _tail)
C["composition"]={"tail":{}}
for b in ("regulated","financial","other"):
    g=[r for r in _tail if r["b"]==b]; sx=sum(r["dx"] for r in g)
    C["composition"]["tail"][b]={"n":len(g),"share_of_tail":round(sx/_tt*100,1),
        "coverage":round(sum(r["do"] for r in g)/sx*100),"netdebt":round(sum(r["dd"] for r in g))}
C["composition"]["ex_regulated"]=_ladder([r for r in _P if r["b"]!="regulated"])
C["composition"]["ex_financial"]=_ladder([r for r in _P if r["b"]!="financial"])
C["composition"]["ex_both"]=_ladder([r for r in _P if r["b"]=="other"])

# 4.3 the annual coverage series: cumulative coverage through each year
C["annual"]={}
_A5=AI5; _REST5=set(_rk)-set(list(_rk)[:5])
for y in range(2022,2026):
    yrs=list(range(2022,y+1))
    rows=_panel(2021,yrs)
    five=[r for r in rows if r["cik"] in _A5]; rest=[r for r in rows if r["cik"] not in _A5]
    C["annual"][str(y)]={
        "five":round(sum(r["do"] for r in five)/sum(r["dx"] for r in five)*100),
        "rest":round(sum(r["do"] for r in rest)/sum(r["dx"] for r in rest)*100)}

# --- who the unregulated non-financial tail is, and how thin debt reporting is ---
_oth=[r for r in _P[50:] if r["b"]=="other"]
def _grp(sics):
    g=[r for r in _oth if r["sic"] in sics]; sx=sum(r["dx"] for r in g)
    return {"n":len(g),"netdebt":round(sum(r["dd"] for r in g)),
            "coverage":round(sum(r["do"] for r in g)/sx*100) if sx else None}
C["tail_other"]={"n":len(_oth),"netdebt":round(sum(r["dd"] for r in _oth)),
    "capex":round(sum(r["dx"] for r in _oth)),
    "coverage":round(sum(r["do"] for r in _oth)/sum(r["dx"] for r in _oth)*100),
    "pharma_chem":_grp({28}),"tobacco":_grp({21}),"food_retail":_grp({54,58})}
# long-term-debt tags are sparsely filed; the five focal firms are not all observed
_LTD=["ProceedsFromIssuanceOfLongTermDebt","RepaymentsOfLongTermDebt"]
_rep={}
for c,n in _NM.items():
    _rep[n]=any(c in raw(t,y) for t in _LTD for y in range(2021,2026))
C["debt_reporting"]={"five_reporting":sorted(k for k,v in _rep.items() if v),
  "five_missing":sorted(k for k,v in _rep.items() if not v),
  "amazon_bn":round(sum(_v("netdebt",{1018724},t)-_v("netdebt",{1018724},2021) for t in range(2022,2026))/1e9),
  "meta_bn":round(sum(_v("netdebt",{1326801},t)-_v("netdebt",{1326801},2021) for t in range(2022,2026))/1e9),
  "universe_pct":C["sample"]["coverage_pct"]["debt_in"]}

# --- sample exclusions and the single-tag omission, both cited in the text ---
_no21=[c for c in F if S[2025]['capex'].get(c,0)>0 and S[2021]['capex'].get(c,0)<=0]
C["excluded"]={"n":len(_no21),
  "spurious_bn":round(sum(sum(agg('capex',{c},t) for t in range(2022,2026)) for c in _no21)/1e9)}
_prim=set(raw('PaymentsToAcquirePropertyPlantAndEquipment',2025))
_alt=raw('PaymentsToAcquireProductiveAssets',2025)
_only=[c for c in _alt if c not in _prim]
C["alt_tag"]={"n_only":len(_only),"n_others":len(_only)-1,
  "capex_bn":round(sum(_alt[c] for c in _only)*R(2025)/1e9)}

# --- the 500-firm funnel, so every registrant is accounted for in the text ---
_both=[c for c in F if S[2021]['capex'].get(c,0)>0 and S[2025]['capex'].get(c,0)>0]
def _inc(c):
    b=_v('capex',{c},2021); return sum(_v('capex',{c},t)-b for t in range(2022,2026))
_pos=[c for c in _both if _inc(c)>0]
C["funnel"]={"universe":len(F),"both_endpoints":len(_both),"positive":len(_pos),
             "nonpositive":len(_both)-len(_pos),"missing_endpoint":len(F)-len(_both)}

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
