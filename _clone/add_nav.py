#!/usr/bin/env python3
"""Add the new top-level nav items (About Us▾Our Objectives, Blog, Free
Resources, Contact Us) to the EXISTING approved pages. Idempotent; touches
ONLY the <nav> list markup — no content/layout/styling changes."""
import os
from build import REPO, add_nav_items

EXISTING = ["index.html", "index-print.html", "disciple.html", "coach.html", "curriculum.html",
            "new-christian-training.html", "how-to-open-a-new-christian-training-center.html",
            "teacher-training-tutorials.html", "why-moves-of-god-succeeded-and-faded.html",
            "be-a-coach-online-training.html"]

for fn in EXISTING:
    p = os.path.join(REPO, fn)
    if not os.path.exists(p):
        print("  skip (missing):", fn); continue
    src = open(p, encoding="utf-8").read()
    if "primary-nav__list" not in src:
        print("  skip (no nav):", fn); continue
    out = add_nav_items(src)
    if out != src:
        open(p, "w", encoding="utf-8").write(out)
        print(f"  nav updated: {fn}")
    else:
        print(f"  no change (already has items): {fn}")
