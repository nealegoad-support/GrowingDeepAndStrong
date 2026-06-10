#!/usr/bin/env python3
"""
Clone engine: wrap live-site CONTENT in the mockup DESIGN shell.

- Design shell (head/header/footer/JS + editorial component classes) is sliced
  VERBATIM from an existing approved page (why-moves-of-god-succeeded-and-faded.html).
- Content is extracted from each cached live page's <article> and remapped onto
  the mockup's editorial component classes. Text is preserved verbatim.
"""
import os, re, json, html
from html.parser import HTMLParser
from manifest import PAGES, DOMAIN, filename

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIVE = "/tmp/gdas_live"
TEMPLATE = os.path.join(REPO, "why-moves-of-god-succeeded-and-faded.html")

# ---------------------------------------------------------------- live metadata
def load_meta():
    j = json.load(open(os.path.expanduser(
        "~/Downloads/www.growingdeepandstrong.com_.2026-06-10T03_12_22.112Z.json")))
    meta = {}
    for l in j["links"]:
        slug = l["url"].replace(DOMAIN, "").strip("/")
        meta[slug] = {"title": l.get("title", ""), "description": l.get("description", "")}
    return meta
META = load_meta()

# ---------------------------------------------------------------- link rewriting
EXISTING = {
    "": "index.html", "home": "index.html",
    "be-a-disciple-discipleship": "disciple.html",
    "be-a-coach-coaching": "coach.html",
    "be-a-coach-online-training": "be-a-coach-online-training.html",
    "curriculum": "curriculum.html",
    "new-christian-training": "new-christian-training.html",
    "how-to-open-a-new-christian-training-center": "how-to-open-a-new-christian-training-center.html",
    "teacher-training-tutorials": "teacher-training-tutorials.html",
    "why-moves-of-god-succeeded-and-faded": "why-moves-of-god-succeeded-and-faded.html",
}
SLUG2FILE = dict(EXISTING)
for slug, group, eyebrow in PAGES:
    SLUG2FILE[slug] = filename(slug)

def rewrite_href(href):
    if not href:
        return "#"
    href = href.strip()
    if href.startswith("#") or href.startswith("mailto:") or href.startswith("tel:"):
        return href
    # normalise live URL -> slug
    m = href
    for pre in (DOMAIN, "https://growingdeepandstrong.com", "http://www.growingdeepandstrong.com"):
        if m.startswith(pre):
            m = m[len(pre):]
    if m.startswith("/"):
        slug = m.strip("/").split("?")[0].split("#")[0]
        if slug in SLUG2FILE:
            return SLUG2FILE[slug]
        # PDFs / uploads stay absolute to the live domain
        if slug.startswith("wp-content/"):
            return DOMAIN + "/" + slug
        return "#"
    # already a relative/local link
    return href

# ---------------------------------------------------------------- shell slicing
src = open(TEMPLATE, encoding="utf-8").read()
HEAD   = re.search(r"<head>(.*?)</head>", src, re.S).group(1)
HEADER = re.search(r"<header\b.*?</header>", src, re.S).group(0)
FOOTER = re.search(r"<footer\b.*?</footer>", src, re.S).group(0)
JS     = re.search(r"</footer>(.*?)</body>", src, re.S).group(1)

