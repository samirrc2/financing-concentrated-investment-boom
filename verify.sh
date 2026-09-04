#!/bin/sh
# One-command verification for a referee. Exits 0 only if everything checks out.
#
#   1. every archived file matches MANIFEST.sha256
#   2. the analysis re-runs end to end from the frozen sources
#   3. regenerated claims.json and figure are byte-identical to the committed ones
#   4. every number in the manuscript reproduces from claims.json
#   5. the manuscript is within the Economics Letters length limit
#
# The working tree is left exactly as found.

set -eu
fail() { printf '\n FAIL: %s\n' "$1" >&2; exit 1; }
step() { printf '\n[%s] %s\n' "$1" "$2"; }

# sha256sum on Linux, shasum -a 256 on macOS
if command -v sha256sum >/dev/null 2>&1; then SHA="sha256sum"
elif command -v shasum   >/dev/null 2>&1; then SHA="shasum -a 256"
else fail "need sha256sum or shasum"; fi

step 1 "checking $(wc -l < MANIFEST.sha256 | tr -d ' ') archived files against MANIFEST.sha256"
$SHA -c MANIFEST.sha256 > /tmp/_vfy_manifest.txt 2>&1 || {
    grep -v ': OK$' /tmp/_vfy_manifest.txt >&2 || true
    fail "manifest mismatch — the archive has been modified"; }
echo "    all files match"

TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
cp claims.json "$TMP/claims.committed.json"
cp figures/Figure_1.png "$TMP/Figure_1.committed.png"

step 2 "re-running the analysis from data/frozen/"
python3 code/make_claims.py > "$TMP/claims.log" 2>&1 || { cat "$TMP/claims.log" >&2; fail "make_claims.py"; }
python3 code/make_figure.py > "$TMP/figure.log" 2>&1 || { cat "$TMP/figure.log" >&2; fail "make_figure.py"; }
echo "    regenerated claims.json and figures/"

step 3 "comparing regenerated output with the committed output"
if ! cmp -s claims.json "$TMP/claims.committed.json"; then
    python3 - "$TMP/claims.committed.json" claims.json <<'PY' >&2
import json, sys
a = json.load(open(sys.argv[1])); b = json.load(open(sys.argv[2]))
def walk(x, y, p=""):
    if isinstance(x, dict):
        for k in x:
            if k in y: walk(x[k], y[k], p + "/" + str(k))
            else: print(f"  MISSING {p}/{k}")
    elif isinstance(x, list):
        for i, (u, v) in enumerate(zip(x, y)): walk(u, v, f"{p}[{i}]")
    elif x != y:
        print(f"  CLAIM CHANGED {p}: committed={x} regenerated={y}")
walk(a, b)
PY
    cp "$TMP/claims.committed.json" claims.json
    cp "$TMP/Figure_1.committed.png" figures/Figure_1.png
    fail "regenerated claims differ from the committed claims file"
fi
cmp -s figures/Figure_1.png "$TMP/Figure_1.committed.png" || {
    cp "$TMP/Figure_1.committed.png" figures/Figure_1.png
    fail "regenerated figure differs from the committed figure"; }
echo "    claims.json and Figure_1.png are byte-identical"

step 4 "auditing every number in the manuscript against claims.json"
python3 code/build_gate.py || fail "a manuscript number does not reproduce (see above)"

step 5 "checking the Economics Letters length limit"
python3 code/wordcount.py || fail "manuscript exceeds the length limit"

git checkout -- figures/Figure_1.pdf 2>/dev/null || true   # PDF embeds a build timestamp
printf '\n=========================================\n PASS - the archive reproduces the paper\n=========================================\n'
