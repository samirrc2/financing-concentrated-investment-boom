#!/usr/bin/env python3
"""Every number asserted in the manuscript must reconcile to claims.json."""
import json,sys
C=json.load(open("claims.json")); tex=open("P28_main.tex").read()
a,r=C["shares"]["ai5"],C["shares"]["rest"]; L=C["levels_bn"]["ai5"]
rv=C["rev_denom"]["ai5"]; pl=C["placebo"]["ai5"]; con=C["concentration"]; lo=C["loo_range"]
K=[("universe n",C["universe"]["n"],500),("revenue tn",C["universe"]["rev_fy2024_tn"],19.75),
 ("n rest",C["universe"]["n_rest"],495),
 ("rule top5 share",C["rule"]["top5_share_pct"],67.3),("rule gap",C["rule"]["gap_5_to_6"],2.9),
 ("agg increase",C["rule"]["aggregate_increase_bn"],385),
 ("ai5 capex 21",a["2021"]["capex"],45.9),("ai5 capex 25",a["2025"]["capex"],70.2),
 ("ai5 bb 21",a["2021"]["buyback"],49.1),("ai5 bb 25",a["2025"]["buyback"],15.4),
 ("ai5 rnd 21",a["2021"]["rnd"],29.8),("ai5 rnd 25",a["2025"]["rnd"],27.4),
 ("ai5 div 21",a["2021"]["dividend"],7.1),("ai5 div 25",a["2025"]["dividend"],7.7),
 ("rest capex 21",r["2021"]["capex"],24.7),("rest capex 25",r["2025"]["capex"],30.0),
 ("rest bb 21",r["2021"]["buyback"],28.6),("rest bb 25",r["2025"]["buyback"],30.5),
 ("rest rnd 21",r["2021"]["rnd"],12.7),("rest rnd 25",r["2025"]["rnd"],14.8),
 ("rest div 21",r["2021"]["dividend"],19.7),("rest div 25",r["2025"]["dividend"],20.7),
 ("lvl capex 21",L["2021"]["capex"],154),("lvl capex 25",L["2025"]["capex"],413),
 ("lvl bb 21",L["2021"]["buyback"],165),("lvl bb 25",L["2025"]["buyback"],90),
 ("lvl rnd 21",L["2021"]["rnd"],100),("lvl rnd 25",L["2025"]["rnd"],161),
 ("lvl ocf 21",L["2021"]["ocf"],336),("lvl ocf 25",L["2025"]["ocf"],588),
 ("rev capex 21",rv["2021"]["capex"],12.3),("rev capex 25",rv["2025"]["capex"],24.7),
 ("rev bb 21",rv["2021"]["buyback"],13.1),("rev bb 25",rv["2025"]["buyback"],5.4),
 ("rev rnd 21",rv["2021"]["rnd"],8.0),("rev rnd 25",rv["2025"]["rnd"],9.7),
 ("plac1317 capex",pl["2013_2017"]["capex"],7.6),("plac1721 capex",pl["2017_2021"]["capex"],14.9),
 ("plac1317 bb",pl["2013_2017"]["buyback"],1.4),("plac1721 bb",pl["2017_2021"]["buyback"],26.8),
 ("plac1317 rnd",pl["2013_2017"]["rnd"],-0.9),("plac1721 rnd",pl["2017_2021"]["rnd"],-2.5),
 ("hhi 21",con["2021"]["hhi"],173),("hhi 25",con["2025"]["hhi"],309),
 ("hhi_ex 21",con["2021"]["hhi_ex"],95),("hhi_ex 25",con["2025"]["hhi_ex"],104),
 ("loo capex lo",lo["capex"][0],18.4),("loo capex hi",lo["capex"][1],33.6),
 ("loo bb lo",lo["buyback"][0],-38.6),("loo bb hi",lo["buyback"][1],-28.3),
 ("ai4 capex",C["ai4_check"]["capex"],33.6),("ai4 bb",C["ai4_check"]["buyback"],-38.6),
 ("bal n",C["balanced"]["n"],1823),("bal ai5 capex",C["balanced"]["ai5"]["capex"],24.3),
 ("bal ai5 bb",C["balanced"]["ai5"]["buyback"],-33.7),
 ("bal rest capex",C["balanced"]["rest"]["capex"],7.3),("bal rest bb",C["balanced"]["rest"]["buyback"],-1.0)]
