#!/usr/bin/env python3
"""Driver: generate mockup pages from live content, per page type."""
import os, re, sys, html
from build import (REPO, LIVE, META, PAGES, DOMAIN, filename, extract_article,
                   extract_product, page, DEFAULT_CTA, rewrite_href, is_protected)

PROTECTED_BODY = '''<p class="editorial__lead has-dropcap" data-aos="fade-up">{intro}</p>
                <aside class="callout callout--looking" data-aos="fade-up">
                    <h2 class="callout__title">Restricted Content</h2>
                    <p>This page is password-protected on the live Growing Deep and Strong® website, so its
                    full content is not publicly available to migrate. Access is granted to registered coaches
                    and partners. Please <a href="contact-us.html">contact us</a> to request access.</p>
                </aside>'''

GENERIC_TITLE = "Growing Deep and Strong, Christian Discipleship training programs"

ACRONYMS = {"Pdf": "PDF", "Gdas": "GDAS", "Nctc": "NCTC", "Nctcsp": "NCTCSP", "Dbc": "DBC"}

def pretty(slug):
    base = slug.split("/")[-1].replace("-", " ").strip().title()
    return " ".join(ACRONYMS.get(w, w) for w in base.split())

GENERIC_DESC_PREFIX = "Our Mandate Is to be a catalyst"

def clean_title(slug, h1=None):
    t = (META.get(slug, {}).get("title") or "").strip()
    if not t or t == GENERIC_TITLE:
        t = (h1 or pretty(slug)).strip()
    # strip any existing "- Growing Deep and Strong" / "| ..." site suffix
    t = re.split(r"\s*[-|–—]\s*Growing Deep and Strong.*$", t)[0].strip()
    t = re.split(r"\s*\|\s*", t)[0].strip()
    # generic "Thank You" titles -> make unique from the slug
    if re.fullmatch(r"thank\s*you!?\.?", t, re.I):
        t = pretty(slug)
    return t + " — Growing Deep and Strong®"

def derive_desc(slug, body_html=""):
    d = (META.get(slug, {}).get("description") or "").strip()
    if d and not d.startswith(GENERIC_DESC_PREFIX):
        return d
    txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", body_html)).strip()
    if txt:
        snip = txt[:155]
        if len(txt) > 155:
            snip = snip.rsplit(" ", 1)[0] + "…"
        return snip
    # no usable body and desc was empty/generic -> unique slug-based fallback
    return f"{pretty(slug)} — part of the Growing Deep and Strong® Christian discipleship resources."

def meta_for(slug):
    m = META.get(slug, {})
    return m.get("title", ""), m.get("description", "")

def price_of(slug):
    """Pull 'AUD $xx.xx' price(s) from a cached product page."""
    try:
        h = open(os.path.join(LIVE, filename(slug)), encoding="utf-8", errors="ignore").read()
    except FileNotFoundError:
        return None
    prices = re.findall(r"AUD\s*\$\s*([\d,]+\.\d{2})", h)
    return prices[0] if prices else None

# ----------------------------------------------------------------- INDEX PAGES
def card(eyebrow, title, body, href, label="Read more"):
    return f'''                <li class="index-card" data-aos="fade-up">
                    <p class="index-card__eyebrow">{html.escape(eyebrow)}</p>
                    <h2 class="index-card__title">{html.escape(title)}</h2>
                    <p class="index-card__body">{html.escape(body)}</p>
                    <a href="{href}" class="btn btn--primary btn--sm">{label} &rarr;</a>
                </li>'''

def index_grid(items):
    return ('<ul class="index-grid">\n' + "\n".join(items) + "\n            </ul>")

def gen_index(slug, eyebrow, intro, members, label="Read more"):
    title, desc = meta_for(slug)
    cards = []
    for s in members:
        t, d = meta_for(s)
        # derive an eyebrow per member from its manifest group
        grp = next((g for (ms, g, eb) in PAGES if ms == s), "")
        eb = next((eb for (ms, g, eb) in PAGES if ms == s), eyebrow)
        ct = re.split(r"\s*[-|–—]\s*Growing Deep and Strong.*$", t)[0].strip() if t else ""
        cards.append(card(eb, ct or pretty(s), d or "", filename(s), label))
    body = (f'<p class="editorial__lead has-dropcap" data-aos="fade-up">{html.escape(intro)}</p>\n'
            + "            " + index_grid(cards))
    return page(clean_title(slug), derive_desc(slug, f'<p>{intro}</p>'), eyebrow,
                html.escape(title or pretty(slug)), body, cta=DEFAULT_CTA)