# Wire footer/nav placeholder "#" links to the real new pages (new pages only).
WIRE = [
    (r'<a href="#">About Us</a>', '<a href="about-us.html">About Us</a>'),
    (r'<a href="#">Blog</a>', '<a href="blogs.html">Blog</a>'),
    (r'<a href="#">Testimonies</a>', '<a href="testimonies.html">Testimonies</a>'),
    (r'<a href="#">SEED for the Sower</a>', '<a href="seed-for-the-sower.html">SEED for the Sower</a>'),
    (r'<a href="#">Strategic Blueprint \(Free\)</a>', '<a href="get-the-strategic-blueprint.html">Strategic Blueprint (Free)</a>'),
    (r'<a href="#">Endorsement</a>', '<a href="endorsement.html">Endorsement</a>'),
    (r'<a href="#">Contact Us</a>', '<a href="contact-us.html">Contact Us</a>'),
    (r'<a href="#">Disclaimer</a>', '<a href="disclaimer.html">Disclaimer</a>'),
    (r'<a href="#">Terms of Service</a>', '<a href="terms-of-service.html">Terms of Service</a>'),
    (r'<a href="#">Privacy Statement</a>', '<a href="privacy-statement.html">Privacy Statement</a>'),
    (r'<a href="#">Vision Decree</a>', '<a href="vision-decree.html">Vision Decree</a>'),
    (r'<a href="#">Partners</a>', '<a href="partners.html">Partners</a>'),
    (r'<a href="#">Sitemap</a>', '<a href="sitemap.html">Sitemap</a>'),
    (r'<a role="menuitem" href="#">Return &amp; Refund Policy</a>',
     '<a role="menuitem" href="return-refund-policy.html">Return &amp; Refund Policy</a>'),
    (r'<a role="menuitem" href="#">Endorsement</a>',
     '<a role="menuitem" href="endorsement.html">Endorsement</a>'),
]
def wire(block):
    out = block
    for pat, rep in WIRE:
        out = re.sub(pat, rep, out)
    # the top-level "Testimonies" nav item is an <a href="#"> with caret
    out = out.replace('<a href="#" aria-haspopup="true" aria-expanded="false">\n                            Testimonies',
                      '<a href="testimonies.html" aria-haspopup="true" aria-expanded="false">\n                            Testimonies')
    return out
def add_nav_items(header):
    """Add About Us (with 'Our Objectives' submenu), Blog, Free Resources and
    Contact Us to the primary nav. Idempotent and scoped to the <nav> region
    only (so footer links don't interfere). Tolerates aria-current on anchors.
    Same markup/indentation as the existing nav items."""
    nm = re.search(r'<nav class="primary-nav".*?</nav>', header, re.S)
    if not nm:
        return header
    nav = nm.group(0)
    about = (
        '                    <li class="has-dropdown">\n'
        '                        <a href="about-us.html" aria-haspopup="true" aria-expanded="false">\n'
        '                            About Us\n'
        '                            <span class="caret" aria-hidden="true"></span>\n'
        '                        </a>\n'
        '                        <ul class="dropdown" role="menu">\n'
        '                            <li role="none"><a role="menuitem" href="our-objectives.html">Our Objectives</a></li>\n'
        '                        </ul>\n'
        '                    </li>\n')
    blog = '                    <li><a href="blogs.html">Blog</a></li>\n'
    free = '                    <li><a href="free-resources.html">Free Resources</a></li>\n'
    contact = '                    <li><a href="contact-us.html">Contact Us</a></li>\n'

    # 1) About Us (+submenu) directly after Home (Home may carry aria-current)
    if 'href="about-us.html" aria-haspopup' not in nav:
        nav = re.sub(r'(<li><a href="index\.html"[^>]*>Home</a></li>\n)',
                     lambda mo: mo.group(1) + about, nav, count=1)
    # 2) Blog directly after "Be A Disciple / Discipleship"
    if '<li><a href="blogs.html">Blog</a></li>' not in nav:
        nav = re.sub(r'(<li><a href="disciple\.html"[^>]*>Be A Disciple / Discipleship</a></li>\n)',
                     lambda mo: mo.group(1) + blog, nav, count=1)
    # 3) Free Resources + Contact Us at the end of the list (before </ul></nav>)
    if '<li><a href="free-resources.html">Free Resources</a></li>' not in nav:
        nav = re.sub(r'(\n\s*</ul>\s*\n\s*</nav>)',
                     lambda mo: "\n" + free + contact.rstrip("\n") + mo.group(1), nav, count=1)
    return header[:nm.start(0)] + nav + header[nm.end(0):]

HEADER_W = wire(add_nav_items(HEADER))
FOOTER_W = wire(FOOTER)

# ---------------------------------------------------------------- content parser
SKIP_SUBTREE_TAGS = {"script", "style", "noscript", "svg", "form", "iframe",
                     "button", "input", "select", "textarea", "nav", "header",
                     "footer", "figure"}
SKIP_CLASS_HINTS = ("comment", "sharedaddy", "jp-relatedposts", "related",
                    "post-navigation", "nav-links", "et_social", "screen-reader",
                    "breadcrumb", "wp-block-buttons", "sidebar", "widget",
                    "author-box", "post-meta", "entry-meta", "yarpp",
                    "add_to_cart", "woocommerce", "wc-block", "products",
                    "product ", "product\"")