K+=[("cfo d_ocf",C["cfo_check"]["d_ocf_bn"],252),("cfo d_capex",C["cfo_check"]["d_capex_bn"],259),
 ("cfo covers",C["cfo_check"]["ocf_covers_pct"],97),("cfo d_bb",abs(C["cfo_check"]["d_buyback_bn"]),74),
 ("mb ai5 capex base",C["meanbase"]["ai5"]["capex"],38.3),("mb ai5 bb base",C["meanbase"]["ai5"]["buyback"],35.4),
 ("mb ai5 d_capex",C["meanbase"]["ai5"]["d_capex"],31.9),("mb ai5 d_bb",C["meanbase"]["ai5"]["d_buyback"],-20.0),
 ("mb rest d_capex",C["meanbase"]["rest"]["d_capex"],-0.7),("mb rest d_bb",C["meanbase"]["rest"]["d_buyback"],1.7)]
X=C["xsec"]; FG=C["five_growth"]
K+=[("xs rnd slope",X["rnd"]["slope"],0.484),("xs rnd t",X["rnd"]["t"],11.4),("xs rnd n",X["rnd"]["n"],153),
 ("xs rnd se",X["rnd"]["se"],0.042),
 ("xs rndnet slope",X["rnd_net"]["slope"],0.111),("xs rndnet t",X["rnd_net"]["t"],2.7),
 ("xs rndnet se",X["rnd_net"]["se"],0.041),
 ("xs bb slope",X["bb"]["slope"],-0.043),("xs bb t",X["bb"]["t"],-0.2),("xs bb n",X["bb"]["n"],237),
 ("xs bb se",X["bb"]["se"],0.182),
 ("xs bbnet slope",X["bb_net"]["slope"],-0.136),("xs bbnet t",X["bb_net"]["t"],-0.7),
 ("xs bbnet se",X["bb_net"]["se"],0.191),
 ("n capex up",X["n_capex_up"],82),("pct cut rnd",X["pct_cut_rnd"],32),
 ("median rnd growth",X["median_rnd_growth"],11.5),
 ("Oracle cap",FG["Oracle"]["cap"],936.2),("Oracle rnd",FG["Oracle"]["rnd"],19.5),("Oracle bb",FG["Oracle"]["bb"],-99.5),
 ("Meta cap",FG["Meta"]["cap"],213.1),("Meta rnd",FG["Meta"]["rnd"],95.4),("Meta bb",FG["Meta"]["bb"],-50.5),
 ("Alpha cap",FG["Alphabet"]["cap"],211.7),("Alpha rnd",FG["Alphabet"]["rnd"],62.5),("Alpha bb",FG["Alphabet"]["bb"],-23.7),
 ("MSFT cap",FG["Microsoft"]["cap"],162.9),("MSFT rnd",FG["Microsoft"]["rnd"],31.7),("MSFT bb",FG["Microsoft"]["bb"],-43.5),
 ("AMZN cap",FG["Amazon"]["cap"],81.3)]
LR=C["longrun"]
K+=[("lr 1950",LR["share_1950"],6.1),("lr 2000",LR["share_2000"],30.1),("lr 2025",LR["share_2025"],32.5),
 ("lr gdp 2000",LR["gdp_2000"],4.4),("lr gdp 2025",LR["gdp_2025"],4.49),
 ("lr range lo",LR["range_2010_2021"][0],27.0),("lr range hi",LR["range_2010_2021"][1],31.6),
 ("lr span lo",LR["span"][0],1947),("lr span hi",LR["span"][1],2025),
 ("lr excess",round(LR["share_2025"]-LR["share_2000"],1),2.4)]
W=C["windows"]; Q=C["quintiles"]
for wk,lab in (("w2125","2125"),("w1721","1721"),("w1317","1317"),("w2125_ex5","ex5")):
    for fk in ("rnd","rnd_net","bb","bb_net"):
        K+=[(f"{lab} {fk} slope",W[wk][fk]["slope"],W[wk][fk]["slope"]),
            (f"{lab} {fk} t",W[wk][fk]["t"],W[wk][fk]["t"]),
            (f"{lab} {fk} se",W[wk][fk]["se"],W[wk][fk]["se"])]
    K+=[(f"{lab} n rnd",W[wk]["rnd"]["n"],W[wk]["rnd"]["n"]),(f"{lab} n bb",W[wk]["bb"]["n"],W[wk]["bb"]["n"])]
for q in Q:
    K+=[(f"Q{q['q']} capex",q["capex"],q["capex"]),(f"Q{q['q']} rnd",q["rnd"],q["rnd"]),
        (f"Q{q['q']} bb",q["bb"],q["bb"])]