# ----------------------------------------------------------------- PRODUCT PAGE
def gen_product(slug, eyebrow):
    title, desc = meta_for(slug)
    name, price, body = extract_product(os.path.join(LIVE, filename(slug)))
    name = name or title
    if not body.strip():
        body = f'<p>{html.escape(desc)}</p>'
    sku = slug.split("/")[-1].upper().replace("-", " ")
    price_html = f'<span class="price-current">AUD ${price}</span>' if price else '<span class="price-current">See store</span>'
    purchase = f'''                <div class="product-card" data-aos="zoom-in-up">
                    <div class="product-card__image" aria-label="{html.escape(name)} — product visual">
                        <div class="product-card__book" aria-hidden="true">
                            <span class="product-card__book-series">Growing Deep <em>AND</em> Strong<sup>&reg;</sup></span>
                            <span class="product-card__book-title">{html.escape(name)}</span>
                        </div>
                    </div>
                    <div class="product-card__details">
                        <div>
                            <p class="product-card__sku">{html.escape(sku)}</p>
                            <h2 class="product-card__title">{html.escape(name)}</h2>
                        </div>
                        <div class="product-card__pricing" aria-label="Pricing">
                            <div class="product-card__pricing-row product-card__pricing-row--current">
                                <span class="price-label">Price:</span>
                                {price_html}
                            </div>
                        </div>
                        <div class="product-card__actions">
                            <a href="shop.html" class="btn btn--gold btn--block btn--lg">Add to Cart &rarr;</a>
                            <p class="product-card__note">Secure checkout &nbsp;·&nbsp; Dispatched globally</p>
                        </div>
                    </div>
                </div>'''
    full_body = purchase + "\n\n                <h2 class=\"section-title\" data-aos=\"fade-up\">Description</h2>\n" + body
    cta = ("Browse the Full Shop &rarr;", "shop.html", "Equip Your Disciples with the Right Tools", "Shop")
    return page(clean_title(slug, name), derive_desc(slug, body), eyebrow, html.escape(name), full_body, cta=cta)

# ----------------------------------------------------------------- GENERIC ARTICLE
def gen_article(slug, group, eyebrow):
    title, desc = meta_for(slug)
    cached = os.path.join(LIVE, filename(slug))
    if is_protected(cached):
        hero = html.escape(pretty(slug))
        intro = html.escape(desc or f"{pretty(slug)} — part of the Growing Deep and Strong® discipleship resources.")
        body = PROTECTED_BODY.format(intro=intro)
        return page(clean_title(slug), derive_desc(slug), eyebrow, hero, body, cta=DEFAULT_CTA)
    h1, body = extract_article(cached)
    hero = html.escape(h1 or (title.split(" - ")[0].split(" — ")[0].strip() if title else slug))
    if not body.strip():
        body = f'<p class="editorial__lead has-dropcap" data-aos="fade-up">{html.escape(desc)}</p>'
    # choose CTA by group
    if group == "blog":
        cta = ("Read More on the Blog &rarr;", "blogs.html", "Keep Growing Deep and Strong", "More Articles")
    elif group == "resource":
        cta = ("See All Free Resources &rarr;", "free-resources.html", "Equip Yourself for the Harvest", "Free Resources")
    elif group == "legal":
        cta = None
    else:
        cta = DEFAULT_CTA
    return page(clean_title(slug, h1), derive_desc(slug, body), eyebrow, hero, body, cta=cta)

# ----------------------------------------------------------------- INDEX MEMBER SETS
def members(group):
    return [s for (s, g, eb) in PAGES if g == group]

INDEX_INTRO = {
    "shop": "Equip your disciples with biblically sound, easy-to-use courses. Every resource in the Growing Deep and Strong® Series has been refined over thousands of hours so a new believer can pick it up and begin their journey with you as their coach.",
    "books": "Browse the Growing Deep and Strong® books and printed resources — written to take a new believer from a pagan background to a confident disciple-maker.",
    "blogs": "Inspiration, teaching, and discipleship insight from Growing Deep and Strong®. Dive into articles written to strengthen your walk and equip you to disciple others.",
    "promotions": "Current promotions and invitations from Growing Deep and Strong® — practical on-ramps to begin or deepen your discipleship journey.",
    "free-resources": "Free downloads, manuals, and tools to help you disciple new believers and start your own New Christian Training Centre.",
}

