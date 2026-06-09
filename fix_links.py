import os
import glob
import re

def fix_links(content):
    # Fix direct absolute paths first
    content = content.replace('href="/"', 'href="index.html"')
    content = content.replace('href="/curriculum"', 'href="curriculum.html"')
    content = content.replace('href="/shop"', 'href="shop.html"')
    content = content.replace('href="/blog"', 'href="blog.html"')
    content = content.replace('href="/contact"', 'href="contact.html"')
    content = content.replace('href="/#free-resources"', 'href="index.html#free-resources"')
    
    def replacer(match):
        a_tag = match.group(0)
        # Check if href is "#"
        if 'href="#"' not in a_tag:
            return a_tag
            
        # extract inner HTML
        inner_html = match.group(2)
        # remove inner tags (like <span class="caret">)
        text = re.sub(r'<[^>]+>', ' ', inner_html)
        # normalize whitespace
        text = ' '.join(text.split())
        
        mapping = {
            'Home': 'index.html',
            'New Christian Training': 'new-christian-training.html',
            'Why Moves of God Succeeded and Faded': 'why-moves-of-god-succeeded-and-faded.html',
            'How to Open a New Christian Training Center': 'how-to-open-a-new-christian-training-center.html',
            'Curriculum': 'curriculum.html',
            'Be A Coach / Coaching': 'coach.html',
            'Be A Coach Online Training': 'coach.html',
            'Be A Disciple / Discipleship': 'disciple.html',
            'I Want to Be a Disciple': 'disciple.html',
            'I Want to Coach Others': 'coach.html',
            'Curriculum / Course Outline': 'curriculum.html',
            'New Christian Training Centres': 'new-christian-training.html',
            'New Christian Training Hubs': 'new-christian-training.html'
        }
        
        if text in mapping:
            return a_tag.replace('href="#"', f'href="{mapping[text]}"')
            
        return a_tag

    # Match <a ...>...</a>
    content = re.sub(r'<a([^>]*)>(.*?)</a>', replacer, content, flags=re.DOTALL | re.IGNORECASE)
    
    # Also fix <a href="#lead-magnet"...> in how-to-open which should go to index.html#lead-magnet? Wait, leave #lead-magnet alone if it's on the same page.
    
    return content

if __name__ == '__main__':
    html_files = glob.glob('*.html')
    for filename in html_files:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content = fix_links(content)
        
        if new_content != content:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {filename}")