KEEP_BLOCK = {"p", "h2", "h3", "h4", "h5", "ul", "ol", "li", "blockquote", "hr", "img", "table", "tr", "td", "th", "thead", "tbody"}
KEEP_INLINE = {"strong", "b", "em", "i", "a", "br", "sup", "sub", "u", "span"}

class Extractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.out = []
        self.skip_depth = 0
        self.h1 = None
        self._cap_h1 = False
        self._h1_buf = []
        self.depth_stack = []  # track tags we opened that need closing emit

    def _classid(self, attrs):
        d = dict(attrs)
        return (d.get("class", "") + " " + d.get("id", "")).lower()

    def handle_starttag(self, tag, attrs):
        if self.skip_depth:
            self.skip_depth += 1
            return
        ci = self._classid(attrs)
        if tag in SKIP_SUBTREE_TAGS or any(h in ci for h in SKIP_CLASS_HINTS):
            self.skip_depth = 1
            return
        if tag == "h1" and self.h1 is None:
            self._cap_h1 = True
            self._h1_buf = []
            return
        d = dict(attrs)
        if tag == "img":
            src = d.get("data-src") or d.get("src") or ""
            if src.startswith("/"):
                src = DOMAIN + src
            if not src or "data:image" in src or "spacer" in src or "blank" in src.lower():
                return
            alt = html.escape(d.get("alt", ""), quote=True)
            self.out.append(f'<figure class="editorial__figure" data-aos="fade-up"><img src="{src}" alt="{alt}" loading="lazy" /></figure>')
            return
        if tag in KEEP_BLOCK:
            cls = ""
            if tag == "h2":
                cls = ' class="section-title" data-aos="fade-up"'
            elif tag == "blockquote":
                cls = ' class="pull-quote" data-aos="fade-up"'
            self.out.append(f"<{tag}{cls}>")
            self.depth_stack.append(tag)
        elif tag in KEEP_INLINE:
            if tag == "a":
                href = rewrite_href(d.get("href", "#"))
                self.out.append(f'<a href="{html.escape(href, quote=True)}">')
            elif tag == "br":
                self.out.append("<br />")
            else:
                self.out.append(f"<{tag}>")
            self.depth_stack.append(tag if tag != "br" else None)
        else:
            # unwrap (div/span/section/etc.) — keep children, drop wrapper
            self.depth_stack.append(None)

    def handle_endtag(self, tag):
        if self.skip_depth:
            self.skip_depth -= 1
            return
        if tag == "h1" and self._cap_h1:
            self.h1 = html.unescape("".join(self._h1_buf)).strip()
            self._cap_h1 = False
            return
        if tag in SKIP_SUBTREE_TAGS:
            return
        if tag == "img":
            return
        if self.depth_stack:
            opened = None
            # pop the matching opened entry (best-effort LIFO)
            opened = self.depth_stack.pop()
        if tag in KEEP_BLOCK and tag != "img":
            self.out.append(f"</{tag}>")
        elif tag in KEEP_INLINE and tag != "br":
            self.out.append(f"</{tag}>")

    def handle_data(self, data):
        if self.skip_depth:
            return
        if self._cap_h1:
            self._h1_buf.append(data)
            return
        self.out.append(data)

    def handle_entityref(self, name):
        if self.skip_depth or self._cap_h1:
            if self._cap_h1: self._h1_buf.append(f"&{name};")
            return
        self.out.append(f"&{name};")

    def handle_charref(self, name):
        if self.skip_depth or self._cap_h1:
            if self._cap_h1: self._h1_buf.append(f"&#{name};")
            return
        self.out.append(f"&#{name};")

def clean_body(body, lead=True):
    # collapse empty tags & whitespace runs
    body = re.sub(r"<p>\s*</p>", "", body)
    body = re.sub(r"<(h[2-4])>\s*</\1>", "", body)
    body = re.sub(r"<li>\s*</li>", "", body)
    body = re.sub(r"[ \t]+\n", "\n", body)
    body = re.sub(r"\n{3,}", "\n\n", body)
    # first surviving <p> becomes the editorial lead with drop-cap
    if lead:
        body = re.sub(r"<p>", '<p class="editorial__lead has-dropcap" data-aos="fade-up">', body, count=1)
    return body.strip()