def build_one(slug, group, eyebrow):
    if slug in ("shop", "books"):
        prods = members("product")
        return gen_index(slug, eyebrow, INDEX_INTRO[slug], prods, label="View product")
    if slug == "blogs":
        return gen_index(slug, eyebrow, INDEX_INTRO["blogs"], members("blog"))
    if slug == "promotions":
        promos = [s for s in members("resource") if s.startswith("promotions/")]
        return gen_index(slug, eyebrow, INDEX_INTRO["promotions"], promos, label="View promotion")
    if slug == "free-resources":
        res = [s for s in members("resource") if not s.startswith("promotions/")]
        return gen_index(slug, eyebrow, INDEX_INTRO["free-resources"], res, label="Get it")
    if group == "product":
        return gen_product(slug, eyebrow)
    return gen_article(slug, group, eyebrow)

EXISTING_LINKS = [
    ("Home", "index.html"),
    ("New Christian Training", "new-christian-training.html"),
    ("Why Moves of God Succeeded and Faded", "why-moves-of-god-succeeded-and-faded.html"),
    ("How to Open a New Christian Training Center", "how-to-open-a-new-christian-training-center.html"),
    ("Curriculum", "curriculum.html"),
    ("Teacher Training Tutorials", "teacher-training-tutorials.html"),
    ("Be A Coach / Coaching", "coach.html"),
    ("Be A Coach Online Training", "be-a-coach-online-training.html"),
    ("Be A Disciple / Discipleship", "disciple.html"),
]

def build_sitemap():
    """A hub page linking every page so nothing is orphaned."""
    def section(title, links):
        items = "\n".join(
            f'                    <li><a href="{href}">{html.escape(label)}</a></li>'
            for label, href in links)
        return (f'                <h2 class="section-title" data-aos="fade-up">{title}</h2>\n'
                f'                <ul class="sitemap-list">\n{items}\n                </ul>')
    def grp(g):
        return [(re.split(r"\s*[-|–—]\s*Growing Deep and Strong.*$", meta_for(s)[0])[0].strip() or pretty(s),
                 filename(s)) for s, gg, e in PAGES if gg == g]
    body = (
        '<p class="editorial__lead has-dropcap" data-aos="fade-up">Every page on the Growing Deep and '
        'Strong® mockup, organised by section. This sitemap ensures every resource is reachable.</p>\n'
        + section("Main Pages", EXISTING_LINKS)
        + "\n" + section("About &amp; Information",
            [(pretty(s), filename(s))
             for s in ["about-us","our-objectives","endorsement","testimonies","vision-decree","partners","contact-us"]])
        + "\n" + section("Discipleship &amp; Training",
            [(pretty(s), filename(s)) for s in ["our-new-christian-course","discipleship-course-outline","discipleship-course-structure","coachs-manual-discipling-others","equipping-the-saints","your-next-steps","grow"]])
        + "\n" + section("Shop &amp; Products", [("Shop","shop.html"),("Books","books.html")] + grp("product"))
        + "\n" + section("Free Resources", [("Free Resources","free-resources.html")] + [(pretty(s), filename(s)) for s,g,e in PAGES if g=="resource" and not s.startswith("promotions/")])
        + "\n" + section("Promotions", [("All Promotions","promotions.html")] + [(pretty(s.split("/")[-1]), filename(s)) for s,g,e in PAGES if s.startswith("promotions/")])
        + "\n" + section("Blog &amp; Articles", [("Blog Index","blogs.html")] + grp("blog"))
        + "\n" + section("Legal", grp("legal"))
    )
    out = page("Sitemap — Growing Deep and Strong®",
               "Full sitemap of the Growing Deep and Strong® Christian discipleship website.",
               "Site Index", "Sitemap", body, cta=DEFAULT_CTA)
    open(os.path.join(REPO, "sitemap.html"), "w", encoding="utf-8").write(out)
    print("  built   sitemap.html")

def main():
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    count = int(sys.argv[2]) if len(sys.argv) > 2 else len(PAGES)
    batch = PAGES[start:start+count]
    written = []
    for slug, group, eyebrow in batch:
        out = build_one(slug, group, eyebrow)
        fn = filename(slug)
        open(os.path.join(REPO, fn), "w", encoding="utf-8").write(out)
        written.append((fn, group, len(out)))
        print(f"  {group:8} {fn:55} {len(out):>7}b")
    if start == 0 and len(batch) == len(PAGES):
        build_sitemap()
    print(f"\nWrote {len(written)} files (manifest index {start}..{start+len(batch)-1})")

if __name__ == "__main__":
    main()
