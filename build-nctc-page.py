#!/usr/bin/env python3
"""
Build the how-to-open-a-new-christian-training-center.html page (v2).

Reads raw text, joins continuation lines into proper paragraphs,
then wraps in editorial-style HTML matching the site's design system.
"""

import re

# ── 1. Read the existing generated file to extract header/footer ──────────
# We'll read the raw text from the original file backup
# First, let's read the current file to extract the raw content lines
# Actually, let's read the raw text portion from the generated HTML
with open("how-to-open-a-new-christian-training-center.html", "r", encoding="utf-8") as f:
    current_html = f.read()

# Extract the content between the BLUEPRINT CONTENT section markers
# We need the original raw text - let's extract text content from the HTML
import html as html_module
from html.parser import HTMLParser

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.texts = []
        self.in_main = False
        self.in_blueprint = False
        self.skip_tags = {'script', 'style'}
        self.current_tag = None
        
    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        attrs_dict = dict(attrs)
        if attrs_dict.get('class', '').startswith('nctc-blueprint__content'):
            self.in_blueprint = True
            
    def handle_data(self, data):
        if self.in_blueprint and self.current_tag not in self.skip_tags:
            stripped = data.strip()
            if stripped:
                self.texts.append(stripped)

# Instead of trying to extract from HTML, let's work with what we know about the content structure.
# The key issue is that the build script split each line of raw text into separate HTML elements.
# We need to fix the content by: joining fragmented paragraphs and removing misclassified lists.

# Strategy: Parse the current HTML, find all text content in .nctc-blueprint__content blocks,
# extract it, join continuation lines, and regenerate.

# Actually, the simplest approach: read all text nodes from the content sections,
# join lines that are continuations (don't start with uppercase or special patterns),
# and rebuild the HTML.

# Let's extract text between section markers using regex
import re

# Find all content between nctc-blueprint__content divs
content_blocks = re.findall(
    r'<div class="nctc-blueprint__content"[^>]*>(.*?)</div>\s*</div>\s*</section>',
    current_html, re.DOTALL
)

def strip_html_tags(html_str):
    """Remove HTML tags and return plain text lines."""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '\n', html_str)
    # Decode HTML entities
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&quot;', '"')
    text = text.replace('&#x27;', "'")
    text = text.replace('&nbsp;', ' ')
    # Split into lines and clean
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    return lines

def escape_html(text):
    """HTML-escape text."""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    return text

# Also extract section headers (eyebrow + title from nct-course__header)
sections_raw = re.findall(
    r'<section class="nct-course__block[^"]*"[^>]*>(.*?)</section>',
    current_html, re.DOTALL
)

# Parse each section: extract header info + content text
parsed_sections = []
for i, section_html in enumerate(sections_raw):
    # Extract eyebrow
    eyebrow_match = re.search(r'class="eyebrow[^"]*"[^>]*>(.*?)</p>', section_html)
    eyebrow = eyebrow_match.group(1).strip() if eyebrow_match else ""
    
    # Extract section title (h2)
    title_match = re.search(r'<h2[^>]*>(.*?)</h2>', section_html, re.DOTALL)
    title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip() if title_match else ""
    
    # Extract section id
    id_match = re.search(r'id="([^"]+)"', section_html[:200])
    section_id = id_match.group(1) if id_match else f"section-{i}"
    
    # Extract subtitle (section-sub)
    sub_match = re.search(r'class="section-sub"[^>]*>(.*?)</p>', section_html, re.DOTALL)
    subtitle = re.sub(r'<[^>]+>', '', sub_match.group(1)).strip() if sub_match else ""
    
    # Extract content block
    content_match = re.search(r'<div class="nctc-blueprint__content"[^>]*>(.*?)$', section_html, re.DOTALL)
    if content_match:
        content_text_lines = strip_html_tags(content_match.group(1))
    else:
        content_text_lines = []
    
    parsed_sections.append({
        'id': section_id,
        'eyebrow': eyebrow,
        'title': title,
        'subtitle': subtitle,
        'lines': content_text_lines,
    })

def is_heading_line(line):
    """Check if a line is likely a heading (all-caps, short, no sentence-ending punctuation)."""
    if not line or len(line) > 120:
        return False
    alpha = re.sub(r'[^a-zA-Z]', '', line)
    if not alpha:
        return False
    upper_ratio = sum(1 for c in alpha if c.isupper()) / len(alpha)
    if upper_ratio > 0.7 and len(line) > 10 and not line.endswith('.'):
        return True
    return False

def is_session_heading(line):
    """Check if a line is a session heading like 'Session 1: ...'."""
    return bool(re.match(r'^Session\s+\d+:', line))

def is_subheading_line(line):
    """Check if a line is a subheading (title case, short, no period)."""
    if not line or len(line) > 100 or len(line) < 8:
        return False
    if line.endswith('.') or line.endswith(','):
        return False
    words = line.split()
    if len(words) < 2 or len(words) > 12:
        return False
    # Most words should be capitalized
    stop_words = {'a','an','the','and','or','of','in','to','for','is','as','with','on','at','by','from','not','but','that','this','into','than','its','are','be'}
    cap_words = sum(1 for w in words if w[0].isupper() or w.lower() in stop_words)
    return cap_words / len(words) > 0.65

def is_numbered_item(line):
    """Check if line starts with a number like '1. ...'."""
    return bool(re.match(r'^\d+\.\s+', line))

def is_continuation_line(line):
    """Check if a line is a continuation of the previous paragraph (starts lowercase, short)."""
    if not line:
        return False
    # Lines starting with lowercase letters are likely continuations
    if line[0].islower():
        return True
    return False

