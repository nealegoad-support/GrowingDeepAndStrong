# Master manifest of pages to clone from the live site into the mockup.
# group: core | product | resource | blog | legal
# slug: live path (no domain, no leading slash)
# eyebrow: small gold label shown above the H1 in the editorial hero
# cta: (label, href) for the closing editorial-cta, or None to use the default

DOMAIN = "https://www.growingdeepandstrong.com"

def filename(slug):
    return slug.replace("/", "-") + ".html"

# (slug, group, eyebrow)
PAGES = [
    # ---------------- CORE (19) ----------------
    ("about-us",                      "core", "About Us"),
    ("our-objectives",                "core", "About Us"),
    ("contact-us",                    "core", "Get in Touch"),
    ("partners",                      "core", "Partners"),
    ("endorsement",                   "core", "Endorsement"),
    ("testimonies",                   "core", "Testimonies"),
    ("vision-decree",                 "core", "Our Vision"),
    ("shop",                          "core", "Shop"),
    ("books",                         "core", "Shop"),
    ("blogs",                         "core", "Blog"),
    ("free-resources",                "core", "Free Resources"),
    ("promotions",                    "core", "Promotions"),
    ("our-new-christian-course",      "core", "Curriculum"),
    ("discipleship-course-outline",   "core", "Curriculum"),
    ("discipleship-course-structure", "core", "Curriculum"),
    ("coachs-manual-discipling-others","core", "Coaching"),
    ("equipping-the-saints",          "core", "Coaching"),
    ("your-next-steps",               "core", "Get Started"),
    ("grow",                          "core", "Get Started"),

    # ---------------- PRODUCT (4) ----------------
    ("product/coachs-basic-course",                              "product", "Shop"),
    ("product/disciples-basic-course",                           "product", "Shop"),
    ("product/disciples-basic-course-inc-bible",                 "product", "Shop"),
    ("product/gdas-nctcsp-new-christian-training-starters-pack", "product", "Shop"),

    # ---------------- RESOURCE (19) ----------------
    ("get-the-strategic-blueprint",        "resource", "Free Resources"),
    ("strategic-blueprint-thank-you",      "resource", "Thank You"),
    ("how-to-start-a-movement",            "resource", "Free Resources"),
    ("how-to-start-a-movement-thank-you",  "resource", "Thank You"),
    ("unlock-the-bible",                   "resource", "Free Resources"),
    ("how-to-unlock-the-bible",            "resource", "Free Resources"),
    ("seed-for-the-sower",                 "resource", "Free Resources"),
    ("the-war-is-real-bonus-manual",       "resource", "Free Resources"),
    ("the-war-is-real-thank-you",          "resource", "Thank You"),
    ("pdf-brochure-thank-you",             "resource", "Thank You"),
    ("thank-you-why-moves-of-god-succeeded-and-faded", "resource", "Thank You"),
    ("encounter-one-weekend",              "resource", "Encounter Weekend"),
    ("encounter-weekend-in-your-area",     "resource", "Encounter Weekend"),
    ("promotions/from-stuck-to-transformed-unleash-the-power-of-gods-word-in-20-weeks", "resource", "Promotion"),
    ("promotions/growing-deep-and-strong-with-god-in-20-weeks", "resource", "Promotion"),
    ("promotions/i-came-with-an-open-mind",   "resource", "Promotion"),
    ("promotions/just-do-it",                 "resource", "Promotion"),
    ("promotions/reignite-your-christian-faith","resource", "Promotion"),
    ("promotions/this-is-the-time-to-do-it",  "resource", "Promotion"),

    # ---------------- LEGAL (4) ----------------
    ("disclaimer",          "legal", "Legal"),
    ("privacy-statement",   "legal", "Legal"),
    ("return-refund-policy","legal", "Legal"),
    ("terms-of-service",    "legal", "Legal"),

    # ---------------- BLOG / ARTICLE (53) ----------------
    ("a-harvest-of-souls", "blog", "Blog"),
    ("after-alpha-whats-next", "blog", "Blog"),
    ("ahab-and-jezebel-optimized", "blog", "Blog"),
    ("ahab-and-jezebel-spirit", "blog", "Blog"),
    ("anointed-for-business-by-ed-silvoso", "blog", "Blog"),
    ("are-you-ready-for-revival", "blog", "Blog"),
    ("are-you-ready-for-the-coming-harvest-of-souls", "blog", "Blog"),
    ("behind-the-scenes-evangelism", "blog", "Blog"),
    ("bible-study-lessons-are-made-easy", "blog", "Blog"),
    ("can-a-christian-be-demonised", "blog", "Blog"),
    ("christian-leadership", "blog", "Blog"),
    ("communion-and-water-baptism", "blog", "Blog"),
    ("demographics-of-the-harvest", "blog", "Blog"),
    ("discipleship-tools-for-the-harvest", "blog", "Blog"),
    ("do-angels-exist", "blog", "Blog"),
    ("does-your-congregation-struggle-to-explain-christianity", "blog", "Blog"),
    ("he-will-keep-you-in-perfect-peace", "blog", "Blog"),
    ("holy-spirit-a-new-era-begins", "blog", "Holy Spirit Series"),
    ("holy-spirit-author-of-gods-word-the-bible-part-3", "blog", "Holy Spirit Series"),
    ("holy-spirit-baptism", "blog", "Holy Spirit Series"),
    ("holy-spirit-is-our-helper", "blog", "Holy Spirit Series"),
    ("holy-spirit-performs-personal-acts", "blog", "Holy Spirit Series"),
    ("holy-spirit-the-birth-and-the-ministry-of-jesus-christ", "blog", "Holy Spirit Series"),
    ("holy-spirit-today", "blog", "Holy Spirit Series"),
    ("how-to-disciple-the-fringe-dwellers", "blog", "Blog"),
    ("husband-and-wife-relationship", "blog", "Blog"),
    ("is-tattooing-and-body-piercing-a-sin", "blog", "Blog"),
    ("is-the-church-a-building-or-a-marketplace-ministry", "blog", "Blog"),
    ("making-disciples-why-is-it-important-christian-discipleship", "blog", "Blog"),
    ("marketplace-ministry", "blog", "Blog"),
    ("pagan-christianity", "blog", "Blog"),
    ("power-of-unforgiveness", "blog", "Blog"),
    ("prophecy-promises", "blog", "Blog"),
    ("restore-family-and-you-restore-society", "blog", "Blog"),
    ("strategies-of-a-religious-spirit", "blog", "Blog"),
    ("spirit-soul-and-body", "blog", "Blog"),
    ("the-church-in-the-whole-world", "blog", "Blog"),
    ("the-holy-spirit-activity-in-the-old-testament", "blog", "Holy Spirit Series"),
    ("the-holy-spirit-in-the-life-and-ministry-of-the-lord-jesus-christ", "blog", "Holy Spirit Series"),
    ("the-holy-spirit-in-the-life-of-the-believer", "blog", "Holy Spirit Series"),
    ("the-kingdom-of-light", "blog", "Blog"),
    ("the-power-of-words-we-speak", "blog", "Blog"),
    ("third-great-awakening", "blog", "Blog"),
    ("this-present-darkness-by-frank-peretti", "blog", "Blog"),
    ("titles-of-holy-spirit-attributes-and-ministry-of-the-holy-spirit", "blog", "Holy Spirit Series"),
    ("two-spiritual-kingdoms", "blog", "Blog"),
    ("we-are-all-called-to-equip-and-disciple-others", "blog", "Blog"),
    ("what-does-christian-discipleship-mean", "blog", "Blog"),
    ("what-does-revival-look-like", "blog", "Blog"),
    ("what-is-christian-discipleship", "blog", "Blog"),
    ("what-is-the-definition-of-ekklesia", "blog", "Blog"),
    ("who-is-jesus-christ", "blog", "Blog"),
    ("wisdom-from-above", "blog", "Blog"),
]

if __name__ == "__main__":
    from collections import Counter
    c = Counter(p[1] for p in PAGES)
    print("TOTAL:", len(PAGES), dict(c))