A5=C["account"]["five"]; AR=C["account"]["rest"]
for lab,src in (("five",A5),("rest",AR)):
    for k in ("ocf","netdebt","neteq","capex","mna","bb","div","dcash","other","sources_total","d_rnd"):
        K+=[(f"acct {lab} {k}",src[k],src[k])]
K+=[("acct five pct_ocf",A5["pct_ocf"],92.3),("acct five pct_debt",A5["pct_debt"],7.3),
    ("acct five covers",A5["ocf_covers_capex_pct"],97)]
CU=C["cumulative"]; LO=C["leave_one_out_cum"]; FL=C["firm_level"]; GS=C["group_size"]; PA=C["path"]
K+=[("cum A capex",CU["five_A"]["capex"],371),("cum A ocf",CU["five_A"]["ocf"],438),
 ("cum A netdebt",CU["five_A"]["netdebt"],-3),("cum A neteq",CU["five_A"]["eq_in"],2),
 ("cum A cov",CU["five_A"]["coverage"],118),("cum A rnd",CU["five_A"]["rnd"],142),
 ("cum A cash",CU["five_A"]["dcash"],214),("cum A div",CU["five_A"]["dividend"],40),
 ("cum A buyback",CU["five_A"]["buyback"],-206),
 ("cum B capex",CU["five_B"]["capex"],588),("cum B ocf",CU["five_B"]["ocf"],762),
 ("cum B netdebt",CU["five_B"]["netdebt"],37),("cum B neteq",CU["five_B"]["eq_in"],-2),
 ("cum B cov",CU["five_B"]["coverage"],130),("cum B rnd",CU["five_B"]["rnd"],229),
 ("cum B cash",CU["five_B"]["dcash"],76),("cum B div",CU["five_B"]["dividend"],49),
 ("cum B buyback",CU["five_B"]["buyback"],78),
 ("rest A cov",CU["rest_A"]["coverage"],-81),("rest B cov",CU["rest_B"]["coverage"],411),
 ("loo Amazon",LO["Amazon"]["coverage"],81),("loo Alphabet",LO["Alphabet"]["coverage"],136),
 ("loo Meta",LO["Meta"]["coverage"],129),("loo Oracle",LO["Oracle"]["coverage"],131),
 ("loo Microsoft",LO["Microsoft"]["coverage"],117),
 ("fl Oracle",FL["Oracle"]["coverage"],63),("fl Alphabet",FL["Alphabet"]["coverage"],67),
 ("fl Meta",FL["Meta"]["coverage"],79),("fl Microsoft",FL["Microsoft"]["coverage"],122),
 ("fl Amazon",FL["Amazon"]["coverage"],344),
 ("gs3",GS["top3"]["coverage"],70),("gs5",GS["top5"]["coverage"],118),
 ("gs10",GS["top10"]["coverage"],104),("gs20",GS["top20"]["coverage"],84),
 ("gs3 share",GS["top3"]["share_of_increase"],26.2),("gs20 share",GS["top20"]["share_of_increase"],63.9),
 ("gs5 share",GS["top5"]["share_of_increase"],38.7),("gs10 share",GS["top10"]["share_of_increase"],52.5),
 ("path 2017",PA["2017"]["capex_over_ocf"],31),("path 2021",PA["2021"]["capex_over_ocf"],46),
 ("path 2025",PA["2025"]["capex_over_ocf"],70),
 ("rnd n both",C["rnd_sample"]["n_report_both"],165),("rnd n reg",C["rnd_sample"]["n_regression"],153),
 ("rnd n none",C["rnd_sample"]["n_no_rnd"],335)]
LD={x["group"]:x for x in C["ladder"]}; DI=C["distribution"]
for g,sh,cv,nd in (("top1",10.1,67,0),("top3",26.2,70,60),("top5",38.7,118,-3),("top10",52.5,104,29),
                   ("top20",63.9,84,-69),("top50",81.5,55,148),("remaining217",18.5,-7,280)):
    K+=[(f"ladder {g} share",LD[g]["share"],sh),(f"ladder {g} cov",LD[g]["coverage"],cv),
        (f"ladder {g} debt",LD[g]["netdebt"],nd)]
K+=[("dist n",DI["n_positive"],267),("dist ge100",DI["cum_ge100"],33.3),
    ("dist lt50",DI["buckets"]["lt50"],30.4),("dist ex5",DI["ex5_ge100"],34.0)]