def join_paragraph_lines(lines):
    """Join continuation lines into proper paragraphs and classify them."""
    result = []  # list of (type, text) tuples
    current_para = []
    
    for line in lines:
        # Skip empty lines
        if not line.strip():
            if current_para:
                result.append(('p', ' '.join(current_para)))
                current_para = []
            continue
        
        # Check for headings
        if is_heading_line(line) and not current_para:
            result.append(('h3', line))
            continue
            
        if is_session_heading(line):
            if current_para:
                result.append(('p', ' '.join(current_para)))
                current_para = []
            result.append(('session', line))
            continue
        
        if is_subheading_line(line) and not current_para:
            result.append(('h4', line))
            continue
        
        if is_numbered_item(line):
            if current_para:
                result.append(('p', ' '.join(current_para)))
                current_para = []
            result.append(('num', line))
            continue
        
        # Check if this is a continuation of previous paragraph
        if current_para and is_continuation_line(line):
            current_para.append(line)
            continue
        
        # Check if this looks like it continues the previous line
        # (previous line doesn't end with sentence-ending punctuation)
        if current_para and not current_para[-1].endswith(('.', '!', '?', ':', '"', '"')):
            current_para.append(line)
            continue
        
        # Start new paragraph
        if current_para:
            result.append(('p', ' '.join(current_para)))
        current_para = [line]
    
    # Flush remaining
    if current_para:
        result.append(('p', ' '.join(current_para)))
    
    return result

def build_content_html(classified_lines, indent="                    "):
    """Convert classified lines into HTML."""
    html_parts = []
    
    for line_type, text in classified_lines:
        escaped = escape_html(text)
        
        if line_type == 'h3':
            slug = re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')
            html_parts.append(f'{indent}<h3 class="nctc-blueprint__major-heading" id="{slug}">{escaped}</h3>')
        
        elif line_type == 'session':
            slug = re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')
            html_parts.append(f'{indent}<h3 class="nctc-blueprint__session-heading" id="{slug}">{escaped}</h3>')
        
        elif line_type == 'h4':
            html_parts.append(f'{indent}<h4 class="nctc-blueprint__sub-heading">{escaped}</h4>')
        
        elif line_type == 'num':
            num_match = re.match(r'^(\d+)\.\s+(.+)', text)
            if num_match:
                num = num_match.group(1)
                rest = escape_html(num_match.group(2))
                html_parts.append(f'{indent}<p class="nctc-blueprint__numbered"><strong>{num}.</strong> {rest}</p>')
            else:
                html_parts.append(f'{indent}<p>{escaped}</p>')
        
        elif line_type == 'scripture':
            html_parts.append(f'{indent}<blockquote class="nctc-blueprint__scripture">')
            html_parts.append(f'{indent}    <p>{escaped}</p>')
            html_parts.append(f'{indent}</blockquote>')
        
        else:  # 'p'
            html_parts.append(f'{indent}<p>{escaped}</p>')
    
    return '\n'.join(html_parts)

# ── 2. Rebuild all section content ────────────────────────────────────────

rebuilt_sections = []
for i, section in enumerate(parsed_sections):
    # Join fragmented lines into proper paragraphs
    classified = join_paragraph_lines(section['lines'])
    content_html = build_content_html(classified)
    
    alt_class = ' nct-course__block--alt' if i % 2 == 1 else ''
    
    section_html = f'''        <section class="nct-course__block{alt_class}" id="{section['id']}" aria-labelledby="{section['id']}-heading">
            <div class="container">
                <div class="nct-course__header" data-aos="fade-up">
                    <p class="eyebrow eyebrow--gold">{escape_html(section['eyebrow'])}</p>
                    <h2 class="section-title" id="{section['id']}-heading">{escape_html(section['title'])}</h2>'''
    
    if section['subtitle']:
        section_html += f'''
                    <p class="section-sub" style="max-width:65ch;">{escape_html(section['subtitle'])}</p>'''
    
    section_html += f'''
                </div>
                <div class="nctc-blueprint__content" data-aos="fade-up" data-aos-delay="100">
{content_html}
                </div>
            </div>
        </section>'''
    
    rebuilt_sections.append(section_html)

all_sections_html = '\n\n'.join(rebuilt_sections)

# ── 3. Read the current file and replace the content sections ─────────────

# Find the start and end markers
# Start: after the blueprint notice section closing
# End: before </main>

# Extract header (everything before the blueprint content sections)
header_match = re.search(
    r'(.*?<!-- ={4,}\s+BLUEPRINT CONTENT.*?-->\n)',
    current_html, re.DOTALL
)
header = header_match.group(1) if header_match else ""

# If no match, find the position after the notice section
if not header:
    header_end = current_html.find('</section>', current_html.find('nctc-blueprint-notice'))
    if header_end > 0:
        header_end = current_html.find('\n', header_end) + 1
        header = current_html[:header_end]

# Extract footer (everything from </main> onwards)
footer_match = re.search(r'(\n\s*</main>.*)', current_html, re.DOTALL)
footer = footer_match.group(1) if footer_match else ""

# Assemble
new_html = header + all_sections_html + footer

# ── 4. Write ──────────────────────────────────────────────────────────────
with open("how-to-open-a-new-christian-training-center.html", "w", encoding="utf-8") as f:
    f.write(new_html)

print(f"✅ Rebuilt page with {len(parsed_sections)} sections")
print(f"   Total lines: {new_html.count(chr(10)) + 1}")

# Show first few sections for verification
for s in parsed_sections[:3]:
    classified = join_paragraph_lines(s['lines'])
    total_paras = sum(1 for t, _ in classified if t == 'p')
    total_headings = sum(1 for t, _ in classified if t in ('h3', 'h4', 'session'))
    print(f"   Section '{s['title'][:50]}': {len(s['lines'])} raw lines → {total_paras} paragraphs, {total_headings} headings")
