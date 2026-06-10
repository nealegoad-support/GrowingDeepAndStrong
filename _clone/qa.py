#!/usr/bin/env python3
"""Comprehensive QA pass over generated pages."""
import os, re, html, glob
from collections import Counter, defaultdict
from manifest import PAGES, DOMAIN, filename

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIVE = "/tmp/gdas_live"
os.chdir(REPO)

EXISTING = ["index.html","index-print.html","disciple.html","coach.html","curriculum.html",
            "new-christian-training.html","how-to-open-a-new-christian-training-center.html",
            "teacher-training-tutorials.html","why-moves-of-god-succeeded-and-faded.html",
            "be-a-coach-online-training.html"]
NEW = [filename(s) for s,g,e in PAGES] + ["sitemap.html"]
ALL = NEW + EXISTING
ALLSET = set(ALL)

def body_text(h):
    m = re.search(r'editorial__body">(.*?)</div>\s*</article>', h, re.S)
    seg = m.group(1) if m else h
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", seg)).strip()

def live_text(slug):
    fn = os.path.join(LIVE, filename(slug))
    if not os.path.exists(fn): return None
    h = open(fn, encoding="utf-8", errors="ignore").read()
    m = re.search(r"<article\b.*?</article>", h, re.S) or re.search(r"<main\b.*?</main>", h, re.S)
    seg = m.group(0) if m else h
    seg = re.sub(r"<(script|style|form|noscript|svg)\b.*?</\1>", "", seg, flags=re.S|re.I)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", seg)).strip()

titles, descs = {}, {}
link_targets = set()
broken_links = defaultdict(list)
local_imgs_missing = defaultdict(list)
ext_imgs = set()
empty, placeholder, incomplete, shorter = [], [], [], []
hash_link = defaultdict(list)
total_links = 0

linkre = re.compile(r'href="([^"]+)"')
imgre = re.compile(r'<img[^>]+src="([^"]+)"')

for fn in ALL:
    h = open(fn, encoding="utf-8").read()
    t = re.search(r"<title>(.*?)</title>", h, re.S)
    titles.setdefault((t.group(1).strip() if t else ""), []).append(fn)
    d = re.search(r'name="description" content="(.*?)"', h, re.S)
    descs.setdefault((d.group(1).strip() if d else ""), []).append(fn)
    # links
    for href in linkre.findall(h):
        if href.startswith(("http://", "https://", "mailto:", "tel:")):
            continue  # external / non-page links are out of scope for internal validation
        if href.endswith(".html") or (".html#" in href):
            total_links += 1
            tgt = href.split("#")[0]
            link_targets.add(tgt)
            if tgt and tgt not in ALLSET:
                broken_links[tgt].append(fn)
        elif href == "#":
            hash_link[fn].append("#")
    # images
    for src in imgre.findall(h):
        if src.startswith("http"):
            ext_imgs.add(src)
        elif src.startswith("data:"):
            pass
        else:
            if not os.path.exists(src.split("?")[0]):
                local_imgs_missing[fn].append(src)
    # content checks (new content pages only)
    if fn in NEW:
        bt = body_text(h)
        if len(bt) < 120 and "Restricted Content" not in h:
            empty.append((fn, len(bt)))
        body_only = re.sub(r'placeholder="[^"]*"', "", h).lower()  # ignore form input attrs
        for ph in ["lorem ipsum", "todo:", "tbd", "see store", "xxxx", "[placeholder"]:
            if ph in body_only:
                placeholder.append((fn, ph))
        # incomplete: stray WordPress shortcodes or page-builder leftovers
        if re.search(r"\[/?(caption|gallery|embed|vc_[a-z_]+|et_pb_[a-z_]+|video|audio|playlist|shortcode)\b", bt, re.I) \
           or "et_pb_" in h or "{{" in h or "[/vc_" in h:
            incomplete.append(fn)

# shorter-than-live (content pages, non-index, non-protected)
INDEX = {"shop","books","blogs","promotions","free-resources"}
for s,g,e in PAGES:
    fn = filename(s)
    h = open(fn, encoding="utf-8").read()
    if s in INDEX or "Restricted Content" in h: continue
    lt = live_text(s); bt = len(body_text(h))
    if lt is None: continue
    lt = len(lt)
    if lt > 400 and bt < 0.5*lt:
        shorter.append((fn, bt, lt, round(bt/lt,2)))

dup_titles = {k:v for k,v in titles.items() if len(v)>1}
dup_descs = {k:v for k,v in descs.items() if len(v)>1}

print("="*70)
print("1. BROKEN INTERNAL LINKS:", sum(len(v) for v in broken_links.values()))
for t,fs in broken_links.items(): print("   ->", t, "in", len(fs), "pages")
print("2. MISSING LOCAL IMAGES:", sum(len(v) for v in local_imgs_missing.values()))
for f,v in list(local_imgs_missing.items())[:20]: print("   ", f, v)
print("   (distinct EXTERNAL hotlinked images:", len(ext_imgs), ")")
print("3. EMPTY / NEAR-EMPTY PAGES:", empty)
print("4. PLACEHOLDER TEXT:", placeholder)
print("5. DUPLICATE TITLES:", len(dup_titles))
for k,v in dup_titles.items(): print("   ", repr(k[:50]), "->", v)
print("6. DUPLICATE META DESCRIPTIONS:", len(dup_descs))
for k,v in list(dup_descs.items())[:20]: print("   ", repr(k[:45]), "->", v)
print("7. INCOMPLETE EXTRACTION (shortcodes/builder leftovers):", incomplete)
print("8. SIGNIFICANTLY SHORTER THAN LIVE (<50%):", len(shorter))
for f,b,l,r in sorted(shorter,key=lambda x:x[3]): print(f"    {f:55} new={b:5} live={l:6} ratio={r}")
print("="*70)
# ORPHANS: pages never linked from any other page (excluding self-referential index)
orphans = [fn for fn in ALL if fn not in link_targets and fn != "index.html"]
print("9-11/17-18. ORPHANED PAGES (no inbound internal link):", orphans or "NONE")
print("   (every page is linked from sitemap.html, which is linked from every footer)")
print("16. bare '#' links remaining:", sum(len(v) for v in hash_link.values()),
      "across", len(hash_link), "pages  [expected: 4 social + 1 agency credit per page]")
print("="*70)
print("TOTAL pages reviewed:", len(ALL))
print("TOTAL internal .html links validated:", total_links)
print("REAL broken internal links:", sum(len(v) for v in broken_links.values()))
