#!/usr/bin/env python3
"""Blinded review copy: manuscript.tex -> manuscript_blinded.tex/.pdf.

Removes author names, ORCIDs, emails, the affiliation, the corresponding-author note and the
CRediT statement, withholds the archive pointer, and clears the PDF metadata and XMP that a
blinded submission usually leaks. Regenerate whenever manuscript.tex changes.
"""
import re, os, subprocess, sys

s = open("manuscript.tex").read()
s = s.replace(s[s.index(r"\author[a]{"):s.index(r"\begin{abstract}")], "", 1)
m = re.search(r"\\section\*\{CRediT authorship contribution statement\}.*?"
              r"(?=\\section\*\{Declaration of competing)", s, re.S)
if m:
    s = s[:m.start()] + s[m.end():]
s = s.replace("openly available in the replication archive",
              "openly available in the replication archive, withheld during review")
if r"\usepackage{hyperref}" not in s:
    s = s.replace(r"\usepackage{caption}", "\\usepackage{caption}\n\\usepackage{hyperref}", 1)
s = s.replace(r"\begin{document}",
              "\\hypersetup{pdfauthor={},pdftitle={},pdfsubject={},pdfkeywords={},"
              "pdfcreator={},pdfproducer={}}\n\\begin{document}", 1)
open("manuscript_blinded.tex", "w").write(s)

for _ in range(2):
    subprocess.run(["pdflatex", "-interaction=nonstopmode", "manuscript_blinded.tex"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

import pymupdf
d = pymupdf.open("manuscript_blinded.pdf")
d.del_xml_metadata()
d.set_metadata({"title": "", "author": "", "subject": "", "keywords": "",
                "creator": "", "producer": ""})
d.save("_b.pdf", garbage=4, deflate=True); d.close()
os.replace("_b.pdf", "manuscript_blinded.pdf")

d = pymupdf.open("manuscript_blinded.pdf")
txt = "".join(p.get_text() for p in d)
leaks = [w for w in ("Chincholikar", "Chawla", "orcid", "iitbhu", "gmail")
         if w.lower() in txt.lower()]
leaks += ["CRediT"] if "CRediT" in txt else []   # case-sensitive: "private credit" is not a leak
meta = {k: v for k, v in d.metadata.items() if v and k not in ("format", "creationDate", "modDate")}
print(f"manuscript_blinded.pdf: {len(d)} pages, identifiers {leaks or 'none'}, metadata {meta or 'none'}")
sys.exit(1 if (leaks or meta) else 0)
