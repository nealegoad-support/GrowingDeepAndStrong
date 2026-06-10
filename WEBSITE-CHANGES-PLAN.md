# Website Changes Plan
### Based on Meeting: CarlandMe (1).mp3

---

## STATUS LEGEND
- ✅ DONE — implemented
- ⏳ REQUIRES EXTERNAL ACCESS — cannot be done in code alone
- 🔲 PENDING — not yet started

---

## 1. TYPOGRAPHY ✅ DONE

| Element | Font | Notes |
|---|---|---|
| All headings (h1–h6) | **Roboto Slab** | Decided after trialling Lora → Playfair Display → Roboto Slab |
| Body text | **Open Sans** | Replaces Inter |
| `.brand__wordmark` ("Growing Deep *and* Strong®") | **EB Garamond** | Kept — trademarked/corporate identity, DO NOT change |
| `.brand__tag` ("Christian Discipleship") | **Inter** | Kept — part of brand wordmark block |

---

## 2. HOMEPAGE HERO SECTION ✅ DONE

### Hero Image ✅
- Replaced old landscape JPG with **Blueprint for Success Poster Text.png**
- Image has "Growing Deep and Strong®", "Blueprint for Success", "Jeremiah 17:7-8" embedded — not readable by Google
- Navy scripture caption strip below image removed (now embedded in image)

### Homepage H1 ✅
- Changed from "Taking people from a pagan background..." to **"Start Your Own New Christian Training Center"** (keyword-rich)
- Eyebrow "The Big Vision" wording removed — now reads "New Christian Training Centres"

---

## 3. HOMEPAGE CALL-TO-ACTION BOXES ✅ DONE

Three dark card panels side-by-side on desktop, stacked on mobile:

| Box | Label | Links To |
|---|---|---|
| Box 1 | **I Want to Be a Disciple** | `disciple.html` |
| Box 2 | **I Want to Coach Others** | `coach.html` |
| Box 3 | **Get Your Free Download** | `#free-resources` section |

- 3-column grid at 1024px+, 2-column at 800px, single column on mobile
- "Coach Others" renamed to "I Want to Coach Others"

---

## 4. CONTENT RELOCATIONS ✅ DONE

- "Taking people from a pagan background to a societal reformer — within 12 months or less." already lives as H1 on `coach.html` — homepage H1 replaced with SEO headline above
- No further moves needed

---

## 5. HEADING HIERARCHY / SEO ✅ DONE

- Homepage H1 is now "Start Your Own New Christian Training Center" — keyword-rich
- `coach.html` H1: "Take people from a pagan background to a societal reformer — within 12 months or less." — appropriate for coach page
- `disciple.html` and `curriculum.html` H1s confirmed appropriate for their pages

---

## 6. BACKGROUND / COLOR SCHEME ✅ DONE

- `.nctc-vision` section (main homepage content area) changed from **dark navy gradient → cream/white background** with dark text
- Free download opt-in sidebar (`.nctc-optin`) kept as **solid navy box** — standout accent on white background
- Hero-split CTA cards kept dark navy — strong contrast on cream background
- All text colors within the section updated for readability on light background

---

## 7. SEO AUDIT & KEYWORD REFRESH ⏳ REQUIRES EXTERNAL ACCESS

### Audit Existing Live Site
- Pull all current meta descriptions, page titles, and URL slugs from **growingdeepandstrong.com**
- Tools available: **Semrush**, **SE Ranking**
- Goal: ensure nothing keyword-rich is accidentally lost during the rebuild

### Keyword Research Refresh
- Existing keyword spreadsheet: done in **2022** (Excel — Global + Australia tabs, competitor analysis)
- Needs a fresh search to check what's changed
- Use outside SEO tools (not solely Google Ads — biased toward paid spend)

### Target Keywords (from meeting)
- "New Christian Training Center"
- "Christian discipleship"
- "Servant leadership"
- "Discipling new Christians"
- "Start your own Christian training center"
- Long-tail variants of the above

**Action needed:** Share live site access or export Semrush/SE Ranking report so meta descriptions can be reviewed and updated in the HTML files.

---

## 8. MOBILE UX ✅ DONE (structure) / 🔲 QA PENDING

- Three CTA boxes are positioned directly below the hero — visible early on mobile scroll
- Cards stack to single column on mobile
- Full mobile QA (visual check on a real phone) still needed once hosted/live

---

## 9. NAVIGATION / PAGE LABELS ✅ CONFIRMED

Nav labels are consistent across all pages:
- "Be A Coach / Coaching" — consistent
- "Be A Disciple / Discipleship" — consistent

---

## SUMMARY

| # | Item | Status |
|---|---|---|
| 1 | Typography (Roboto Slab + Open Sans) | ✅ Done |
| 2 | Hero image + keyword H1 | ✅ Done |
| 3 | Three CTA boxes | ✅ Done |
| 4 | Content relocation (coach headline) | ✅ Done |
| 5 | H1 SEO fix | ✅ Done |
| 6 | White background theme | ✅ Done |
| 7 | SEO audit (live site meta/keywords) | ⏳ Needs live site access |
| 8 | Mobile QA | 🔲 Pending — test on real device |
| 9 | Nav consistency | ✅ Confirmed |
