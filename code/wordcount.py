#!/usr/bin/env python3
"""Economics Letters length gate: main text + table notes + figure captions + references.

EL returns submissions over 2,000 words without review. Front matter (title, authors,
abstract, keywords), the journal's required declarations, and appendices/online supplement
are excluded, following the journal's own convention. Run: python3 code/wordcount.py
"""
import re, sys

LIMIT = 2000

def strip(t):
    t = re.sub(r"(?<!\\)%.*", "", t)                      # comments
    t = re.sub(r"\\(begin|end)\{[^}]*\}(\[[^\]]*\])?", " ", t)
    t = re.sub(r"\\(label|ref|eqref|cite|includegraphics|url|setlength|renewcommand"
               r"|newcommand|addlinespace|arraystretch|tabcolsep|multicolumn|captionsetup"
               r"|setcounter|vspace|hspace|clearpage|normalsize|footnotesize|small|noindent"
               r"|centering|toprule|midrule|bottomrule|par|medskip|linewidth|textwidth)"
               r"\*?(\[[^\]]*\])?(\{[^{}]*\})*", " ", t)
    t = re.sub(r"\\[a-zA-Z@]+\*?(\[[^\]]*\])?", " ", t)   # any remaining control sequence
    t = re.sub(r"[${}&\\~^_|@]", " ", t)                  # math delimiters, alignment, escapes
    t = re.sub(r"[-]{2,}", "-", t)                        # en/em dashes join a range: one word
    return t

def words(t):
    return [w for w in re.split(r"\s+", strip(t)) if re.search(r"[A-Za-z0-9]", w)]

def section(tex, start, end):
    i = tex.index(start); j = tex.index(end, i)
    return tex[i:j]

def main(path="manuscript.tex"):
    tex = open(path).read()
    body = section(tex, r"\section{Introduction}", r"\section*{CRediT")
    refs = section(tex, r"\begin{thebibliography}", r"\end{thebibliography}")
    abstract = section(tex, r"\begin{abstract}", r"\end{abstract}")
    nb, nr = len(words(body)), len(words(refs))
    total = nb + nr
    print(f"  main text, tables and captions : {nb:5d}")
    print(f"  references                     : {nr:5d}")
    print(f"  COUNTED TOTAL                  : {total:5d}   (limit {LIMIT})")
    print(f"  abstract (counted separately)  : {len(words(abstract)):5d}")
    if total > LIMIT:
        print(f"OVER LIMIT by {total-LIMIT}"); return 1
    print(f"under limit with {LIMIT-total} words to spare"); return 0

if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
