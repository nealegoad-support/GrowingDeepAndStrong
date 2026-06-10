#!/usr/bin/env python3
"""Download all live pages from the manifest into /tmp/gdas_live/<filename>.html"""
import os, sys, urllib.request, urllib.error, ssl
from concurrent.futures import ThreadPoolExecutor
from manifest import PAGES, DOMAIN, filename

OUT = "/tmp/gdas_live"
os.makedirs(OUT, exist_ok=True)
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def fetch(page):
    slug, group, eyebrow = page
    url = f"{DOMAIN}/{slug}"
    dest = os.path.join(OUT, filename(slug))
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (clone-mockup)"})
        with urllib.request.urlopen(req, timeout=30, context=ctx) as r:
            data = r.read().decode("utf-8", "ignore")
        with open(dest, "w", encoding="utf-8") as f:
            f.write(data)
        return (slug, "OK", len(data))
    except Exception as e:
        return (slug, f"ERR {e}", 0)

results = []
with ThreadPoolExecutor(max_workers=8) as ex:
    for res in ex.map(fetch, PAGES):
        results.append(res)
        print(f"{res[1]:>10}  {res[2]:>8}  {res[0]}")

ok = sum(1 for r in results if r[1] == "OK")
print(f"\nDONE: {ok}/{len(results)} fetched")
fails = [r for r in results if r[1] != "OK"]
if fails:
    print("FAILURES:")
    for f in fails:
        print(" ", f[0], f[1])