def _run(inner, lead=True):
    p = Extractor()
    p.feed(inner)
    p.close()
    return p.h1, clean_body("".join(p.out), lead=lead)

def extract_product(fn):
    """Return (name, price_str, description_html) from a WooCommerce product page."""
    h = open(fn, encoding="utf-8", errors="ignore").read()
    # product name from product_title / first h1
    nm = re.search(r'class="product_title[^"]*"[^>]*>(.*?)</h1>', h, re.S) or re.search(r"<h1[^>]*>(.*?)</h1>", h, re.S)
    name = html.unescape(re.sub(r"<[^>]+>", "", nm.group(1))).strip() if nm else None
    # price from the product summary <p class="price">
    pm = re.search(r'<p class="price">(.*?)</p>', h, re.S)
    price = None
    if pm:
        pp = re.search(r"AUD\s*\$\s*([\d,]+\.\d{2})", re.sub(r"<[^>]+>", " ", pm.group(1)))
        price = pp.group(1) if pp else None
    # description tab content
    dm = re.search(r'id="tab-description"[^>]*>(.*?)(?:<div[^>]*id="tab-|</div>\s*</div>\s*</article>)', h, re.S)
    desc_html = ""
    if dm:
        inner = re.sub(r"<h2[^>]*>\s*Description\s*</h2>", "", dm.group(1), flags=re.I)
        _, desc_html = _run(inner, lead=False)
    return name, price, desc_html

def is_protected(fn):
    h = open(fn, encoding="utf-8", errors="ignore").read()
    m = re.search(r"<article\b.*?</article>", h, re.S)
    art = m.group(0) if m else h
    return ("post_password" in art) or ("password-protection-box" in art)

def text_len(body):
    return len(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", body)).strip())

def raw_rescue(seg):
    """Last-resort: pull prose blocks from a region ignoring skip-hints.
    Used only for thin funnel/landing pages whose content sits in
    page-builder 'widget' wrappers the structured extractor skips."""
    seg = re.sub(r"<(script|style|form|svg|nav|header|footer|noscript)\b.*?</\1>", "", seg, flags=re.S | re.I)
    blocks = []
    seen = set()
    for m in re.finditer(r"<(h2|h3|p|li)\b[^>]*>(.*?)</\1>", seg, re.S | re.I):
        tag = m.group(1).lower()
        inner = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(2))).strip()
        if len(inner) < 4 or inner in seen:
            continue
        seen.add(inner)
        if tag in ("h2", "h3"):
            blocks.append(f'<h2 class="section-title" data-aos="fade-up">{inner}</h2>')
        elif tag == "li":
            blocks.append(f"<li>{inner}</li>")
        else:
            blocks.append(f"<p>{inner}</p>")
    out = "\n".join(blocks)
    out = re.sub(r"(?:<li>.*?</li>\n?)+", lambda mo: "<ul>" + mo.group(0) + "</ul>", out, flags=re.S)
    return clean_body(out)

def extract_article(fn):
    h = open(fn, encoding="utf-8", errors="ignore").read()
    m = re.search(r"<article\b.*?</article>", h, re.S)
    h1, body = _run(m.group(0) if m else h)
    # Some landing pages keep their content in <main> outside <article>.
    if text_len(body) < 160:
        mm = re.search(r"<main\b.*?</main>", h, re.S)
        if mm:
            h1b, bodyb = _run(mm.group(0))
            if text_len(bodyb) > text_len(body):
                h1, body = (h1 or h1b), bodyb
            # still thin -> raw prose rescue from <main>
            if text_len(body) < 160:
                rescued = raw_rescue(mm.group(0))
                if text_len(rescued) > text_len(body):
                    body = rescued
    return h1, body