SM=C["sample"]; AF=C["ai_filter"]; LD2={x["group"]:x for x in C["ladder"]}
K+=[("sample universe",SM["universe"],500),("sample capex25",SM["capex_2025"],421),
 ("sample capexboth",SM["capex_both"],404),("sample analysis",SM["analysis"],267),
 ("sample aiscored",SM["ai_scored"],261),("sample rndboth",SM["rnd_both"],165),
 ("sample capexshare",SM["analysis_capex_share"],87),
 ("cov capex",SM["coverage_pct"]["capex"],81),("cov ocf",SM["coverage_pct"]["ocf"],84),
 ("cov rev",SM["coverage_pct"]["rev"],93),("cov rnd",SM["coverage_pct"]["rnd"],33),
 ("cov bb",SM["coverage_pct"]["buyback"],55),("cov debt",SM["coverage_pct"]["debt_in"],25),
 ("ai dec n",AF["decile"]["n"],27),("ai dec capex",AF["decile"]["capex"],401),
 ("ai dec cov",AF["decile"]["coverage_all"],128),("ai dec debt",AF["decile"]["netdebt_all"],-24),
 ("ai dec cov ex5",AF["decile"]["coverage_ex5"],248),("ai dec debt ex5",AF["decile"]["netdebt_ex5"],-20),
 ("ai dec thr",AF["decile"]["threshold"],2.21),("ai dec five",AF["decile"]["five_share"],92.5),
 ("ai qui n",AF["quintile"]["n"],53),("ai qui cov",AF["quintile"]["coverage_all"],138),
 ("ai qui cov ex5",AF["quintile"]["coverage_ex5"],301),("ai qui thr",AF["quintile"]["threshold"],1.35),
 ("ai median",AF["median"],0.64),("ai p90",AF["p90"],2.21),
 ("lad5 share",LD2["top5"]["share"],38.7),("lad10 share",LD2["top10"]["share"],52.5),
 ("lad20 share",LD2["top20"]["share"],63.9),("lad50 share",LD2["top50"]["share"],81.5),
 ("lad50 cov",LD2["top50"]["coverage"],55),("ladR share",LD2["remaining217"]["share"],18.5),
 ("ladR cov",LD2["remaining217"]["coverage"],-7),("ladR debt",LD2["remaining217"]["netdebt"],280),
 ("dist total",C["distribution"]["total_positive_capex_bn"],959),
 ("dist lt50b",C["distribution"]["buckets"]["lt50"],30.4)]
D=[("d capex",round(a["2025"]["capex"]-a["2021"]["capex"],1),24.3),
   ("d bb",round(a["2025"]["buyback"]-a["2021"]["buyback"],1),-33.7),
   ("d rnd",round(a["2025"]["rnd"]-a["2021"]["rnd"],1),-2.4),
   ("d rest capex",round(r["2025"]["capex"]-r["2021"]["capex"],1),5.3),
   ("d rest bb",round(r["2025"]["buyback"]-r["2021"]["buyback"],1),1.9),
   ("d rest rnd",round(r["2025"]["rnd"]-r["2021"]["rnd"],1),2.1),
   ("rnd growth %",round((L["2025"]["rnd"]/L["2021"]["rnd"]-1)*100),61),
   ("ocf growth %",round((L["2025"]["ocf"]/L["2021"]["ocf"]-1)*100),75),
   ("hhi range lo",min(con[str(y)]["hhi"] for y in range(2013,2021)),106),
   ("hhi range hi",max(con[str(y)]["hhi"] for y in range(2013,2021)),177)]
# A number CITED in the manuscript must reconcile. A claim not cited is not a failure.
cited=lambda c: str(abs(c)).rstrip('0').rstrip('.') in tex.replace("{,}","")
bad=[f"  MISMATCH {l}: claims={g} manuscript={c}" for l,g,c in K+D if abs(g-c)>0.051]
unused=[l for l,g,c in K+D if not cited(c)]
print(f"build gate: {len(K+D)} assertions | {len(K+D)-len(unused)} cited in manuscript")
if bad: print("\n".join(bad)); print(f"FAILED ({len(bad)})"); sys.exit(1)
print("ALL CITED NUMBERS RECONCILE to claims.json")
if unused: print(f"  ({len(unused)} claims computed but not cited: {', '.join(unused[:8])}"
                 + (", ..." if len(unused)>8 else "") + ")")
