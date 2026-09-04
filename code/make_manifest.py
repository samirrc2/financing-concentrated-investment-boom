#!/usr/bin/env python3
"""Write MANIFEST.sha256: every file a referee needs, in `sha256sum -c` format.

Membership is whatever git tracks, so build artefacts and caches excluded by .gitignore can
never drift into the archive. MANIFEST.sha256 itself is excluded; verify.sh checks the rest.
"""
import hashlib, subprocess, sys

files = sorted(subprocess.run(["git", "ls-files"], capture_output=True, text=True,
                              check=True).stdout.split())
files = [f for f in files if f != "MANIFEST.sha256"]
with open("MANIFEST.sha256", "w") as out:
    for f in files:
        h = hashlib.sha256(open(f, "rb").read()).hexdigest()
        out.write(f"{h}  {f}\n")
print(f"MANIFEST.sha256: {len(files)} files")