# ---------------------------------------------------------------- page assembly
# Additive CSS — applied to NEW pages only (injected per-page, never touches
# style.css or the approved pages). Uses the mockup palette/typography tokens.
EXTRA_CSS = '''
    <style>
        /* --- additive helpers for cloned content pages (new pages only) --- */
        .editorial__figure { margin: 2.4rem auto; text-align: center; }
        .editorial__figure img { max-width: 100%; height: auto; border-radius: 6px;
            box-shadow: 0 10px 30px rgba(10,26,38,.12); }
        .editorial__body table { width: 100%; border-collapse: collapse; margin: 2rem 0;
            font-family: "Open Sans", sans-serif; font-size: .95rem; }
        .editorial__body th, .editorial__body td { border: 1px solid #e4dcca;
            padding: .7rem .9rem; text-align: left; vertical-align: top; }
        .editorial__body th { background: #f3ede1; font-weight: 600; }
        .index-grid { list-style: none; margin: 2.5rem 0 0; padding: 0; display: grid;
            gap: 1.6rem; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); }
        .index-card { display: flex; flex-direction: column; background: #fff;
            border: 1px solid #ece4d4; border-radius: 8px; padding: 1.6rem 1.6rem 1.8rem;
            box-shadow: 0 6px 20px rgba(10,26,38,.06); transition: transform .25s, box-shadow .25s; }
        .index-card:hover { transform: translateY(-4px); box-shadow: 0 14px 34px rgba(10,26,38,.12); }
        .index-card__eyebrow { font-family: "Inter", sans-serif; font-size: .72rem;
            letter-spacing: .12em; text-transform: uppercase; color: #b8924a; margin: 0 0 .5rem; }
        .index-card__title { font-family: "Roboto Slab", serif; font-size: 1.2rem;
            color: #1c3a52; margin: 0 0 .6rem; line-height: 1.25; }
        .index-card__body { font-family: "Open Sans", sans-serif; color: #4a5a66;
            font-size: .94rem; line-height: 1.6; margin: 0 0 1.2rem; flex: 1; }
        .index-card .btn { align-self: flex-start; margin-top: auto; }
        .sitemap-list { list-style: none; margin: .6rem 0 2.2rem; padding: 0; columns: 2;
            column-gap: 2.5rem; font-family: "Open Sans", sans-serif; }
        .sitemap-list li { margin: 0 0 .55rem; break-inside: avoid; }
        .sitemap-list a { color: #1c3a52; text-decoration: none; border-bottom: 1px solid transparent; }
        .sitemap-list a:hover { color: #b8924a; border-bottom-color: #b8924a; }
        @media (max-width: 640px){ .sitemap-list { columns: 1; } }
        .contact-details { font-family: "Open Sans", sans-serif; line-height: 1.9;
            color: #2a3b46; font-size: 1.05rem; }
        .contact-details strong { color: #1c3a52; }
    </style>'''

def page(title, description, eyebrow, hero_title, body_html, cta=None, verse=None):
    head = HEAD + EXTRA_CSS
    head = re.sub(r"<title>.*?</title>", f"<title>{html.escape(title)}</title>", head, flags=re.S)
    head = re.sub(r'(<meta name="description" content=").*?(" />)',
                  lambda mo: mo.group(1) + html.escape(description, quote=True) + mo.group(2),
                  head, flags=re.S)
    verse_html = f'\n                <p class="editorial-hero__verse" data-aos="fade-up" data-aos-delay="160">{verse}</p>' if verse else ""
    cta_html = ""
    if cta:
        label, href, sub, eyb = cta
        cta_html = f'''
        <section class="editorial-cta" aria-labelledby="editorial-cta-heading">
            <div class="container container--narrow editorial-cta__inner" data-aos="zoom-in-up">
                <p class="eyebrow eyebrow--gold">{eyb}</p>
                <h2 class="section-title section-title--center" id="editorial-cta-heading">{sub}</h2>
                <a href="{href}" class="btn btn--gold btn--lg">{label}</a>
            </div>
        </section>'''
    return f'''<!DOCTYPE html>
<html lang="en">

<head>{head}</head>

<body>

{HEADER_W}

    <main id="main">

        <section class="editorial-hero" aria-labelledby="editorial-hero-heading">
            <div class="container container--narrow">
                <p class="eyebrow eyebrow--gold" data-aos="fade-up">{html.escape(eyebrow)}</p>
                <h1 class="editorial-hero__title" id="editorial-hero-heading" data-aos="fade-up">{hero_title}</h1>{verse_html}
            </div>
        </section>

        <article class="editorial">
            <div class="container container--narrow editorial__body">
{body_html}
            </div>
        </article>
{cta_html}
    </main>

{FOOTER_W}
{JS}</body>

</html>
'''

DEFAULT_CTA = ("Explore the Discipleship Curriculum &rarr;", "curriculum.html",
               "Take the Next Step in Your Discipleship Journey", "Growing Deep and Strong")
