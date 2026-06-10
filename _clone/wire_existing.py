#!/usr/bin/env python3
"""Site-wide consistency: wire the '#' placeholder nav/footer links on the
EXISTING approved pages to the real new pages. Touches ONLY <a href> targets
in the shared header/footer — no content, layout, or styling is altered."""
import os, re
from build import REPO, wire   # `wire` applies the same href replacements used on new pages

EXISTING = ["index.html", "index-print.html", "disciple.html", "coach.html", "curriculum.html",
            "new-christian-training.html", "how-to-open-a-new-christian-training-center.html",
            "teacher-training-tutorials.html", "why-moves-of-god-succeeded-and-faded.html",
            "be-a-coach-online-training.html"]

for fn in EXISTING:
    p = os.path.join(REPO, fn)
    if not os.path.exists(p):
        print("  skip (missing):", fn); continue
    src = open(p, encoding="utf-8").read()
    if "<a" not in src:           # be-a-coach-online-training.html is plain text
        print("  skip (no anchors):", fn); continue
    out = wire(src)
    if out != src:
        before = src.count('href="#"')
        after = out.count('href="#"')
        open(p, "w", encoding="utf-8").write(out)
        print(f"  wired   {fn:50}  '#' links {before} -> {after}")
    else:
        print(f"  nochange {fn}")
