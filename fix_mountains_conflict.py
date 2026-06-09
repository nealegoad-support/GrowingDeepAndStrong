import re

# Update coach.html
with open('coach.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Specifically replace class="mountains" with class="coach-mountains" and class="mountains__header" with class="coach-mountains__header"
content = content.replace('class="mountains"', 'class="coach-mountains"')
content = content.replace('class="mountains__header"', 'class="coach-mountains__header"')
# Also update the aria-labelledby if needed but that's fine.

with open('coach.html', 'w', encoding='utf-8') as f:
    f.write(content)

# Update style.css
with open('style.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
in_c5_section = False
for i, line in enumerate(lines):
    if "C5. 7 MOUNTAINS MANDATE" in line:
        in_c5_section = True
        
    # We only rename .mountains and .mountains__header
    # But leave .mountains-grid as is, since it's shared!
    if in_c5_section:
        if '.mountains {' in line:
            line = line.replace('.mountains', '.coach-mountains')
        elif '.mountains ' in line: # covers media query
            line = line.replace('.mountains', '.coach-mountains')
        elif '.mountains__header' in line:
            line = line.replace('.mountains__header', '.coach-mountains__header')
            
    if "CSS Grid for auto-wrapping items" in line:
        in_c5_section = False # stop replacing

    new_lines.append(line)

with open('style.css', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Decoupled .mountains to .coach-mountains in coach.html and style.css")
