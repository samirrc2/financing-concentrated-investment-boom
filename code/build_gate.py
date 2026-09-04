#!/usr/bin/env python3
"""Build gate: every number asserted in the manuscript must exist in claims.json.

This runs in the direction that matters. The previous version compared claims.json against a
hand-maintained list of expected values, which had to be edited by hand whenever the analysis
changed and so could not catch a transcription error introduced at the same time. This version
reads the numbers out of the manuscript and requires each one to be reproducible from the claims
file, so a mistyped figure fails the build.

Exemptions are listed explicitly below: years, structural integers, and quantities that are part
of a source's own text (a filing quotation, a BLS series name) rather than a result of ours.
"""
import json, re, sys

C = json.load(open("claims.json"))
TEX = open("manuscript.tex").read()

# ---- every value the analysis produces, at the precision it is reported ----
VALUES = set()
def walk(x):
    if isinstance(x, dict):
        for v in x.values(): walk(v)
    elif isinstance(x, list):
        for v in x: walk(v)
    elif isinstance(x, bool):
        pass
    elif isinstance(x, (int, float)):
        f = float(x)
        VALUES.update({round(f, 3), round(f, 1), float(round(f))})
walk(C)

# ---- what is not ours to verify ----
YEARS = set(range(1984, 2027))
STRUCTURAL = {0, 1, 2, 3, 4, 5, 10, 20, 50, 100, 500, 10000}   # cuts, counts, scaling
QUOTED = {69, 115, 135}          # dollar figures inside verbatim 10-K quotations
SERIES = {41312, 4131}           # BLS series identifiers
DERIVED = {263 - 50}             # the tail count, = analysis sample less the top fifty
EXEMPT = YEARS | STRUCTURAL | QUOTED | SERIES | DERIVED

def numbers(tex):
    body = tex[tex.index(r"\begin{abstract}"):tex.index(r"\section*{CRediT")] \
         + tex[tex.index(r"\appendix"):]
    body = re.sub(r"(?<!\\)%.*", "", body)
    body = re.sub(r"\\(label|ref|eqref|url|includegraphics|cite)\{[^}]*\}", " ", body)
    body = re.sub(r"https?://\S+", " ", body)
    body = re.sub(r"\b\d{6,}\b|\b\d{4}-\d{2}-\d{6}\b", " ", body)
    body = body.replace("{,}", "")
    for m in re.finditer(r"-?\d+(?:\.\d+)?", body):
        ctx = re.sub(r"\s+", " ", body[max(0, m.start()-60):m.end()+20]).strip()
        yield float(m.group(0)), m.group(0), ctx


# ---- anchored checks: a number must appear where it belongs, not merely somewhere ----
# The audit above catches a number with no backing claim. It cannot catch a number swapped
# for a different value that happens to exist elsewhere in claims.json, so the headline
# figures and both table bodies are additionally tied to their exact source.
def anchored(tex, C):
    errs = []
    L = {x["group"]: x for x in C["ladder"]}
    rem = [k for k in L if k.startswith("remaining")][0]
    N = {k: (int(k[3:]) if k.startswith("top") else C["funnel"]["positive"] - 50) for k in L}

    abstract = tex[tex.index(r"\begin{abstract}"):tex.index(r"\end{abstract}")]
    for label, want in (("top-5 coverage", L["top5"]["coverage"]),
                        ("top-10 coverage", L["top10"]["coverage"]),
                        ("top-10 share", L["top10"]["share"]),
                        ("tail coverage", L[rem]["coverage"]),
                        ("tail firm count", N[rem])):
        if not re.search(rf"(?<![\d.]){abs(want)}(?![\d.])", abstract.replace("{,}", "")):
            errs.append(f"abstract does not state the {label} ({want})")

    rows = dict(top1="Top 1", top3="Top 3", top5="Top 5", top10="Top 10",
                top20="Top 20", top50="Top 50", **{rem: "Remaining firms"})
    body = tex[tex.index(r"\label{tab:ladder}"):tex.index(r"\label{tab:placebo}")]
    for key, name in rows.items():
        m = re.search(rf"{re.escape(name)}\s*&([^\\]*)\\\\", body)
        if not m:
            errs.append(f"Table 1 row '{name}' not found"); continue
        cells = [c.strip() for c in m.group(1).split("&")]
        want = [str(N[key]), str(L[key]["share"]), str(L[key]["coverage"])]
        if cells[:3] != want:
            errs.append(f"Table 1 row '{name}': shows {cells[:3]}, claims say {want}")

    pl = C["placebo_ladder"]; order = ("w2225", "w1821", "w1417")
    tab2 = tex[tex.index(r"\label{tab:placebo}"):]
    tab2 = tab2[:tab2.index(r"\end{table}")]
    for name, field in (("Top 5", "cov5"), ("Top 10", "cov10"), ("Top 20", "cov20"),
                        ("Top 50", "cov50"), ("Remaining firms", "cov_rest")):
        m = re.search(rf"^{re.escape(name)}\s*&([^\\]*)\\\\", tab2, re.M)
        if not m:
            errs.append(f"Table 2 row '{name}' not found"); continue
        cells = [c.strip() for c in m.group(1).split("&")]
        want = [str(pl[w][field]) for w in order]
        if cells != want:
            errs.append(f"Table 2 row '{name}': shows {cells}, claims say {want}")
    m = re.search(r"Top-5 share of increase\s*&([^\\]*)\\\\", tab2)
    if m:
        cells = [c.strip() for c in m.group(1).split("&")]
        want = [str(pl[w]["top5_share"]) for w in order]
        if cells != want:
            errs.append(f"Table 2 top-5 share row: shows {cells}, claims say {want}")
    return errs

def main():
    seen, bad = 0, []
    for v, raw, ctx in numbers(TEX):
        if v in EXEMPT or abs(v) in EXEMPT:
            continue
        seen += 1
        if not any(c in VALUES for c in (round(v, 3), round(v, 1), float(round(v)),
                                         round(-v, 3), round(-v, 1), float(round(-v)))):
            bad.append((raw, ctx))
    print(f"build gate: {seen} numbers asserted in the manuscript, "
          f"{seen - len(bad)} reproduced from claims.json")
    if bad:
        for raw, ctx in bad:
            print(f"  UNVERIFIED {raw:>10}   ...{ctx}")
        print(f"FAILED ({len(bad)} numbers have no backing claim)")
        return 1
    # cross-consistency: the same quantity must not be computed two ways
    top1 = [x for x in C["ladder"] if x["group"] == "top1"][0]["coverage"]
    largest = max(C["firm_level"], key=lambda k: C["firm_level"][k]["capex"])
    if top1 != C["firm_level"][largest]["coverage"]:
        print(f"  INCONSISTENT: ladder top1 coverage {top1}% vs {largest} "
              f"{C['firm_level'][largest]['coverage']}% -- the same firm, two answers")
        print("FAILED (a quantity is reported two different ways)")
        return 1
    errs = anchored(TEX, C)
    if errs:
        for e in errs:
            print("  ANCHOR FAILED:", e)
        print(f"FAILED ({len(errs)} anchored checks)")
        return 1
    print("EVERY MANUSCRIPT NUMBER RECONCILES to claims.json")
    print("  anchored: abstract headline figures, Table 1 rows, Table 2 rows")
    print(f"  cross-check: top-1 coverage == {largest} coverage == {top1}%")
    print(f"  deflator: {C['universe']['deflator']}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
